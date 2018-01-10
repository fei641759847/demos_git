#coding: utf-8

from flask import Blueprint

house_api=Blueprint('house',__name__)

from house_api import *
