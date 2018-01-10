#coding: utf-8
import pymysql
config={"host":"127.0.0.1",
        "port":3306,
        "user":"root",
        "password":"123.com",
        "db":"spider",
        "charset":"utf8",
}

conn=pymysql.connect(**config)
cur=conn.cursor()

cur.execute('select city,count(*) from house_v4 group by city')
res_v4=cur.fetchall()
city_v4={}
for i in res_v4:
  city_v4[i[0]]=i[1]

cur.execute('select city,count(*) from house_v7 group by city')
res_v7=cur.fetchall()
city_v7={}
for j in res_v7:
  city_v7[j[0]]=j[1]

cur.close()
conn.close()
print len(city_v4)
print len(city_v7)
for k in city_v4:
  if k not in city_v7.keys():
    print k
#print res_v4
