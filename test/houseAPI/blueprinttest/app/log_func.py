#coding:utf-8
import logging
import config
from app import app

LOG_PATH=app.config['LOG_PATH']

logging.basicConfig(level=logging.DEBUG,
        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
        datefmt='%a,%d %b %Y %H:%M:%S',
        filename=LOG_PATH,
        filemod='a')

def log_debug(message):
  logging.debug(message)
