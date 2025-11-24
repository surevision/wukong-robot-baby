
# -*- coding: utf-8 -*
import RPi.GPIO as GPIO
import serial
import time

class AsrPro():

    GPIO_PA_4 = 37
    SERIAL_HELLO = "hello"
    BOUNCETIME = 2000
    
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(GPIO_PA_4, GPIO.IN)    # 定义25引脚为输入模式
        
        # 打开串口
        self.ser = serial.Serial("/dev/ttyAMA0", 115200)
        # self.ser = serial.Serial("/dev/ttyS0", 115200)
    
    def terminate()
        if self.ser != None:
            self.ser.close()
        GPIO.clean()
    
    def __del__(self):
        pass
        # self.terminate()
    
    # 回调方式
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
            if GPIO.input(GPIO_PA_4) and len(recv) > 2:    # 用GPIO.input(引脚)函数来获取引脚电平状态
                print("HIGH!!!!!!!!!!!!!")
                if (detected_callback):
                    detected_callback()
        GPIO.add_event_detect(GPIO_PA_4, GPIO.RISING, callback=__detected_callback, bouncetime=BOUNCETIME)
    
    # 主循环模式
    def loop(self, detected_callback):
        last_time = time.time()
        while True:
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
            if GPIO.input(GPIO_PA_4) and len(recv) > 2:    # 用GPIO.input(引脚)函数来获取引脚电平状态
                print("HIGH!!!!!!!!!!!!!")
                if time.time() - last_time > BOUNCETIME:
                    last_time = time.time()
                    if (detected_callback):
                        detected_callback()
            time.sleep(0.03)