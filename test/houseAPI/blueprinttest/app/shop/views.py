#coding:utf-8
from app.shop import shop
from flask import render_template

@shop.route('/')
def shop_index():
  return render_template('/shop/index.html')
  return 'shop'
