#coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import pymysql
import json

config={
  'host':'127.0.0.1',
  'port':3306,
  'user':'root',
  'password':'123.com',
  'db':'spider',
  'charset':'utf8'
}

def select_db():
  try:
    conn=pymysql.connect(**config)
    cur=conn.cursor()
    cur.execute('select * from house limit 2')
    result=cur.fetchall()
    for i in result:
      print type(i)
      print i
      for j in i:
        pass
  except:
    print 'error'

def insert_db(info):
  try:
    conn=pymysql.connect(**config)
    cur=conn.cursor()
    sql="insert into test values(%s,%s)"
    cur.execute(sql,info)
    cur.close()
    conn.commit()
    conn.close()
  except:
    pass

if __name__=='__main__':
  info=('1','hello')
  insert_db(info)
#select_db()
