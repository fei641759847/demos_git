#coding:utf-8
from app import app
#from app.blog import blog
#from app.shop import shop
#from app.yangpu_api_12_8_17_7 import yangpu_api
from app.house import house_api

#app.register_blueprint(blog,url_prefix='/blog')
#app.register_blueprint(shop,url_prefix='/shop')
#app.register_blueprint(yangpu_api,url_prefix='/yangpu_api')
app.register_blueprint(house_api,url_prefix='/house_api')

if __name__=='__main__':
  #app.run(host='0.0.0.0',port=8899)
  app.run()
