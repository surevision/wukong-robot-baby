#!/bin/bash
# 设置环境变量
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
screen -S key /usr/bin/sudo /usr/bin/python /home/pi/pi-page/matrix_keypad.py
