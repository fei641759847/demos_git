#coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import requests,lxml,json,re,time
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import threading,random
import pymysql
import logging
from fake_useragent import UserAgent

#创建随机的请求头部
def createHeader():
  ua=UserAgent()
  header={'User-Agent':ua.random}
  return header

###############日志模块##################
logging.basicConfig(level=logging.WARNING,
  format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
  filename='./house_v2.log',
  filemod='w')
console = logging.StreamHandler()
console.setLevel(logging.WARNING)
formatter = logging.Formatter('%(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
##########################################

############要获取的城市##################
#cities=[u'武汉']
cities=[]
def buding():
  #获取省份url
  createProvinceUrls()
  #获取城市url
  createCityUrls()
  #先清空数据
  #delete_db()
  #cities_list=[u'贵阳',u'北京',u'上海',u'重庆',u'天津',u'南京',u'东莞',u'广州',u'珠海',u'惠州',u'中山']
  cities_list=[u'武汉',u'合肥']
  for i in cities_list:
    global cities
    cities=[i]
    #print i
    #print cities
    main()
##########################################
#province_urls中存放省份的url，{湖南:http:...}
province_urls={}
#url_all存放所有url,{湖南:{长沙：url...}...}
urls_all={}
#info_list存放所有获取到的数据
info_list=[]

#url条件限制
def formateUrl():
  #开始时间&auction_start_from=2017-10-1
  #中止时间&auction_start_to=2017-11-30
  #可贷款&support_loans=1
  #已结束&sorder=2中止&sorder=4撤回&sorder=5
  base_url='https://sf.taobao.com/item_list.htm?spm=a213w.3064813.a214dqe.3.RdVmDP&category=50025969'
  starttime='2017-10-1'
  url=base_url+'&auction_start_from='+starttime+'&auction_start_to=2017-11-30'
  return url
base_url=formateUrl()

def createProvinceUrls():
  logging.warning(u'开始获取所有省份的url...')
  header=createHeader()
  response=requests.get(base_url,timeout=5,headers=header)
  soup=BeautifulSoup(response.text,'lxml')
  soup_urls=soup.select('ul.condition > li.triggle > em > a')
  for i in soup_urls:
    #获取到的城市名后面有个中文空格，所以去掉
    province_urls[i.text[:-1]]='https://'+i['href'].split('//')[1]
  logging.warning(u'共取得%s'%len(province_urls))

def createCityUrls():
  logging.warning(u'开始获取每个城市的url...')
  for i in province_urls:
    city_urls_one={}
    try:
      header=createHeader()
      response=requests.get(province_urls[i],timeout=5,headers=header)
      soup=BeautifulSoup(response.text,'lxml')
      soup_urls=soup.select('li.unfold > div.sub-condition > ul > li > em > a')
      for j in soup_urls:
        city_urls_one[j.text]='https://'+j['href'].split('//')[1]
    except:
      logging.error(i+u'的城市url获取出错')
    urls_all[i]=city_urls_one
  logging.warning(u'每个城市的url获取结束')

#得到单个城市的页数
def getPages(url):
  try:
    response=requests.get(url)
    soup=BeautifulSoup(response.text,'lxml')
    total_page_soup=soup.select_one('span.page-skip > em.page-total')
    if total_page_soup:
      total_page=int(total_page_soup.text)
      return total_page
    else:
      return 0
  except:
    logging.error('get page filed:'+url)

#生成当前城市每一页的url
def createPageUrl(url_city):
  total_page=getPages(url_city)
  urls_page=[]
  if total_page!=0:
    for i in range(1,total_page+1):
      urls_page.append(url_city+'&page='+str(i))
  return urls_page

#这里需要一个城市单页的url
#爬取数据，忽视函数名
def createEveryUrls(url,province,city):
  info={}
  try:
    header=createHeader()
    response=requests.get(url,timeout=5,headers=header)
    soup=BeautifulSoup(response.text,'lxml')
    data_thispage=soup.select_one('script#sf-item-list-data').text
    #print 'start json'
    data=json.loads(data_thispage)
    #print data['data'][0]
    for i in data['data']:
      #省份，城市
      info['province']=province
      info['city']=city
      #当前房产的url
      info['itemurl']='https:'+i['itemUrl']
      #当前房产的名字
      info['target']=i['title']
      logging.warning(u'获取到：'+i['title'])
      #评估价
      info['consultPrice']=i['consultPrice']
      #当前价
      info['currentPrice']=i['currentPrice']
      #出价次数
      info['bidCount']=i['bidCount']
      #报名人数
      info['applyCount']=i['applyCount']
      #时间
      time_s_l=time.localtime(i['start']/1000)
      time_e_l=time.localtime(i['end']/1000)
      t_s=time.strftime('%Y-%m-%d %H:%M:%S',time_s_l)
      t_e=time.strftime('%Y-%m-%d %H:%M:%S',time_e_l)
      info['start']=t_s
      info['end']=t_e
      #状态
      info['status']=i['status']
      #是否可贷款
      info['supportOrgLoan']=i['supportOrgLoan']
      #获取更多信息
      res=requests.get(info['itemurl'],timeout=5,headers=header)
      sou=BeautifulSoup(res.text,'lxml')
      #处置单位
      soup_department=sou.select_one('div.pai-info > p:nth-of-type(2) > a')
      if soup_department:
        info['department']=soup_department.text
      else:
        info['department']='-'
      #起拍价
      soup_price=sou.select('span.pay-price > span.J_Price')
      info['startPrice']=soup_price[0].text.strip('\n')
      info['startPrice']=info['startPrice'].replace(',','')
      #获取描述信息的url并请求页面
      url_desc='http:'+sou.select('#J_desc')[0].attrs['data-from']
      response_desc=requests.get(url_desc,timeout=5,headers=header)
      soup_desc=BeautifulSoup(response_desc.text,'lxml')
      #用途
      info['property']='-'
      detail = [u'办公；',u'、商业；',u'、成套住宅；',u'办公用房',u'、其它；',u'、商服（住宅）；',u'、办公；',u'、住宅；',u'城镇住宅用地',u'商业服务',u'住宅用地',u'、商服用地；',u'1、住宅。',u'办公',u'工业',u'仓储',u'非居住', u'商业', u'非住宅', u'住宅', u'工业用地', u'工业用途房地产', u'、其他商服用地', u'其他商服用地', u'办公写字楼', u'商住综合用地',u'综合',u'商用；']
      for d in detail:
        prope=soup_desc.find(text=d)
        if prope:
          info['property']=prope
      #暂时定义流拍率
      info['pass_in']='-'
      info_list.append(info)
  except:
    logging.warning('createEveryUrls error:'+url)

#把每个城市加入到一个线程中
def addThread():
  thread_list=[]
  for city in cities:
    for province in urls_all:
      if urls_all[province].has_key(city):
        #创建这个城市每一页的url列表
        url_list=createPageUrl(urls_all[province][city])
        for url in url_list:
          thread_list.append(threading.Thread(target=createEveryUrls,args=(url,province,city)))
  logging.warning(u'共创建了%s个线程'%(len(thread_list)))
  return thread_list

def getData():
  thread_list=addThread()
  for i in thread_list:
    i.start()
  for j in thread_list:
    j.join()

#数据库操作
dbconfig={
  'host':'127.0.0.1',
  'port':3306,
  'user':'root',
  'password':'123.com',
  'db':'spider',
  'charset':'utf8'
}
def delete_db():
  logging.warning('delete old db start')
  conn=pymysql.connect(**dbconfig)
  cur=conn.cursor()
  cur.execute('delete from house_v2')
  cur.close()
  conn.commit()
  conn.close()
  logging.warning('delete old db success')

def insert_db(j):
  try:
    conn=pymysql.connect(**dbconfig)
    cur=conn.cursor()
    sql="insert into house_v2 (province,city,target,currentPrice,bidCount,consultPrice,applyCount,supportOrgLoan,start,end,status,department,startPrice,property,pass_in,itemurl) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    data=(j['province'],j['city'],j['target'],j['currentPrice'],j['bidCount'],j['consultPrice'],j['applyCount'],j['supportOrgLoan'],j['start'],j['end'],j['status'],j['department'],j['startPrice'],j['property'],j['pass_in'],j['itemurl'])
    #print(data)
    cur.execute(sql,data)
    cur.close()
    conn.commit()
    conn.close()
  except:
    logging.warning('one message insert into db error')
#数据库入口函数
def db():
  logging.warning('db function start')
  #delete_db()
  logging.warning('insert into db start')
  for i in info_list:
    insert_db(i)
  logging.warning('db function end')

def pass_func():
#统计流拍及成功次数，department_list的值前面是流拍次数，后面是成功次数
  department_dict={}
  for i in info_list:
    if i['department'] not in department_dict:
      department_dict[i['department']]=[0,0]
    else:
      if (i['status']=='done' or i['status']=='failure') and i['bidCount']==0:
        #流拍加1
        department_dict[i['department']][0]+=1
      elif (i['status']=='done' or i['status']=='failure') and i['bidCount']!=0:
        #成功加1
        department_dict[i['department']][1]+=1
#把流拍率加入到总数据中去
  for j in info_list:
    pass_no=department_dict[j['department']][0]
    pass_yes=department_dict[j['department']][1]
    if pass_no+pass_yes==0:
      pass_per=0
    else:
      pass_per=pass_no/float(pass_no+pass_yes)
    j['pass_in']='%.1f'%(pass_per*100)+'%'

#主函数入口
def main():
  t_s=time.strftime('%H:%M:%S',time.localtime(time.time()))
  #抓取数据
  getData()
  #计算流拍率
  pass_func()
  #存储到mysql
  db()
  #执行完数据库存储后再次把info_list置空
  global info_list
  info_list=[]
  t_e=time.strftime('%H:%M:%S',time.localtime(time.time()))
  logging.warning('start time:'+t_s)
  logging.warning('end time:'+t_e)

if __name__=='__main__':
  buding()
