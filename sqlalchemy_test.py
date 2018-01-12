# -*- coding:utf-8 -*-
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,String
from sqlalchemy.orm import sessionmaker

engine=create_engine('mysql+mysqldb://root:123.com@localhost/flask_allin')
Base=declarative_base()
class User(Base):
  __tablename__='users'
  id=Column(Integer,primary_key=True)
  name=Column(String(16))
  fullname=Column(String(16))
  password=Column(String(16))
  def __repr__(self):
    return "<User(name='%s',fullname='%s',password='%s')>" %(self.name,self.fullname,self.password)

class Address(Base):
  __tablename__='address'
  id=Column(Integer,primary_key=True)
  name=Column(String(16))
  fullname=Column(String(16))
  password=Column(String(16))
  def __repr__(self):
    return "<Address(name='%s',fullname='%s',password='%s')>" %(self.name,self.fullname,self.password)

#print User.__table__
Base.metadata.create_all(engine)
ed_user=User(name='ed',fullname='edname',password='edpassword')
ed_user1=User(name='ed1',fullname='edname1',password='edpassword1')
Session=sessionmaker(bind=engine)
session=Session()
#session.add(ed_user)
session.add_all([ed_user,ed_user1])
ed_user.password='123.com'
session.commit()
#把session关闭后session里面就没东西了
session.close()
ulist=session.query(User).filter_by(password="123.com")
for i in ulist:
  print i
if ed_user in session:
  print 'yes'
else:
  print 'no'
