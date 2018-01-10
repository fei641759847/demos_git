#coding: utf-8
#writen by zhanghongfei
#use for get movies from 电影天堂
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import requests,lxml,time
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import pymongo,threading,random,MySQLdb
from requests.adapters import HTTPAdapter
from multiprocessing import Pool
import threadpool
import re

#创建随机请求头部
def createHeader():
  ua=UserAgent()
  header={'User-Agent':ua.random}
  return header

#设置请求重试次数
def createRequest():
  s=requests.Session()
  s.mount('http://',HTTPAdapter(max_retries=5))
  s.mount('https://',HTTPAdapter(max_retries=5))
  return s

#打开一个页面
def getPage(url):
  header=createHeader()
  s=createRequest()
  res=s.get(url,timeout=5,headers=header)
  res.encoding='gb2312'
  soup=BeautifulSoup(res.text,'lxml')
  return soup

#获取分类的链接
def getType():
  type_dict={}
  url='http://www.ygdy8.net/html/gndy/dyzz/index.html'
  soup_type=getPage(url)
  data_type=soup_type.select('table > tr > td > a')
  for i in data_type:
    type_dict[i.text]='http://www.ygdy8.net'+i.get('href')
  return type_dict

#获取每个分类的每一页的链接
#url参数是某一个分类的链接
def getEveryPageUrl(url):
  #url='http://www.ygdy8.net/html/gndy/rihan/index.html'
  url_list=[]
  soup_page=getPage(url)
  data_page=soup_page.select_one('div.x > td').text
  #print data_page[:15]
  total=re.findall(u'共(\d*)页',data_page)[0]
  print 'total',total
  data_url=soup_page.select_one('div.x > td > a').get('href')
  print data_url
  url_list.append(url)
  for i in range(2,int(total)+1):
    url_list.append(url[:-10]+data_url[:-6]+str(i)+'.html')
  print len(url_list)
  print url_list[28]
  return url_list

#单个线程获取单页中的所有数据
#这里的url是某一个分类下某一页的链接
def getMovies(url):
  #url='http://www.ygdy8.net/html/gndy/rihan/list_6_2.html'
  soup_out=getPage(url)
  data_out=soup_out.select('td > b > a')
  data_time=soup_out.select('tr > td > font')
  for i in range(0,len(data_out)+1):
    if i%2:
      try:
        info={}
        info['type']=url.split('/')[-2]
        info['weburl']='http://www.ygdy8.net'+data_out[i].get('href')
        #print info['type']
        #print info['weburl']
        info['updatetime']=re.findall(u'\u65e5\u671f\uff1a(.*) \r\n',data_time[(i-1)/2].text)[0]
        #print type(info['updatetime'])
        #print info['updatetime']
        soup_in=getPage(info['weburl'])
        data_title=soup_in.select('div.title_all > h1 > font')[0].text
        #print data_title
        info['title']=data_title
        data_desc=soup_in.select('div#Zoom > td')
        #print data_desc[0]
        info['desc']=str(data_desc[0])
        #print (info['desc'])
        #存储
        print 'mariadb start'
        mariadb_insert(info)
        info={}
      except:
        print 'get movie error'

#创建线程池并运行
def createThreadPool(args):
  pool=threadpool.ThreadPool(5)
  request=threadpool.makeRequests(getMovies,args)
  [pool.putRequest(res) for res in request]
  pool.wait()

#存储到mongodb
def db_insert(info):
  url='mongodb://localhost:27017'
  client=pymongo.MongoClient(url)
  db=client.spider
  collection=db.movie
  collection.insert(info)

#存储到mariadb
def mariadb_insert(info):
  config={"host":"127.0.0.1",
          "port":3306,
          "user":"root",
          "passwd":"123.com",
          "db":"spider",
          "charset":"utf8"
         }
  conn=MySQLdb.connect(**config)
  cur=conn.cursor()
  sql="insert into movie1 (title,updatetime,type,des) values (%s,%s,%s,%s)"
  data=(info['title'],info['updatetime'],info['type'],info['desc'])
  cur.execute(sql,data)
  cur.close()
  conn.commit()
  conn.close()

#进程池
def multi_func():
  pool=Pool(3)
  d=getType()
  for i in d:
    pool.apply_async(func=thread_func,args=(d[i],),callback=None)
  pool.close()
  pool.join()

#单个进程执行的任务
def thread_func(url):
  args=getEveryPageUrl(url)
  createThreadPool(args)

if __name__=='__main__':
  multi_func()
  #d=getType()
  #for i in d:
  #  print i,d[i]
  #getEveryPageUrl('url')
  #getMovies('url')
