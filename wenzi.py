#coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import urllib, urllib2, base64
import os,json
from PIL import Image

def imgToWords():
    access_token = '24.fe833a4ba91803b6dccfb3b405862a89.2592000.1518245381.282335-10674045'
    url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general?access_token=' + access_token
    f=open('xg.jpg','rb')
    img = base64.b64encode(f.read())
    params = {"image": img}
    params = urllib.urlencode(params)
    request = urllib2.Request(url, params)
    request.add_header('Content-Type', 'application/x-www-form-urlencoded')
    response = urllib2.urlopen(request)
    content = response.read()
    if (content):
        #print(content.decode('utf-8').encode('gbk'))
        return content

def getImg():
    os.system('adb shell screencap /sdcard/test.png')
    os.system('adb pull /sdcard/test.png .')

def getKeyWords():
    data=imgToWords()
    d=json.loads(data)
    return d['words_result'][3]['words']+d['words_result'][4]['words']
    #return d['words_result'][4]['words'],d['words_result'][3]['words']
    
def searchInWeb(data):
    os.system('"C:/Program Files/Internet Explorer/iexplore.exe" http://www.baidu.com/s?wd='+data)
    
if __name__=='__main__':
    getImg()
    im=Image.open('xg.jpg')
    im.show()
    #data1,data2=getKeyWords()
    data=getKeyWords()
    d=data.decode('utf-8').encode('gbk')
    #d1=data1.decode('utf-8').encode('gbk')
    #d2=data2.decode('utf-8').encode('gbk')
    #print d1,d2
    #searchInWeb(d1)
    searchInWeb(d)
    #searchInWeb(d2)
    