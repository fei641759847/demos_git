#coding:utf-8
from app.blog import blog
from flask import render_template
from ..log_func import log_debug
#调用log_func.py模块中得log_debug函数
from app import app
#调用app，为了拿到config
from ..email_func import sendEmail


MONGODB_URI=app.config['MONGODB_URI']

@blog.route('/')
def blog_index():
  log_debug('reuse test')
  log_debug(MONGODB_URI)
  #测试邮件调用
  sendEmail()
  return render_template('/blog/index.html')

@blog.route('/login')
def blog_login():
  return 'blog login'
