#coding: utf-8
import threadpool,time

def test(i):
  print i+100
  time.sleep(3)

i=[1,2,3,4,5,6,7,8,9,0,11,12,13,14,15]
pool=threadpool.ThreadPool(5)
res=threadpool.makeRequests(test,i)
[pool.putRequest(r) for r in res]
#for r in res:
#  pool.putRequest(r)
pool.wait()
