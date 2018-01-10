#coding: utf-8

class Student(object):
  '''
  hello
  '''
  def __init__(self,name,age):
    self.name=name
    self.age=age
    self.__address='shanghai'
  pass

class Stu(Student):
  def foo(self):
    print 'Stu'

wi=Stu('wi',28)
wi.foo()
print dir(wi)
print wi.__doc__
