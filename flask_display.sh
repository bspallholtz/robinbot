#!/bin/bash
netstat -ltnp | grep -w '5000' | awk '{print $NF}' | awk -F\/ '{print $1}' | xargs -I % kill -9 %
export FLASK_APP=/home/ec2-user/robinbot/flask_display.py
/usr/bin/python3 -m flask run --host=0.0.0.0
