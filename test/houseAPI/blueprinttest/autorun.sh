#!/bin/bash
#this sh use for start house_api
nohup gunicorn -w 4 -b 0.0.0.0:8899 run:app &
