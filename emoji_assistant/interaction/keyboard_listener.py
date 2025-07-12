"""
键盘监听模块
"""

import threading
import time
from pynput import keyboard
from PyQt5.QtCore import QObject, pyqtSignal


class KeyboardListener(QObject):
    """键盘监听器"""
    
    # 信号定义
    key_pressed = pyqtSignal(str)  # 按键字符
    listening_started = pyqtSignal()
    listening_stopped = pyqtSignal()
    
    def __init__(self, emotion_detector=None):
        super().__init__()
        
        self.emotion_detector = emotion_detector
        self.listener = None
        self.is_listening = False
        self.listening_thread = None
        
        # 配置
        self.enabled = True
        self.ignore_special_keys = True
        self.ignore_modifier_keys = True
        
        # 特殊键映射
        self.special_key_map = {
            keyboard.Key.space: ' ',
            keyboard.Key.enter: '\n',
            keyboard.Key.tab: '\t',
            keyboard.Key.backspace: '\b',
            keyboard.Key.delete: '\x7f'
        }
        
        # 修饰键列表
        self.modifier_keys = {
            keyboard.Key.shift, keyboard.Key.shift_r,
            keyboard.Key.ctrl, keyboard.Key.ctrl_r,
            keyboard.Key.alt, keyboard.Key.alt_r,
            keyboard.Key.cmd, keyboard.Key.cmd_r,
            keyboard.Key.caps_lock
        }
        
        # 添加可能存在的修饰键
        try:
            self.modifier_keys.add(keyboard.Key.num_lock)
        except AttributeError:
            pass
        
        try:
            self.modifier_keys.add(keyboard.Key.scroll_lock)
        except AttributeError:
            pass
    
    def start_listening(self):
        """开始监听键盘"""
        if self.is_listening:
            print("⚠️ 键盘监听器已经在运行")
            return
        
        try:
            self.is_listening = True
            self.listening_thread = threading.Thread(target=self._listen_loop)
            self.listening_thread.daemon = True
            self.listening_thread.start()
            
            self.listening_started.emit()
            print("🎹 键盘监听器已启动")
            
        except Exception as e:
            print(f"❌ 启动键盘监听器失败: {e}")
            self.is_listening = False
    
    def stop_listening(self):
        """停止监听键盘"""
        if not self.is_listening:
            return
        
        try:
            self.is_listening = False
            
            if self.listener:
                self.listener.stop()
                self.listener = None
            
            if self.listening_thread and self.listening_thread.is_alive():
                self.listening_thread.join(timeout=1.0)
            
            self.listening_stopped.emit()
            print("🛑 键盘监听器已停止")
            
        except Exception as e:
            print(f"❌ 停止键盘监听器失败: {e}")
    
    def _listen_loop(self):
        """监听循环"""
        try:
            with keyboard.Listener(
                on_press=self._on_key_press,
                on_release=self._on_key_release
            ) as listener:
                self.listener = listener
                listener.join()
                
        except Exception as e:
            print(f"❌ 键盘监听循环出错: {e}")
            self.is_listening = False
    
    def _on_key_press(self, key):
        """按键按下事件"""
        if not self.enabled or not self.is_listening:
            return
        
        try:
            char = self._get_key_char(key)
            if char:
                # 发送信号
                self.key_pressed.emit(char)
                
                # 发送到情绪检测器
                if self.emotion_detector:
                    self.emotion_detector.add_character(char)
                
        except Exception as e:
            print(f"❌ 处理按键事件失败: {e}")
    
    def _on_key_release(self, key):
        """按键释放事件"""
        # 目前不需要处理释放事件
        pass
    
    def _get_key_char(self, key):
        """获取按键字符"""
        try:
            # 处理特殊键
            if hasattr(key, 'char'):
                if key.char:
                    return key.char
                else:
                    return None
            
            # 处理特殊键映射
            if key in self.special_key_map:
                return self.special_key_map[key]
            
            # 忽略修饰键
            if self.ignore_modifier_keys and key in self.modifier_keys:
                return None
            
            # 忽略其他特殊键
            if self.ignore_special_keys:
                return None
            
            # 尝试转换为字符
            return str(key)
            
        except Exception as e:
            print(f"❌ 获取按键字符失败: {e}")
            return None
    
    def set_enabled(self, enabled):
        """设置监听器启用状态"""
        self.enabled = enabled
        if enabled:
            print("✅ 键盘监听器已启用")
        else:
            print("⏸️ 键盘监听器已暂停")
    
    def set_ignore_special_keys(self, ignore):
        """设置是否忽略特殊键"""
        self.ignore_special_keys = ignore
    
    def set_ignore_modifier_keys(self, ignore):
        """设置是否忽略修饰键"""
        self.ignore_modifier_keys = ignore
    
    def add_special_key_mapping(self, key, char):
        """添加特殊键映射"""
        self.special_key_map[key] = char
    
    def get_status(self):
        """获取监听器状态"""
        return {
            'is_listening': self.is_listening,
            'enabled': self.enabled,
            'ignore_special_keys': self.ignore_special_keys,
            'ignore_modifier_keys': self.ignore_modifier_keys
        }
    
    def __del__(self):
        """析构函数"""
        self.stop_listening() 