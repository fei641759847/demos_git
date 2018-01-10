# /usr/bin/env python
#-*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
import json
import xlwt
from fake_useragent import UserAgent
import time
import random
import threading
import pymysql
import logging

logging.basicConfig(level=logging.DEBUG,
        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
        datefmt='%a,%d %b %Y %H:%M:%S',
        filename='./house.log',)

config={
  'host':'127.0.0.1',
  'port':3306,
  'user':'root',
  'password':'123.com',
  'db':'spider',
  'charset':'utf8'
}
def delete_db():
  conn=pymysql.connect(**config)
  cur=conn.cursor()
  cur.execute('delete from house_all_new')
  cur.close()
  conn.commit()
  conn.close()

def insert_db(j):
  try:
    conn=pymysql.connect(**config)
    cur=conn.cursor()
    sql="insert into house_all_new (province,city,target,currentPrice,bidCount,marketPrice,applyCount,viewerNum,startTime,stopTime,status,department,addPrice,deposit,startPrice,period,property,pass_in,company,tel) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    data=(j['province'],j['city'],j['target'],j['currentPrice'],j['bidCount'],j['marketPrice'],j['applyCount'],j['viewerNum'],j['startTime'],j['stopTime'],j['status'],j['department'],j['addPrice'],j['deposit'],j['startPrice'],j['period'],j['property'],j['pass_in'],j['company'],j['tel'])
    #print(data)
    cur.execute(sql,data)
    cur.close()
    conn.commit()
    conn.close()
  except:
    logging.debug('db error')

infos = []
workbook = xlwt.Workbook()

def message_from_url(url, city, province):
    """
    爬取数据
    """
    time.sleep(random.randint(0, 3))
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    response = requests.get(url, timeout=60, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    script = soup.select_one('script#sf-item-list-data')
    items = json.loads(re.sub(r'\s*', '', script.text))['data']
    sub_infos = []
    #尝试添加是否可贷款字段
    #a=soup.select_one('div.pm-bid-right > div.org-loan-service > a')
    #try:
    #  print(a.text)
    #except:
    #  print('no')
    #print(" come from %s" % threading.currentThread().getName())
    for item in items:
        info = {}
        info['province'] = province
        info['city'] = city
        info['target'] = item['title']

        info['currentPrice'] = str(item['currentPrice'])
        info['currentPrice'] = info['currentPrice'].split('.')[0]
        info['currentPrice'] = info['currentPrice'].strip()
        info['currentPrice'] = info['currentPrice'].replace(',', '')
        info['currentPrice'] = info['currentPrice'].split('.')[0]

        info['bidCount'] = int(item['bidCount'])
        info['marketPrice'] = item['consultPrice']
        if info['marketPrice'] == 0.0:
            info['marketPrice'] = str(item['marketPrice'])
            info['marketPrice'] = info['marketPrice'].strip()
            info['marketPrice'] = info['marketPrice'].replace(',', '')
            info['marketPrice'] = info['marketPrice'].split('.')[0]

        info['applyCount'] = int(item['applyCount'])
        info['viewerNum'] = int(item['viewerCount'])
        info['startTime'] = int(item['start'] / 1000)
        info['stopTime'] = int(item['end'] / 1000)
        if item['status'] == 'doing':
            info['status'] = '正在进行'
        elif item['status'] == 'done' or item['status'] == 'failure':
            info['status'] = '已经结束'
        elif item['status'] == 'break':
            info['status'] = '中止'
        elif item['status'] == 'revocation':
            info['status'] = '撤回'
        else:
            info['status'] = '即将开始'
        item_url = 'http:%s' % item['itemUrl']
        time.sleep(random.random())
        ua = UserAgent()
        headers = {'User-Agent': ua.random}
        response = requests.get(item_url, timeout=60, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        s_department = soup.select_one('div.pai-info > p:nth-of-type(2) > a')
        # print('s_department', s_department)
        if s_department is None:
            i = soup.select_one('div.pai-info > p:nth-of-type(2)').text
            i = re.sub(r'\s*', '', i)
            info['department'] = i.split("：")[1]
        else:
            info['department'] = soup.select('div.pai-info > p:nth-of-type(2) > a')[0].text
        #print(info['department'])
        # J_HoverShow > tr:nth-child(1) > td:nth-child(1) > span.pay-price > span
        # print(soup.select('span.J_Price')[1].text)
        #info['startPrice'] = soup.select('span.J_Price')[1].text
        info['startPrice'] = soup.select('span.pay-price > span.J_Price')[0].text
        info['startPrice'] = info['startPrice'].strip()
        info['startPrice'] = info['startPrice'].replace(',', '')
        info['startPrice'] = info['startPrice'].split('.')[0]
        # print(info['startPrice'])

        # span_list1 = soup.select('td nth-of-type(2) > p > span')
        # span_list = soup.select('table > tbody > tr:nth-of-type(5) > td:nth-of-type(2) > p > span')
        # J_desc > table > tbody > tr:nth-child(6) > td:nth-child(2) > p > span
        # J_desc > table > tbody > tr:nth-child(8) > td:nth-child(2) > p > span


        info['addPrice'] = soup.select('span.J_Price')[2].text
        info['addPrice'] = info['addPrice'].strip()
        info['addPrice'] = info['addPrice'].replace(',', '')

        info['deposit'] = soup.select('#J_HoverShow > tr:nth-of-type(2) > td:nth-of-type(1) > span.pai-save-price > span')[
                0].text
        info['deposit'] = str(info['deposit'])
        info['deposit'] = info['deposit'].strip()
        info['deposit'] = info['deposit'].replace(',', '')
        info['deposit'] = info['deposit'].split('.')[0]

        info['period'] = soup.select('#J_HoverShow > tr:nth-of-type(2) > td:nth-of-type(2) > span:nth-of-type(2)')[
            0].get_text()
        info['period'] = info['period'][1:]
        info['property']=''
        info['pass_in']=''
        #增加辅助机构
        try:
          url_notice = soup.select('#J_NoticeDetail')[0].attrs['data-from']
          url_notice = 'http:' + url_notice
          ua = UserAgent()
          headers = {'User-Agent': ua.random}
          response_notice = requests.get(url_notice, timeout=60, headers=headers)
          res_comp=re.findall('拍卖辅助机构：(.*)公司',response_notice.text)
          res_tel=re.findall('辅助机构咨询电话：<span>(\d\d\d\d\d\d\d*)\D+',response_notice.text)
          if len(res_comp)==1:
            info['company']=res_comp[0]+'公司'
            print(res_comp[0])
          else:
            info['company']='-'
            #print('nothing',end='')
          if len(res_tel)>=1:
            info['tel']=res_tel[0]
            print(res_tel)
          else:
            res_tel=re.findall('辅助机构咨询电话：</span></strong><span style=\"font-size: 19.0px;\">(\d\d\d\d\d\d\d*)\D+',response_notice.text)
            if len(res_tel)>=1:
              info['tel']=res_tel[0]
            else:
              info['tel']='-'
        except:
          info['company']='-'
          info['tel']='-'
        #print response_notice.text
        #用途
        url_detail = soup.select('#J_desc')[0].attrs['data-from']
        url_detail = 'http:' + url_detail
        ua = UserAgent()
        headers = {'User-Agent': ua.random}
        response = requests.get(url_detail, timeout=60, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        #print('detail_response', response)
        detail = ['城镇住宅用地','商业服务','住宅用地','、商服用地；','1、住宅。','办公','工业','仓储','非居住', '商业', '非住宅', '住宅', '工业用地', '工业用途房地产', '、其他商服用地', '其他商服用地', '办公写字楼', '商住综合用地','综合','商用；']
        for d in detail:
            p = soup.find(text=d)
            #aaa=re.compile(r'{%s}'%d)
            #p = aaa.findall(response.text)
            if p is not None:
                #print(d)
                info['property'] = d

        # properties = [p.text for p in span_list2]
        # print('properties', properties)
        # info['property'] = ''
        # for p in properties:
        #     if '土地性质' in p:
        #         p_list = soup.select('td:nth-of-type(3) > p > span')
        #         print('p_list', p_list)
        #         info['property'] = [''.join(p) for p.text in p_list]
        #         print("info['property']", info['property'])

        sub_infos.append(info)
        logging.debug('抓取到 %s' % item['title'])
    infos.extend(sub_infos)
    # print('infos', infos)


def save_sheet_in_excel():
    """
    保存数据到excel
    """
    sheet = workbook.add_sheet('sheet')
    names = ['省份', '城市', '标的物', '当前价', '出价数', '评估价', '报名人数', '围观人数', '开拍时间',
             '预计结束时间', '状态', '处置单位', '起拍价', '加价幅度', '保证金', '竞价周期', '性质']
    for index, name in enumerate(names):
        sheet.write(0, index, name)

    for index, info in enumerate(infos):
        row = index + 1
        for key, value in info.items():
            index = names.index(key)
            sheet.write(row, index, value)
    # 设置冻结
    sheet.panes_frozen = True
    sheet.horz_split_pos = 1


def create_thread(pages, base_url, city, province):
    """
    创建多线程
    """
    thread_list = []
    for index, page in enumerate(range(pages)):
        thread_name = "thread_%s" % index
        url = base_url + '&page=' + str(index)
        thread_list.append(threading.Thread(target=message_from_url, name=thread_name, args=(url, city, province)))
    return thread_list


def city_of_url(url, search_citys):
    """
    获得城市的url
    """
    url = 'http://%s' % url
    # print('url', url)
    #print('search_citys', search_citys)
    # 构造请求数据
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    response = requests.get(url, timeout=60, headers=headers)
    # print(response.text)
    soup = BeautifulSoup(response.text, 'html.parser')
    tags = soup.select('ul > li.triggle.unfold > div > ul > li > em > a')
    # print(tags)
    sub_urls = []
    citys = []
    for tag in tags:
        u = tag['href']
        city = tag.text
        # print('city', city)
        citys.append(city)
        url = u.split('//')[1]
        # print('url', url)
        sub_urls.append(url)
    search_urls = []
    # 选择符合要求的城市
    for index, city in enumerate(citys):
        if city in search_citys:
            search_urls.append(sub_urls[index])
    #print(search_urls)
    return search_urls



def province_of_url(url):
    """
    获得省份的url
    """
    response = requests.get(url)
    # print(response.text)
    soup = BeautifulSoup(response.text, 'html.parser')
    tags = soup.select('ul > li > em > a')
    # print(tags)
    urls = []
    provinces = []
    #search_provinces = {'湖南':['岳阳']}
    search_provinces = dict(
        安徽=['合肥'],
       # 甘肃=['兰州'],
       # 湖南=['岳阳','株洲','湘潭','衡阳','郴州'],
       # 湖南=['长沙'],
       # 广东=['深圳'],
       # 福建=['泉州','龙岩','宁德','三明','漳州','南平'],
       # 甘肃=['兰州'],
       # 广西=['南宁'],
       # 贵州=['贵阳'],
       # 海南=['海口', '三亚'],
       # 河北=['石家庄'],
       # 黑龙江=['哈尔滨'],
       # 吉林=['长春'],
       # 江苏=['徐州', '无锡', '常州', '南京', '南通'],
       # 江苏=['南京','南通','徐州','常州'],
       # 江苏=['南京'],
       # 江西=['南昌'],
       # 辽宁=['大连', '沈阳'],
       # 山东=['济南', '青岛','烟台'],
       # 山西=['太原'],
       # 陕西=['西安'],
       # 新疆=['乌鲁木齐'],
       # 云南=['昆明'],
       # 浙江=['温州', '宁波', '绍兴', '嘉兴', '金华', '台州'],
       # 北京=['北京'],
       # 上海=['上海'],
       # 重庆=['重庆'],
       # 天津=['天津'],
       # 广东=['中山', '广州', '深圳', '东莞', '惠州', '珠海']
    )
    tags = tags[11:43]
    web_province = ['浙江', '江苏', '河南', '福建', '上海', '广东', '安徽', '内蒙古', '北京', '湖北', '云南', '山东', '海南', '江西', '广西', '天津',
                    '重庆', '湖南', '河北', '四川', '山西', '贵州', '宁夏', '青海', '辽宁', '吉林', '黑龙江', '西藏', '陕西', '甘肃', '新疆', '香港']
    #print('tags', tags)
    for tag in tags:
        u = tag['href']
        province = tag.text
        #print('provice', province)
        provinces.append(province)
        url = u.split('//')[1]
        #print('url', url)
        urls.append(url)
    #print('打印所有urls', urls)
    p_urls = {}
    sp = list(search_provinces.keys())
    #print('sp', sp)
    #print('浙江' in sp)
    for index, province in enumerate(web_province):
        #print('province', province)
        if province in sp:
            #print('选择出url')
            p_urls[province] = urls[index]
    logging.debug('目标爬取省份字典%s' % p_urls)
    return p_urls, search_provinces

def spider_house():
    """
    多线程爬取数据
    """
    #&sorder=2是已结束的条件
    #&sorder=4是中止的条件
    #&sorder=5是撤回的条件
    #&support_loans=1是可贷款的条件
    #base_url = 'https://sf.taobao.com/item_list.htm?spm=a213w.7398504.filter.2.GytMAm&category=50025969&auction_start_seg=0&auction_start_from=2017-10-01&auction_start_to=null'
    base_url = 'https://sf.taobao.com/item_list.htm?spm=a213w.7398504.filter.2.GytMAm&category=50025969&sorder=5&auction_start_seg=0&auction_start_from=2017-9-1&auction_start_to=2017-11-30'
    provinces_urls, provinces = province_of_url(base_url)
    for province, p_url in provinces_urls.items():
        citys = provinces[province]
        #print(citys)
        urls = city_of_url(p_url, citys)
        # 历遍城市url
        for index, url in enumerate(urls):
            url = 'http://%s' % url
            ua = UserAgent()
            headers = {'User-Agent': ua.random}
            response = requests.get(url, timeout=60, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            logging.debug('爬取 %s 市' % citys[index])
            #try:
            #  total_page = int(soup.select_one('em.page-total').text)
            #except:
            #  total_page = 1
            total_page = int(soup.select_one('em.page-total').text)
            logging.debug('一共 %s 页数据' % total_page)
            # 创建线程
            thread_list = create_thread(total_page, url, citys[index], province)
            # 启动所有线程
            for thread in thread_list:
                thread.start()
            # 主线程中等待所有子线程退出
            for thread in thread_list:
                thread.join()
    # 保存到数据库里面
    #save_data_in_database()
    #print(len(infos))

def test():
    """
    用于测试
    """
    city = '乌鲁木齐'
    province = '新疆'
    url = 'https://sf.taobao.com/item_list.htm?spm=a213w.7398504.filter.47.XY422R&category=50025969&city=%CE%DA%C2%B3%C4%BE%C6%EB&province=&auction_start_seg=-1'
    message_from_url(url, city, province)
    print(infos)
    #save_data_in_database()


def test_perproty():
    city = '江苏'
    province = '南通'
    url = 'https://sf.taobao.com/item_list.htm?spm=a213w.7398504.filter.73.VPZiGh&category=50025969&city=%C4%CF%CD%A8&sorder=0&auction_start_seg=-1'
    message_from_url(url, city, province)
    print(infos)
    #save_data_in_database()

def pass_func():
#统计流拍及成功次数，department_list的值前面是流拍次数，后面是成功次数
    department_dict={}
    for i in infos:
      if i['department'] not in department_dict:
        department_dict[i['department']]=[0,0]
        #print 'new department'
      else:
        if i['status']==u'已经结束' and i['bidCount']==0:
          #流拍加1
          #print 'liupai+1'
          department_dict[i['department']][0]+=1
        elif i['status']==u'已经结束' and i['bidCount']!=0:
          #成功加1
          #print 'chenggong+1'
          department_dict[i['department']][1]+=1
#把流拍率加入到总数据中去
    for j in infos:
      pass_no=department_dict[j['department']][0]
      pass_yes=department_dict[j['department']][1]
      if pass_no+pass_yes==0:
        pass_per=0
      else:
        pass_per=pass_no/float(pass_no+pass_yes)
      #j['pass_in']=str(round(pass_per,3)*100)+'%'
      j['pass_in']='%.1f'%(pass_per*100)+'%'
#改时间戳
    for i in infos:
      t=i['startTime']
      t1=i['stopTime']
      time_local=time.localtime(t)
      t_a=time.strftime("%Y-%m-%d %H:%M:%S",time_local)
      time_local1=time.localtime(t1)
      t1_a=time.strftime("%Y-%m-%d %H:%M:%S",time_local1)
      i['startTime']=t_a
      i['stopTime']=t1_a

if __name__ == '__main__':
    spider_house()
    pass_func()
    #保存之前是否删除原数据
    #delete_db()
    #保存到数据库
    for info in infos:
        insert_db(info)

    # test()
    #test_perproty()
    # db.drop_all()

