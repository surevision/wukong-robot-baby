
# -*- coding: utf-8 -*
import RPi.GPIO as GPIO
import serial
import time
 
GPIO.setmode(GPIO.BOARD)
GPIO.setup(37, GPIO.IN)    # 定义25引脚为输入模式
 
# 打开串口
# ser = serial.Serial("/dev/ttyAMA0", 115200)
ser = serial.Serial("/dev/ttyS0", 115200)
def main():
    while True:
        # 获得接收缓冲区字符
        count = ser.inWaiting()
        if count != 0:
            # 读取内容并回显
            recv = ser.read(count)
            ser.write(recv)
            print(recv)
        # 清空接收缓冲区
        ser.flushInput()
        if GPIO.input(37):    # 用GPIO.input(引脚)函数来获取引脚电平状态
                              # 如果有信号输入，那么就证明有物体经过，则进行处理
            print("HIGH!!!!!!!!!!!!!")
        # 必要的软件延时
        time.sleep(0.1)
    
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        if ser != None:
            ser.close()
