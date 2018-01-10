#coding: utf-8
a=[1,2]

def dd():
  print 'd',a
def cc():
  dd()
  global a
  a=[]
  print 'c',a

cc()
print 'out',a
