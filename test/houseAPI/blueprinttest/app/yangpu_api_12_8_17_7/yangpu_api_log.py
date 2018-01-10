#! coding: utf-8
import logging

logging.basicConfig(level=logging.DEBUG,
  format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
  datefmt='%d %b %Y %H:%M:%S',
  filename='./yangpu_api_log.log',
  filemod='w')

def log_debug(message):
  logging.debug(message)

log_debug('test')
