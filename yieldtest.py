#coding: utf-8
def odd():
  n=1
  while True:
    yield n
    n+=2
oddnum=odd()
count=0
for o in oddnum:
  if count>=5: break
  print o
  count +=1
