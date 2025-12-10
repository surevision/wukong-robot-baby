#!/bin/bash
# 设置环境变量
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
screen -S key /home/admin/.pyenv/versions/3.9.6/bin/python /home/admin/pi-page/matrix_keypad.py
