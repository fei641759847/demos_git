#coding: utf-8
#written by zhanghongfei 2017-12-18
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
import re
from requests.adapters import HTTPAdapter
from multiprocessing import Pool

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
cities_all=[]
def buding():
  t_s=time.strftime('%H:%M:%S',time.localtime(time.time()))
  #获取省份url
  createProvinceUrls()
  #获取城市url
  createCityUrls()
  for i in urls_all:
    for j in urls_all[i]:
      cities_all.append(j)
  #print cities_all
  print len(cities_all)
  #先清空数据
  #delete_db()
  #cityNum()
  cities_list=[u'合肥',u'兰州',u'南宁',u'贵阳',u'海口',u'三亚',u'哈尔滨',u'长春',u'南昌',u'大连',u'沈阳',u'济南',u'青岛',u'烟台',u'太原',u'西安',u'乌鲁木齐',u'昆明',u'宁波',u'绍兴',u'温州',u'北京',u'上海',u'重庆',u'天津',u'南京',u'东莞',u'广州',u'深圳',u'珠海',u'惠州',u'中山',u'嘉兴',u'金华',u'台州',u'石家庄']
  #cities_list=[u'长沙',u'张家界',u'合肥',u'兰州',u'南宁']
  pool=Pool(10)
  for i in cities_list:
  #for i in cities_all:
    #global cities
    cities=[i]
    #print i
    #print cities
    #main()
    pool.apply_async(func=main,args=(cities,),callback=None)
  pool.close()
  pool.join()
  t_e=time.strftime('%H:%M:%S',time.localtime(time.time()))
  logging.warning('total start time:'+t_s)
  logging.warning('total end time:'+t_e)
##########################################
#province_urls中存放省份的url，{湖南:http:...}
province_urls={}
#url_all存放所有url,{湖南:{长沙：url...}...}
urls_all={}
#info_list存放所有获取到的数据
info_list=[]
#定义一个城市名和数字的映射关系
city_num={u'\u5357\u5145': 58, u'\u6f33\u5dde': 101, u'\u6e05\u8fdc': 190, u'\u9ec4\u5357': 82, u'\u8386\u7530': 100, u'\u4f5b\u5c71': 189, u'\u6b66\u5a01': 244, u'\u5854\u57ce': 88, u'\u9e70\u6f6d': 147, u'\u4e09\u4e9a': 149, u'\u6069\u65bd': 120, u'\u9e64\u5c97': 175, u'\u9e21\u897f': 177, u'\u5b9c\u5bbe': 54, u'\u5b89\u9633': 15, u'\u901a\u8fbd': 296, u'\u547c\u548c\u6d69\u7279': 301, u'\u9ed1\u6cb3': 166, u'\u6986\u6797': 232, u'\u8302\u540d': 186, u'\u963f\u62c9\u5c14': 90, u'\u695a\u96c4': 205, u'\u53a6\u95e8': 107, u'\u5bbf\u5dde': 308, u'\u963f\u575d': 45, u'\u9ec4\u5188': 121, u'\u6587\u5c71': 203, u'\u6d77\u5317': 80, u'\u63ed\u9633': 195, u'\u4f0a\u6625': 174, u'\u4e09\u95e8\u5ce1': 22, u'\u510b\u5dde': 164, u'\u67f3\u5dde': 219, u'\u4e1c\u839e': 185, u'\u4e09\u660e': 106, u'\u5468\u53e3': 24, u'\u5b89\u5e86': 315, u'\u5fb7\u5b8f': 208, u'\u4e0a\u9976': 140, u'\u4e50\u4e1c': 156, u'\u7389\u6eaa': 209, u'\u4fdd\u4ead': 161, u'\u6b66\u6c49': 132, u'\u6c60\u5dde': 321, u'\u8944\u9633': 128, u'\u5f00\u5c01': 14, u'\u5185\u6c5f': 55, u'\u963f\u62c9\u5584': 305, u'\u4e34\u6c82': 41, u'\u6dee\u5357': 316, u'\u671d\u9633': 341, u'\u5927\u5e86': 171, u'\u9675\u6c34': 153, u'\u5b9a\u897f': 243, u'\u4e34\u6ca7': 210, u'\u5410\u9c81\u756a': 96, u'\u91d1\u660c': 249, u'\u5170\u5dde': 246, u'\u9075\u4e49': 5, u'\u6cf0\u5b89': 40, u'\u5357\u901a': 77, u'\u6dee\u5317': 317, u'\u51c9\u5c71': 50, u'\u961c\u65b0': 342, u'\u677e\u539f': 276, u'\u666f\u5fb7\u9547': 146, u'\u8d35\u9633': 4, u'\u8d35\u6e2f': 223, u'\u5e38\u5dde': 74, u'\u5415\u6881': 335, u'\u4e94\u6307\u5c71': 154, u'\u8346\u5dde': 127, u'\u626c\u5dde': 75, u'\u6d77\u53e3': 150, u'\u6797\u829d': 337, u'\u56db\u5e73': 272, u'\u6500\u679d\u82b1': 65, u'\u8d63\u5dde': 145, u'\u5a01\u6d77': 37, u'\u8346\u95e8': 131, u'\u6d77\u5357\u85cf\u65cf': 79, u'\u4e4c\u9c81\u6728\u9f50': 85, u'\u7389\u6797': 224, u'\u8861\u9633': 288, u'\u6842\u6797': 217, u'\u7ea2\u6cb3': 213, u'\u676d\u5dde': 116, u'\u4e34\u6c7e': 325, u'\u9752\u5c9b': 38, u'\u5305\u5934': 304, u'\u5e7f\u5143': 63, u'\u5e73\u9876\u5c71': 27, u'\u4ed9\u6843': 119, u'\u53f0\u5dde': 111, u'\u7518\u5b5c': 59, u'\u7518\u5357': 254, u'\u9f99\u5ca9': 99, u'\u5e86\u9633': 248, u'\u4fdd\u5c71': 201, u'\u4e2d\u5c71': 193, u'\u6f84\u8fc8': 151, u'\u65b0\u4f59': 137, u'\u7261\u4e39\u6c5f': 172, u'\u6e56\u5dde': 117, u'\u6e58\u6f6d': 283, u'\u6f2f\u6cb3': 26, u'\u4e50\u5c71': 46, u'\u6dee\u5b89': 66, u'\u4e4c\u6d77': 300, u'\u91cd\u5e86': 271, u'\u7126\u4f5c': 17, u'\u5341\u5830': 129, u'\u77f3\u5634\u5c71': 266, u'\u9999\u6e2f\u5c9b': 323, u'\u5bbf\u8fc1': 78, u'\u5408\u80a5': 320, u'\u5357\u5b81': 220, u'\u5b5d\u611f': 124, u'\u6210\u90fd': 53, u'\u6d77\u897f': 81, u'\u6587\u660c': 159, u'\u6e29\u5dde': 110, u'\u5ef6\u5b89': 233, u'\u664b\u57ce': 332, u'\u90b5\u9633': 290, u'\u9e64\u58c1': 18, u'\u535a\u5c14\u5854\u62c9': 87, u'\u627f\u5fb7': 258, u'\u65e5\u7167': 31, u'\u664b\u4e2d': 331, u'\u5c6f\u660c': 158, u'\u6000\u5316': 289, u'\u6f6e\u5dde': 183, u'\u70df\u53f0': 33, u'\u5e38\u5fb7': 293, u'\u8bb8\u660c': 12, u'\u660c\u5409': 92, u'\u798f\u5dde': 103, u'\u5e7f\u5b89': 62, u'\u6d4e\u5357': 44, u'\u629a\u987a': 350, u'\u5c71\u5357': 339, u'\u9547\u6c5f': 68, u'\u6f5c\u6c5f': 123, u'\u77f3\u5bb6\u5e84': 260, u'\u5f20\u5bb6\u754c': 285, u'\u5409\u5b89': 142, u'\u8087\u5e86': 184, u'\u4fe1\u9633': 19, u'\u592a\u539f': 327, u'\u8fbd\u6e90': 275, u'\u9f50\u9f50\u54c8\u5c14': 168, u'\u53cc\u9e2d\u5c71': 169, u'\u82cf\u5dde': 73, u'\u65b0\u4e61': 20, u'\u6c38\u5dde': 291, u'\u660c\u6c5f': 162, u'\u8862\u5dde': 115, u'\u6c55\u5934': 196, u'\u804a\u57ce': 32, u'\u5a04\u5e95': 292, u'\u9ed4\u897f\u5357': 8, u'\u6d1b\u9633': 10, u'\u9632\u57ce\u6e2f': 218, u'\u4e34\u9ad8': 152, u'\u54b8\u5b81': 125, u'\u76d8\u9526': 344, u'\u846b\u82a6\u5c9b': 346, u'\u94a6\u5dde': 229, u'\u5d07\u5de6': 226, u'\u6c5f\u95e8': 191, u'\u9152\u6cc9': 245, u'\u5357\u660c': 141, u'\u5b9a\u5b89': 165, u'\u8fbd\u9633': 352, u'\u8861\u6c34': 263, u'\u5ba3\u57ce': 310, u'\u9a6c\u978d\u5c71': 313, u'\u56fa\u539f': 267, u'\u90f4\u5dde': 281, u'\u4f0a\u7281': 97, u'\u9ed4\u5357': 2, u'\u672c\u6eaa': 345, u'\u9526\u5dde': 349, u'\u968f\u5dde': 122, u'\u5927\u5174\u5b89\u5cad': 173, u'\u5546\u4e18': 13, u'\u7ecd\u5174': 114, u'\u516d\u76d8\u6c34': 3, u'\u6d4e\u5b81': 30, u'\u514b\u5b5c\u52d2\u82cf\u67ef\u5c14\u514b\u5b5c': 94, u'\u6e58\u897f': 294, u'\u7ee5\u5316': 176, u'\u5434\u5fe0': 269, u'\u91d1\u534e': 118, u'\u65e0\u9521': 67, u'\u96c5\u5b89': 47, u'\u4eb3\u5dde': 318, u'\u4e34\u590f': 250, u'\u90a2\u53f0': 262, u'\u5eca\u574a': 264, u'\u6606\u660e': 214, u'\u6df1\u5733': 180, u'\u5b81\u6ce2': 109, u'\u90af\u90f8': 265, u'\u9ed4\u4e1c\u5357': 7, u'\u8fd0\u57ce': 329, u'\u9ec4\u77f3': 134, u'\u743c\u6d77': 148, u'\u901a\u5316': 278, u'\u4e0a\u6d77': 324, u'\u6f4d\u574a': 28, u'\u8d3a\u5dde': 227, u'\u666e\u6d31': 211, u'\u767d\u57ce': 279, u'\u8d44\u9633': 64, u'\u8fde\u4e91\u6e2f': 72, u'\u66f2\u9756': 200, u'\u957f\u6cbb': 328, u'\u5174\u5b89': 302, u'\u6e5b\u6c5f': 197, u'\u54c8\u5c14\u6ee8': 170, u'\u547c\u4f26\u8d1d\u5c14': 297, u'\u6e2d\u5357': 236, u'\u978d\u5c71': 348, u'\u957f\u6c99': 282, u'\u4e2d\u536b': 268, u'\u6cf8\u5dde': 57, u'\u9647\u5357': 241, u'\u83cf\u6cfd': 34, u'\u5fb7\u9633': 61, u'\u94dc\u4ec1': 6, u'\u5e7f\u5dde': 179, u'\u961c\u9633': 312, u'\u5cb3\u9633': 284, u'\u5927\u8fde': 343, u'\u4e39\u4e1c': 353, u'\u840d\u4e61': 138, u'\u516d\u5b89': 314, u'\u6885\u5dde': 188, u'\u5b89\u5eb7': 235, u'\u5609\u5cea\u5173': 252, u'\u6c88\u9633': 351, u'\u7ef5\u9633': 52, u'\u6d77\u4e1c': 83, u'\u963f\u52d2\u6cf0': 98, u'\u9042\u5b81': 48, u'\u6cc9\u5dde': 102, u'\u6cb3\u6e90': 187, u'\u8425\u53e3': 347, u'\u4fdd\u5b9a': 261, u'\u5b9c\u660c': 133, u'\u4e03\u53f0\u6cb3': 167, u'\u6ec1\u5dde': 319, u'\u6714\u5dde': 326, u'\u5f20\u5bb6\u53e3': 255, u'\u94dc\u9675': 309, u'\u6012\u6c5f': 207, u'\u5e73\u51c9': 251, u'\u76ca\u9633': 287, u'\u5317\u6d77': 225, u'\u5b9c\u6625': 144, u'\u5929\u6c34': 247, u'\u9633\u6cc9': 333, u'\u54b8\u9633': 239, u'\u81ea\u8d21': 49, u'\u4e91\u6d6e': 199, u'\u5b89\u987a': 1, u'\u4e3d\u6c5f': 206, u'\u5317\u4eac': 216, u'\u62c9\u8428': 336, u'\u963f\u91cc': 338, u'\u897f\u5b89': 238, u'\u5b9d\u9e21': 237, u'\u897f\u5b81': 84, u'\u4e3d\u6c34': 108, u'\u5580\u4ec0': 86, u'\u9a7b\u9a6c\u5e97': 11, u'\u94dc\u5ddd': 231, u'\u83b1\u829c': 43, u'\u6765\u5bbe': 228, u'\u5df4\u97f3\u90ed\u695e': 95, u'\u662d\u901a': 215, u'\u8fbe\u5dde': 51, u'\u4e94\u5bb6\u6e20': 89, u'\u6fee\u9633': 16, u'\u829c\u6e56': 307, u'\u6c55\u5c3e': 181, u'\u9633\u6c5f': 182, u'\u4e5d\u6c5f': 139, u'\u629a\u5dde': 143, u'\u94c1\u5cad': 340, u'\u67a3\u5e84': 42, u'\u5927\u7406': 204, u'\u5fb7\u5dde': 39, u'\u5927\u540c': 334, u'\u94f6\u5ddd': 270, u'\u6bd5\u8282': 9, u'\u682a\u6d32': 286, u'\u73e0\u6d77': 194, u'\u4e07\u5b81': 160, u'\u897f\u53cc\u7248\u7eb3': 202, u'\u5ffb\u5dde': 330, u'\u4e4c\u5170\u5bdf\u5e03': 298, u'\u4e1c\u65b9': 157, u'\u5df4\u4e2d': 56, u'\u5f20\u6396': 253, u'\u6d4e\u6e90': 23, u'\u4f73\u6728\u65af': 178, u'\u6cf0\u5dde': 69, u'\u97f6\u5173': 192, u'\u6dc4\u535a': 36, u'\u5929\u6d25': 136, u'\u795e\u519c\u67b6': 130, u'\u9102\u5c14\u591a\u65af': 299, u'\u5357\u5e73': 104, u'\u6cb3\u6c60': 230, u'\u9ec4\u5c71': 322, u'\u5510\u5c71': 256, u'\u767d\u5c71': 274, u'\u868c\u57e0': 311, u'\u5546\u6d1b': 234, u'\u5409\u6797': 277, u'\u9102\u5dde': 135, u'\u6ee8\u5dde': 29, u'\u5f90\u5dde': 71, u'\u963f\u514b\u82cf': 91, u'\u4e1c\u8425': 35, u'\u5357\u9633': 21, u'\u68a7\u5dde': 221, u'\u5df4\u5f66\u6dd6\u5c14': 303, u'\u60e0\u5dde': 198, u'\u767e\u8272': 222, u'\u957f\u6625': 280, u'\u743c\u4e2d': 163, u'\u5ef6\u8fb9\u671d\u9c9c\u65cf': 273, u'\u7709\u5c71': 60, u'\u767d\u6c99': 155, u'\u5609\u5174': 112, u'\u514b\u62c9\u739b\u4f9d': 93, u'\u6c49\u4e2d': 240, u'\u8fea\u5e86': 212, u'\u76d0\u57ce': 76, u'\u767d\u94f6': 242, u'\u9521\u6797\u90ed\u52d2': 295, u'\u79e6\u7687\u5c9b': 257, u'\u5929\u95e8': 126, u'\u8d64\u5cf0': 306, u'\u6ca7\u5dde': 259, u'\u5357\u4eac': 70, u'\u821f\u5c71': 113, u'\u90d1\u5dde': 25, u'\u5b81\u5fb7': 105}
#city_num={}
def cityNum():
  print 'cityNum create'
  i=1
  for city in cities_all:
    city_num[city]=i
    i+=1
  #print city_num
#url条件限制
def formateUrl():
  #开始时间&auction_start_from=2017-10-1
  #中止时间&auction_start_to=2017-11-30
  #可贷款&support_loans=1
  #已结束&sorder=2中止&sorder=4撤回&sorder=5
  base_url='https://sf.taobao.com/item_list.htm?spm=a213w.3064813.a214dqe.3.RdVmDP&category=50025969'
  starttime='2017-11-1'
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
    return 0

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
  try:
    header=createHeader()
    #response=requests.get(url,timeout=5,headers=header)
    s=requests.Session()
    s.mount('http://',HTTPAdapter(max_retries=3))
    s.mount('https://',HTTPAdapter(max_retries=3))
    response=s.get(url,timeout=5,headers=header)
    soup=BeautifulSoup(response.text,'lxml')
    data_thispage=soup.select_one('script#sf-item-list-data').text
    #print 'start json'
    data=json.loads(data_thispage)
    #print data['data'][0]
    for i in data['data']:
      info={}
      #省份，城市
      info['province']=province
      info['city']=city
      info['citynum']=city_num[city]
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
      info['supportOrgLoan']=i['supportOrgLoan']+i['supportLoans']
      #print info['supportOrgLoan'],type(info['supportOrgLoan'])
      #获取更多信息
      res=s.get(info['itemurl'],timeout=5,headers=header)
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
      #增加辅助机构
      try:
        url_notice = sou.select('#J_ItemNotice')[0].attrs['data-from']
        url_notice = 'https:' + url_notice
        response_notice = s.get(url_notice, timeout=5, headers=header)
        res_comp=re.findall(u'拍卖辅助机构：(.*)公司',response_notice.text.decode('utf8'))
        res_tel=re.findall(u'辅助机构咨询电话：<span>(\d\d\d\d\d\d\d*)\D+',response_notice.text.decode('utf8'))
        if len(res_comp)>=1:
          info['company']=res_comp[0]+u'公司'
          #print(res_comp[0])
        else:
          info['company']='-'
          #print('nothing',end='')
        if len(res_tel)>=1:
          info['tel']=res_tel[0]
          #print(res_tel[0])
        else:
          res_tel=re.findall(u'辅助机构咨询电话：</span></strong><span style=\"font-size: 19.0px;\">(\d\d\d\d\d\d\d*)\D+',response_notice.text)
          if len(res_tel)>=1:
            info['tel']=res_tel[0]
          else:
              info['tel']='-'
      except:
        info['company']='-'
        info['tel']='-'
      #获取描述信息的url并请求页面
      url_desc='http:'+sou.select('#J_desc')[0].attrs['data-from']
      response_desc=s.get(url_desc,timeout=5,headers=header)
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
    logging.warning('createEveryUrls error:'+city)

#把每个城市加入到一个线程中
def addThread(cities):
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

def getData(cities):
  thread_list=addThread(cities)
  for i in thread_list:
    i.start()
  for j in thread_list:
    j.join()
"""
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
  cur.execute('delete from house_v3')
  cur.close()
  conn.commit()
  conn.close()
  logging.warning('delete old db success')

def insert_db(j):
  try:
    conn=pymysql.connect(**dbconfig)
    cur=conn.cursor()
    sql="insert into house_v3 (province,city,target,currentPrice,bidCount,consultPrice,applyCount,supportOrgLoan,start,end,status,department,startPrice,property,pass_in,itemurl,citynum,company,tel) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    data=(j['province'],j['city'],j['target'],j['currentPrice'],j['bidCount'],j['consultPrice'],j['applyCount'],j['supportOrgLoan'],j['start'],j['end'],j['status'],j['department'],j['startPrice'],j['property'],j['pass_in'],j['itemurl'],j['citynum'],j['company'],j['tel'])
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
  logging.warning('insert into db start')
  for i in info_list:
    insert_db(i)
  logging.warning('db function end')
"""
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
def main(cities):
  cities=cities
  t_s=time.strftime('%H:%M:%S',time.localtime(time.time()))
  #抓取数据
  getData(cities)
  #计算流拍率
  pass_func()
  #存储到mysql
  #db()
  #执行完数据库存储后再次把info_list置空
  global info_list
  info_list=[]
  t_e=time.strftime('%H:%M:%S',time.localtime(time.time()))
  logging.warning('start time:'+t_s)
  logging.warning('end time:'+t_e)

if __name__=='__main__':
  buding()
