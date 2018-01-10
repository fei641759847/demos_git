#coding: utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import logging
from flask import Flask,Blueprint,render_template,send_from_directory,request
import json,time
import pymysql
#import MySQLdb
from . import house_api
import os
from app import app

#city_num={ u'贵阳':1,u'北京':2,u'上海':3,u'重庆':4,u'天津':5,u'南京':6,u'东莞':7,u'广州':8,u'珠海':9,u'惠州':10,u'中山':11,u'武汉':12,u'合肥':13,u'长沙':14,u'常州':15,u'南通':16,u'徐州':17}

logging.basicConfig(level=logging.DEBUG,
        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
        datefmt='%a,%d %b %Y %H:%M:%S',
        filename='./house.log',
        filemod='a')
'''
config={
  'host':'localhost',                                      
  'port':3306,                                             
  'user':'wx_spider',                                           
  'password':'Data_123',
  'db':'spider',
  'charset':'utf8',
}
'''
def select_db():
  house_dict={}
  house_list=[]
  try:
    #conn=pymysql.connect(**config)
    #conn=MySQLdb.connect('localhost','wx_spider','Data_123','spider',charset='utf8')
    conn=pymysql.connect('localhost','wx_spider','Data_123','spider',charset='utf8')
    cur=conn.cursor()
    #cur.execute('select * from house limit 2')
    cur.execute('select * from house_all')
    result=cur.fetchall()
    for i in result:
      #print type(i)
      #print i
      pass_yse=0
      pass_no=0
      department_dict={}
      house_dict={
        'id':i[0],
        'province':i[1],
        'city':i[2],
        'target':i[3],
        'currentPrice':i[4],
        'bidCount':i[5],
        'marketPrice':i[6],
        'applyCount':i[7],
        'viewerNum':i[8],
        'startTime':i[9],
        'stopTime':i[10],
        'status':i[11],
        'department':i[12],
        'addPrice':i[13],
        'deposit':i[14],
        'startPrice':i[15],
        'period':i[16],
        'property':i[17],
        'pass_in':i[18],
      }

      house_list.append(house_dict)

    logging.debug('data ok')
    return house_list
  except:
    logging.debug('data error')

@house_api.route('/all')
def house():
  data=select_db()
  return json.dumps(data)

city_num={u'\u5357\u5145': 58, u'\u6f33\u5dde': 101, u'\u6e05\u8fdc': 190, u'\u9ec4\u5357': 82, u'\u8386\u7530': 100, u'\u4f5b\u5c71': 189, u'\u6b66\u5a01': 244, u'\u5854\u57ce': 88, u'\u9e70\u6f6d': 147, u'\u4e09\u4e9a': 149, u'\u6069\u65bd': 120, u'\u9e64\u5c97': 175, u'\u9e21\u897f': 177, u'\u5b9c\u5bbe': 54, u'\u5b89\u9633': 15, u'\u901a\u8fbd': 296, u'\u547c\u548c\u6d69\u7279': 301, u'\u9ed1\u6cb3': 166, u'\u6986\u6797': 232, u'\u8302\u540d': 186, u'\u963f\u62c9\u5c14': 90, u'\u695a\u96c4': 205, u'\u53a6\u95e8': 107, u'\u5bbf\u5dde': 308, u'\u963f\u575d': 45, u'\u9ec4\u5188': 121, u'\u6587\u5c71': 203, u'\u6d77\u5317': 80, u'\u63ed\u9633': 195, u'\u4f0a\u6625': 174, u'\u4e09\u95e8\u5ce1': 22, u'\u510b\u5dde': 164, u'\u67f3\u5dde': 219, u'\u4e1c\u839e': 185, u'\u4e09\u660e': 106, u'\u5468\u53e3': 24, u'\u5b89\u5e86': 315, u'\u5fb7\u5b8f': 208, u'\u4e0a\u9976': 140, u'\u4e50\u4e1c': 156, u'\u7389\u6eaa': 209, u'\u4fdd\u4ead': 161, u'\u6b66\u6c49': 132, u'\u6c60\u5dde': 321, u'\u8944\u9633': 128, u'\u5f00\u5c01': 14, u'\u5185\u6c5f': 55, u'\u963f\u62c9\u5584': 305, u'\u4e34\u6c82': 41, u'\u6dee\u5357': 316, u'\u671d\u9633': 341, u'\u5927\u5e86': 171, u'\u9675\u6c34': 153, u'\u5b9a\u897f': 243, u'\u4e34\u6ca7': 210, u'\u5410\u9c81\u756a': 96, u'\u91d1\u660c': 249, u'\u5170\u5dde': 246, u'\u9075\u4e49': 5, u'\u6cf0\u5b89': 40, u'\u5357\u901a': 77, u'\u6dee\u5317': 317, u'\u51c9\u5c71': 50, u'\u961c\u65b0': 342, u'\u677e\u539f': 276, u'\u666f\u5fb7\u9547': 146, u'\u8d35\u9633': 4, u'\u8d35\u6e2f': 223, u'\u5e38\u5dde': 74, u'\u5415\u6881': 335, u'\u4e94\u6307\u5c71': 154, u'\u8346\u5dde': 127, u'\u626c\u5dde': 75, u'\u6d77\u53e3': 150, u'\u6797\u829d': 337, u'\u56db\u5e73': 272, u'\u6500\u679d\u82b1': 65, u'\u8d63\u5dde': 145, u'\u5a01\u6d77': 37, u'\u8346\u95e8': 131, u'\u6d77\u5357\u85cf\u65cf': 79, u'\u4e4c\u9c81\u6728\u9f50': 85, u'\u7389\u6797': 224, u'\u8861\u9633': 288, u'\u6842\u6797': 217, u'\u7ea2\u6cb3': 213, u'\u676d\u5dde': 116, u'\u4e34\u6c7e': 325, u'\u9752\u5c9b': 38, u'\u5305\u5934': 304, u'\u5e7f\u5143': 63, u'\u5e73\u9876\u5c71': 27, u'\u4ed9\u6843': 119, u'\u53f0\u5dde': 111, u'\u7518\u5b5c': 59, u'\u7518\u5357': 254, u'\u9f99\u5ca9': 99, u'\u5e86\u9633': 248, u'\u4fdd\u5c71': 201, u'\u4e2d\u5c71': 193, u'\u6f84\u8fc8': 151, u'\u65b0\u4f59': 137, u'\u7261\u4e39\u6c5f': 172, u'\u6e56\u5dde': 117, u'\u6e58\u6f6d': 283, u'\u6f2f\u6cb3': 26, u'\u4e50\u5c71': 46, u'\u6dee\u5b89': 66, u'\u4e4c\u6d77': 300, u'\u91cd\u5e86': 271, u'\u7126\u4f5c': 17, u'\u5341\u5830': 129, u'\u77f3\u5634\u5c71': 266, u'\u9999\u6e2f\u5c9b': 323, u'\u5bbf\u8fc1': 78, u'\u5408\u80a5': 320, u'\u5357\u5b81': 220, u'\u5b5d\u611f': 124, u'\u6210\u90fd': 53, u'\u6d77\u897f': 81, u'\u6587\u660c': 159, u'\u6e29\u5dde': 110, u'\u5ef6\u5b89': 233, u'\u664b\u57ce': 332, u'\u90b5\u9633': 290, u'\u9e64\u58c1': 18, u'\u535a\u5c14\u5854\u62c9': 87, u'\u627f\u5fb7': 258, u'\u65e5\u7167': 31, u'\u664b\u4e2d': 331, u'\u5c6f\u660c': 158, u'\u6000\u5316': 289, u'\u6f6e\u5dde': 183, u'\u70df\u53f0': 33, u'\u5e38\u5fb7': 293, u'\u8bb8\u660c': 12, u'\u660c\u5409': 92, u'\u798f\u5dde': 103, u'\u5e7f\u5b89': 62, u'\u6d4e\u5357': 44, u'\u629a\u987a': 350, u'\u5c71\u5357': 339, u'\u9547\u6c5f': 68, u'\u6f5c\u6c5f': 123, u'\u77f3\u5bb6\u5e84': 260, u'\u5f20\u5bb6\u754c': 285, u'\u5409\u5b89': 142, u'\u8087\u5e86': 184, u'\u4fe1\u9633': 19, u'\u592a\u539f': 327, u'\u8fbd\u6e90': 275, u'\u9f50\u9f50\u54c8\u5c14': 168, u'\u53cc\u9e2d\u5c71': 169, u'\u82cf\u5dde': 73, u'\u65b0\u4e61': 20, u'\u6c38\u5dde': 291, u'\u660c\u6c5f': 162, u'\u8862\u5dde': 115, u'\u6c55\u5934': 196, u'\u804a\u57ce': 32, u'\u5a04\u5e95': 292, u'\u9ed4\u897f\u5357': 8, u'\u6d1b\u9633': 10, u'\u9632\u57ce\u6e2f': 218, u'\u4e34\u9ad8': 152, u'\u54b8\u5b81': 125, u'\u76d8\u9526': 344, u'\u846b\u82a6\u5c9b': 346, u'\u94a6\u5dde': 229, u'\u5d07\u5de6': 226, u'\u6c5f\u95e8': 191, u'\u9152\u6cc9': 245, u'\u5357\u660c': 141, u'\u5b9a\u5b89': 165, u'\u8fbd\u9633': 352, u'\u8861\u6c34': 263, u'\u5ba3\u57ce': 310, u'\u9a6c\u978d\u5c71': 313, u'\u56fa\u539f': 267, u'\u90f4\u5dde': 281, u'\u4f0a\u7281': 97, u'\u9ed4\u5357': 2, u'\u672c\u6eaa': 345, u'\u9526\u5dde': 349, u'\u968f\u5dde': 122, u'\u5927\u5174\u5b89\u5cad': 173, u'\u5546\u4e18': 13, u'\u7ecd\u5174': 114, u'\u516d\u76d8\u6c34': 3, u'\u6d4e\u5b81': 30, u'\u514b\u5b5c\u52d2\u82cf\u67ef\u5c14\u514b\u5b5c': 94, u'\u6e58\u897f': 294, u'\u7ee5\u5316': 176, u'\u5434\u5fe0': 269, u'\u91d1\u534e': 118, u'\u65e0\u9521': 67, u'\u96c5\u5b89': 47, u'\u4eb3\u5dde': 318, u'\u4e34\u590f': 250, u'\u90a2\u53f0': 262, u'\u5eca\u574a': 264, u'\u6606\u660e': 214, u'\u6df1\u5733': 180, u'\u5b81\u6ce2': 109, u'\u90af\u90f8': 265, u'\u9ed4\u4e1c\u5357': 7, u'\u8fd0\u57ce': 329, u'\u9ec4\u77f3': 134, u'\u743c\u6d77': 148, u'\u901a\u5316': 278, u'\u4e0a\u6d77': 324, u'\u6f4d\u574a': 28, u'\u8d3a\u5dde': 227, u'\u666e\u6d31': 211, u'\u767d\u57ce': 279, u'\u8d44\u9633': 64, u'\u8fde\u4e91\u6e2f': 72, u'\u66f2\u9756': 200, u'\u957f\u6cbb': 328, u'\u5174\u5b89': 302, u'\u6e5b\u6c5f': 197, u'\u54c8\u5c14\u6ee8': 170, u'\u547c\u4f26\u8d1d\u5c14': 297, u'\u6e2d\u5357': 236, u'\u978d\u5c71': 348, u'\u957f\u6c99': 282, u'\u4e2d\u536b': 268, u'\u6cf8\u5dde': 57, u'\u9647\u5357': 241, u'\u83cf\u6cfd': 34, u'\u5fb7\u9633': 61, u'\u94dc\u4ec1': 6, u'\u5e7f\u5dde': 179, u'\u961c\u9633': 312, u'\u5cb3\u9633': 284, u'\u5927\u8fde': 343, u'\u4e39\u4e1c': 353, u'\u840d\u4e61': 138, u'\u516d\u5b89': 314, u'\u6885\u5dde': 188, u'\u5b89\u5eb7': 235, u'\u5609\u5cea\u5173': 252, u'\u6c88\u9633': 351, u'\u7ef5\u9633': 52, u'\u6d77\u4e1c': 83, u'\u963f\u52d2\u6cf0': 98, u'\u9042\u5b81': 48, u'\u6cc9\u5dde': 102, u'\u6cb3\u6e90': 187, u'\u8425\u53e3': 347, u'\u4fdd\u5b9a': 261, u'\u5b9c\u660c': 133, u'\u4e03\u53f0\u6cb3': 167, u'\u6ec1\u5dde': 319, u'\u6714\u5dde': 326, u'\u5f20\u5bb6\u53e3': 255, u'\u94dc\u9675': 309, u'\u6012\u6c5f': 207, u'\u5e73\u51c9': 251, u'\u76ca\u9633': 287, u'\u5317\u6d77': 225, u'\u5b9c\u6625': 144, u'\u5929\u6c34': 247, u'\u9633\u6cc9': 333, u'\u54b8\u9633': 239, u'\u81ea\u8d21': 49, u'\u4e91\u6d6e': 199, u'\u5b89\u987a': 1, u'\u4e3d\u6c5f': 206, u'\u5317\u4eac': 216, u'\u62c9\u8428': 336, u'\u963f\u91cc': 338, u'\u897f\u5b89': 238, u'\u5b9d\u9e21': 237, u'\u897f\u5b81': 84, u'\u4e3d\u6c34': 108, u'\u5580\u4ec0': 86, u'\u9a7b\u9a6c\u5e97': 11, u'\u94dc\u5ddd': 231, u'\u83b1\u829c': 43, u'\u6765\u5bbe': 228, u'\u5df4\u97f3\u90ed\u695e': 95, u'\u662d\u901a': 215, u'\u8fbe\u5dde': 51, u'\u4e94\u5bb6\u6e20': 89, u'\u6fee\u9633': 16, u'\u829c\u6e56': 307, u'\u6c55\u5c3e': 181, u'\u9633\u6c5f': 182, u'\u4e5d\u6c5f': 139, u'\u629a\u5dde': 143, u'\u94c1\u5cad': 340, u'\u67a3\u5e84': 42, u'\u5927\u7406': 204, u'\u5fb7\u5dde': 39, u'\u5927\u540c': 334, u'\u94f6\u5ddd': 270, u'\u6bd5\u8282': 9, u'\u682a\u6d32': 286, u'\u73e0\u6d77': 194, u'\u4e07\u5b81': 160, u'\u897f\u53cc\u7248\u7eb3': 202, u'\u5ffb\u5dde': 330, u'\u4e4c\u5170\u5bdf\u5e03': 298, u'\u4e1c\u65b9': 157, u'\u5df4\u4e2d': 56, u'\u5f20\u6396': 253, u'\u6d4e\u6e90': 23, u'\u4f73\u6728\u65af': 178, u'\u6cf0\u5dde': 69, u'\u97f6\u5173': 192, u'\u6dc4\u535a': 36, u'\u5929\u6d25': 136, u'\u795e\u519c\u67b6': 130, u'\u9102\u5c14\u591a\u65af': 299, u'\u5357\u5e73': 104, u'\u6cb3\u6c60': 230, u'\u9ec4\u5c71': 322, u'\u5510\u5c71': 256, u'\u767d\u5c71': 274, u'\u868c\u57e0': 311, u'\u5546\u6d1b': 234, u'\u5409\u6797': 277, u'\u9102\u5dde': 135, u'\u6ee8\u5dde': 29, u'\u5f90\u5dde': 71, u'\u963f\u514b\u82cf': 91, u'\u4e1c\u8425': 35, u'\u5357\u9633': 21, u'\u68a7\u5dde': 221, u'\u5df4\u5f66\u6dd6\u5c14': 303, u'\u60e0\u5dde': 198, u'\u767e\u8272': 222, u'\u957f\u6625': 280, u'\u743c\u4e2d': 163, u'\u5ef6\u8fb9\u671d\u9c9c\u65cf': 273, u'\u7709\u5c71': 60, u'\u767d\u6c99': 155, u'\u5609\u5174': 112, u'\u514b\u62c9\u739b\u4f9d': 93, u'\u6c49\u4e2d': 240, u'\u8fea\u5e86': 212, u'\u76d0\u57ce': 76, u'\u767d\u94f6': 242, u'\u9521\u6797\u90ed\u52d2': 295, u'\u79e6\u7687\u5c9b': 257, u'\u5929\u95e8': 126, u'\u8d64\u5cf0': 306, u'\u6ca7\u5dde': 259, u'\u5357\u4eac': 70, u'\u821f\u5c71': 113, u'\u90d1\u5dde': 25, u'\u5b81\u5fb7': 105}

@house_api.route('/spider')
def blog_login():
  return render_template('/house/select.html',city_num=city_num)

@house_api.route('/select',methods=['GET','POST'])
def select_db():
  cmd_status=''
  if request.method=='POST':
    city=request.form['city1']
    loan=request.form['loan']
    start=request.form['start'].replace('/','-')
    end=request.form['end'].replace('/','-')
    status=request.form['do']
    #时间限制
    if start=='':
      start='2017-9-1'
    if end=='':
      end='2017-11-30'
    #城市编号
    citynum=0
    for i in city_num:
      if city==i:
        citynum=city_num[city]
    if citynum==0:
      return render_template('/house/select.html',city_num=city_num)
    #状态
    if status=='1':
      cmd_status="and status!='todo' and status!='doing'"
    else:
      cmd_status=''
    #可贷款
    if loan=='1':
      cmd_loan="and supportOrgLoan=1"
    else:
      cmd_loan=''
    print citynum,loan,start,end,status
    cmd='''mysql -uroot -p'123.com' -e "select * from spider.house_v3 where citynum=%s and start>'%s' and end<'%s' %s %s into outfile '/tmp/house.xls'"'''%(citynum,start,end,cmd_status,cmd_loan)
    print cmd
    os.popen(cmd)
    time.sleep(5)
    os.popen('rm -rf /root/test/houseAPI/blueprinttest/app/xlsfile/house.xls')
    os.popen('mv /tmp/house.xls /root/test/houseAPI/blueprinttest/app/xlsfile/')
  return render_template('/house/down.html')

@house_api.route('/down')
def down_xls():
  dirpath=os.path.join(app.root_path,'xlsfile')
  return send_from_directory(dirpath,'house.xls',as_attachment=True)
