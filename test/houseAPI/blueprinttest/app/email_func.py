#coding:utf-8
from app import mail,app
from flask_mail import Message

#获取邮件配置
mail_server=app.config['MAIL_SERVER']

def sendEmail():
  pass
