
# -*- coding: utf-8 -*
import RPi.GPIO as GPIO
import serial
import time

class AsrPro():

    GPIO_PA_4 = 37
    SERIAL_HELLO = "hello"
    
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(GPIO_PA_4, GPIO.IN)    # 定义25引脚为输入模式
        
        # 打开串口
        # ser = serial.Serial("/dev/ttyAMA0", 115200)
        self.ser = serial.Serial("/dev/ttyS0", 115200)
    
    def terminate()
        if self.ser != None:
            self.ser.close()
        GPIO.clean()
    
    def __del__(self):
        self.terminate()
    
    def listen(self, detected_callback):
        def __detected_callback():
            # 获得接收缓冲区字符
            count = self.ser.inWaiting()
            recv = ""
            if count != 0:
                # 读取内容并回显
                recv = self.ser.read(count)
                # self.ser.write(recv)
                print(recv)
            # 清空接收缓冲区
            self.ser.flushInput()
            if GPIO.input(GPIO_PA_4) and SERIAL_HELLO in recv:    # 用GPIO.input(引脚)函数来获取引脚电平状态
                                # 如果有信号输入，那么就证明有物体经过，则进行处理
                print("HIGH!!!!!!!!!!!!!")
                if (detected_callback):
                    detected_callback()
        GPIO.add_event_detect(GPIO_PA_4, GPIO.RISING, callback=__detected_callback, bouncetime=200)