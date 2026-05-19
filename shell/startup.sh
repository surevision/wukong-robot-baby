#!/bin/bash
# 设置环境变量
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
#sudo rfkill unblock all
#sudo ifconfig wlan0 up
#sudo killall wpa_supplicant
#sudo wpa_supplicant -B -Dwext -c /etc/wpa_supplicant/wpa_supplicant.conf -i wlan0

#sudo dhcpcd wlan0

#screen -S key /home/pi/.pyenv/versions/3.9.6/bin/python /home/pi/pi-page/matrix_keypad.py
nohup /usr/bin/python /home/pi/pi-page/matrix_keypad.py >/home/pi/key.log 2>&1 &
