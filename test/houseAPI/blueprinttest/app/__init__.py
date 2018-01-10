#coding:utf-8
from flask import Flask
import config
#from flask_mail import Mail

app=Flask(__name__)
app.config.from_object(config)
#mail=Mail(app)
