#coding: utf-8
import threading
import random,time

def test(i):
  time.sleep(random.randint(1,5))
  print i

def addThread():
  thread_list=[]
  for i in range(0,10):
    thread_list.append(threading.Thread(target=test,args=(i,)))
  return thread_list

def main():
  thread_list=addThread()
  for j in thread_list:
    j.start()
  for j in thread_list:
    j.join()

if __name__=='__main__':
  main()
  print 'main'
