#coding: utf-8
import base64
import urllib
import requests

def imgToBase64():
  with open('/root/test/shuoming0300.png','rb') as f:
    ls_f=base64.b64encode(f.read())
  print ls_f

def imgFromWeb():
  img_url=urllib.urlopen('http://f.hiphotos.baidu.com/image/h%3D300/sign=4937f93072cb0a469a228d395b61f63e/7dd98d1001e9390164fb96f472ec54e737d1967a.jpg')
  img_f=img_url.read()
  ls_f=base64.b64encode(img_f)
  with open('./1.jpg','wb') as f:
    f.write(img_f)
  print 'ok'
  #print ls_f

def imgFromWeb2():
  res=requests.get('http://f.hiphotos.baidu.com/image/h%3D300/sign=4937f93072cb0a469a228d395b61f63e/7dd98d1001e9390164fb96f472ec54e737d1967a.jpg')
  with open('./2.jpg','wb') as f:
    f.write(res.content)

imgFromWeb2()
#imgFromWeb()
#imgToBase64()
