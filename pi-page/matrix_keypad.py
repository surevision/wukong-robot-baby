#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
import threading
from collections import defaultdict
import os

try:
    import keyboard
    KEYBOARD_AVAILABLE = True
except ImportError:
    KEYBOARD_AVAILABLE = False
    print("警告: keyboard库未安装，将使用模拟模式运行")

class MatrixKeypad:
    def __init__(self):
        # 设置GPIO模式为BCM
        GPIO.setmode(GPIO.BCM)
        
        # 定义行和列的GPIO引脚（BCM编号）
        self.rows = [21, 20, 16, 12]    # 行引脚
        self.cols = [13, 6, 25, 29]    # 列引脚
        
        # 定义键盘映射（4x4）
        self.key_map = [
            ['1', '2', '3', 'A'],
            ['4', '5', '6', 'B'],
            ['7', '8', '9', 'C'],
            ['*', '0', '#', 'D']
        ]
        
        # 按键状态跟踪
        self.key_states = defaultdict(lambda: False)
        
        # 设置行引脚为输出，初始为高电平
        for row_pin in self.rows:
            GPIO.setup(row_pin, GPIO.OUT)
            GPIO.output(row_pin, GPIO.HIGH)
        
        # 设置列引脚为输入，启用上拉电阻
        for col_pin in self.cols:
            GPIO.setup(col_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        # 运行标志
        self.running = True
        
    def get_key_mapping(self, key):
        """获取按键映射"""
        key_mapping = {
            
            # 数字键映射
            '1': '1', '2': '2', '3': '3',
            '4': '4', '5': '5', '6': '6',
            '7': '7', '8': '8', '9': '9',
            '0': '0',
            
            # 字母键映射
            'A': 'a', 'B': 'b', 'C': 'c', 'D': 'd',

            # 方向键映射
            '8': 'down',    # 上键
            '2': 'up',      # 下键
            '4': 'left',    # 左
            '6': 'right',   # 右
            
            # 功能键映射
            'A': 'esc',     # ESC
            'B': 'backspace', # 退格
            'C': 'space',   # 空格
            'D': 'enter',   # 回车
            '5': 'enter',     # ESC
        }
        return key_mapping.get(key)
    
    def get_key_name(self, key):
        """获取键名"""
        key_names = {
            'up': "上箭头",
            'down': "下箭头", 
            'left': "左箭头",
            'right': "右箭头",
            'esc': "ESC",
            'backspace': "退格",
            'space': "空格", 
            'enter': "回车",
            '1': "1", '2': "2", '3': "3",
            '4': "4", '5': "5", '6': "6",
            '7': "7", '8': "8", '9': "9",
            '0': "0",
            'a': "A", 'b': "B", 'c': "C", 'd': "D",
        }
        return key_names.get(key, key)
    
    def scan_keypad(self):
        """扫描键盘并检测按键状态变化"""
        while self.running:
            for row_idx, row_pin in enumerate(self.rows):
                # 将当前行设置为低电平
                GPIO.output(row_pin, GPIO.LOW)
                
                # 检查每一列
                for col_idx, col_pin in enumerate(self.cols):
                    # 读取列引脚状态
                    current_state = GPIO.input(col_pin) == GPIO.LOW
                    key_char = self.key_map[row_idx][col_idx]
                    
                    # 检测状态变化
                    if current_state and not self.key_states[key_char]:
                        # 按键按下
                        self.key_states[key_char] = True
                        self.on_key_press(key_char)
                    elif not current_state and self.key_states[key_char]:
                        # 按键释放
                        self.key_states[key_char] = False
                        self.on_key_release(key_char)
                
                # 恢复当前行为高电平
                GPIO.output(row_pin, GPIO.HIGH)
                
                # 短暂延迟防止抖动
                time.sleep(0.001)
            
            # 扫描间隔
            time.sleep(0.01)
    
    def on_key_press(self, key):
        """处理按键按下事件"""
        print(f"[按下] 按键: {key}")
        
        # 获取键映射
        key_name = self.get_key_mapping(key)
        
        if key_name is not None and KEYBOARD_AVAILABLE:
            # 使用keyboard库模拟按键按下
            try:
                keyboard.press(key_name)
                key_display_name = self.get_key_name(key_name)
                print(f"  模拟按键按下: {key_display_name} : {key_name} {key}")
            except Exception as ex:
                print(f"  模拟按键失败: {ex}")
        else:
            # 未映射的键或keyboard库不可用
            print(f"  keyboard库不可用或未映射的键: {key}")
    
    def on_key_release(self, key):
        """处理按键释放事件"""
        print(f"[释放] 按键: {key}")
        
        # 获取键映射
        key_name = self.get_key_mapping(key)
        
        if key_name is not None and KEYBOARD_AVAILABLE:
            # 使用keyboard库模拟按键释放
            try:
                keyboard.release(key_name)
                key_display_name = self.get_key_name(key_name)
                print(f"  模拟按键释放: {key_display_name} : {key_name} {key}")
            except Exception as ex:
                print(f"  模拟按键释放失败: {ex}")
    
    def print_key_mapping(self):
        """打印按键映射说明"""
        print("\n=== 键盘映射说明 ===")
        print("方向键:")
        print("  8 -> 下箭头")
        print("  2 -> 上箭头") 
        print("  4 -> 左箭头")
        print("  6 -> 右箭头")
        print("  5 -> 回车")
        print("功能键:")
        print("  A -> ESC")
        print("  B -> 退格")
        print("  C -> 空格") 
        print("  D -> 回车")
        print("数字键: 发送对应数字")
        print("字母键: 发送对应字母")
        print("特殊键 * 和 #: 仅显示")
        if not KEYBOARD_AVAILABLE:
            print("模式: 模拟模式（仅显示按键信息）")
        else:
            print("模式: keyboard库模拟按键")
        print("==================\n")
    
    def test_keyboard(self):
        """测试keyboard库功能"""
        if not KEYBOARD_AVAILABLE:
            print("keyboard库不可用，跳过测试")
            return
            
        print("执行键盘测试...")
        test_keys = ['a', '1', 'enter']
        
        for key in test_keys:
            print(f"测试按键: {self.get_key_name(key)}")
            try:
                keyboard.press(key)
                time.sleep(0.1)
                keyboard.release(key)
                time.sleep(0.5)
            except Exception as ex:
                print(f"测试按键失败: {ex}")
    
    def start(self):
        """启动键盘扫描"""
        self.print_key_mapping()
        
        # 测试键盘功能
        # self.test_keyboard()
        
        print("开始扫描键盘...")
        print("按Ctrl+C退出")
        
        try:
            self.scan_thread = threading.Thread(target=self.scan_keypad)
            self.scan_thread.daemon = True
            self.scan_thread.start()
            
            # 主线程等待
            while self.running:
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        """停止扫描并清理资源"""
        print("\n停止键盘扫描...")
        self.running = False
        
        # 等待扫描线程结束
        if hasattr(self, 'scan_thread'):
            self.scan_thread.join(timeout=1.0)
        
        # 清理GPIO
        GPIO.cleanup()
        print("GPIO资源已清理")

def main():
    # 检查keyboard库是否可用
    if not KEYBOARD_AVAILABLE:
        print("keyboard库未安装，请安装:")
        print("  sudo pip3 install keyboard")
        print("将继续在模拟模式下运行...")
        print()
    
    try:
        keypad = MatrixKeypad()
        keypad.start()
    except Exception as e:
        print(f"程序运行出错: {e}")
        import traceback
        traceback.print_exc()
        GPIO.cleanup()

if __name__ == "__main__":
    main()