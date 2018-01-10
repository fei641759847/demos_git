#coding:utf-8
import pymongo

def connectdb(uri,dbname):
  try:
    client=pymongo.MongoClient(uri)
    db=client[dbname]
    return db
  except:
    #log:db connect error

def getCollection(db,tablename):
  collection=db[tablename]
  #log.info:collection connected
  return collection

def getContent(collection,condition,one=True,displayfilter=None):
  if displayfilter != None:
    pass
  if one:
    result=collection.find_one(condition)
  else:
    result=collection.find(condition)
  return result 

