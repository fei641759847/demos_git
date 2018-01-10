#!coding: utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask import Flask
from flask import request,jsonify,Blueprint
import json,codecs
from yangpu_api_log import log_debug
import requests
from urllib import urlopen,quote
from . import yangpu_api

#app=Flask(__name__)
#yangpu_api=Blueprint('yangpu_api',__name__)

#data={"name":"张","age":18}
def getData():
  with open('/root/backupofjd/root/blueprinttest/app/yangpu_api_12_8_17_7/yangpugongshang.txt','r') as f:
    f_dict=json.load(f)
  log_debug(str(type(f_dict)))
  return f_dict

def shidi():
#是否实地经营数据处理
  shidi_no=0
  shidi_yes=0
  shidi_no_dict={}
  shidi_yes_dict={}
  shidi_list=[]
  data=getData()
  for i in data:
    if '实地经营' in i.keys():
      if i[u'实地经营']=='非' or i[u'实地经营']=='否':
        shidi_no+=1
      else:
        shidi_yes+=1
  shidi_no_dict={"type":"0","x":u"非","y":str(shidi_no)}
  shidi_yes_dict={"type":"1","x":u"是","y":str(shidi_yes)}
  shidi_list=[shidi_no_dict,shidi_yes_dict]
  log_debug(str(shidi_no)+'--'+str(shidi_yes))
  log_debug(str(len(data)))
  return shidi_list

def nianbao():
  #年报情况数据处理
  data=getData()
  nianbao_data={}
  nianbao_list=[]
  for i in data:
    if '年报' in i.keys():
      if i[u'年报'] in nianbao_data:
        nianbao_data[i[u'年报']]+=1
      else:
        nianbao_data[i[u'年报']]=1
  type_num=1
  for j in nianbao_data:
    #print j,nianbao_data[j]
    d={"type":str(type_num),"x":j,"y":str(nianbao_data[j])}
    nianbao_list.append(d)
    type_num+=1
  return nianbao_list

def shudishichang():
  #属地市场监管所数据处理
  data=getData()
  shudishichang_data={}
  shudishichang_list=[]
  for i in data:
    if '属地市场监管所' in i.keys():
      if i[u'属地市场监管所'] in shudishichang_data:
        shudishichang_data[i[u'属地市场监管所']]+=1
      else:
        shudishichang_data[i[u'属地市场监管所']]=1
  for j in shudishichang_data:
    #print j,shudishichang_data[j]
    d={"title":j,"cnt":shudishichang_data[j],"type":1}
    shudishichang_list.append(d)
  return shudishichang_list

def getlnglat(address):
#根据地址查询坐标
  url = 'http://api.map.baidu.com/geocoder/v2/'
  output = 'json'
  ak = 'rCCNOsh0eFCnOpyH3jvVsrYhe90ooXrm'
  add = quote(address) #由于本文地址变量为中文，为防止乱码，先用quote进行编码
  uri = url + '?' + 'address=' + add  + '&output=' + output + '&ak=' + ak
  req = urlopen(uri)
  res = req.read().decode()
  temp = json.loads(res)
  lat=temp['result']['location']['lat']
  lng=temp['result']['location']['lng']
  return [lat,lng]

def map_data():
#地图数据处理
  data=getData()
  map_list=[]
  j=0
  for i in data:
    address=str(data[0][u'注册地址'])
    latlng=getlnglat(address)
    d={"img":"","video":"","lng":str(latlng[1]),"lat":str(latlng[0]),"s":1,"value":"1"}
    map_list.append(d)
    log_debug(j)
    j+=1
  f=open('./map_data.txt','w')
  f.write(str(map_list))
  f.flush()
  f.close()
  return map_list

@yangpu_api.route('/map',methods=['GET','POST'])
def map_api():
  #data=map_data()
  with open('/root/backupofjd/root/blueprinttest/app/yangpu_api_12_8_17_7/map_data.txt','r') as f:
    data=eval(f.read())
  return jsonify(data)

@yangpu_api.route('/shidi',methods=['GET','POST'])
def shidi_api():
  shidi_data=shidi()
  return jsonify(shidi_data)

@yangpu_api.route('/nianbao',methods=['GET','POST'])
def nianbao_api():
  nianbao_data=nianbao()
  return jsonify(nianbao_data)

@yangpu_api.route('/shudishichang',methods=['GET','POST'])
def shudishichang_api():
  shudishichang_data=shudishichang()
  return jsonify(shudishichang_data)

#if __name__=='__main__':
#  app.run(debug=True,host='0.0.0.0',port=5001)
