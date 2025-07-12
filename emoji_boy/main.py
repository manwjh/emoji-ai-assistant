#!/usr/bin/env python3
"""
Emoji 虚拟人桌面助手 - 主程序入口
"""

import sys
import signal
import atexit
import traceback
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QThread, QTimer
from PyQt5.QtGui import QFont

from ui.floating_head import FloatingEmojiWindow
from interaction.emotion_detector import EmotionDetector
from core.llm_client import LLMClient
import config


class EmojiAssistant:
    """Emoji 助手主控制器"""
    
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)
        
        # 设置应用程序属性
        self.app.setApplicationName("Emoji Assistant")
        self.app.setApplicationVersion("0.1.0")
        
        # 配置字体，避免字体警告
        self._setup_fonts()
        
        # 初始化核心组件
        self.llm_client = None
        self.emotion_detector = None
        self.floating_window = None
        self.keyboard_thread = None
        
        # 初始化组件
        self._init_components()
        
        # 设置信号处理
        self._setup_signal_handlers()
        
        # 注册清理函数
        atexit.register(self._cleanup)
    
    def _setup_fonts(self):
        """设置字体，避免字体警告"""
        try:
            # 设置默认字体为系统可用字体
            system_font = QFont()
            system_font.setFamily("Arial")  # 使用通用字体
            self.app.setFont(system_font)
        except Exception as e:
            print(f"⚠️ 字体设置失败: {e}")
    
    def _init_components(self):
        """初始化组件"""
        try:
            # 初始化核心组件
            self.llm_client = LLMClient()
            self.emotion_detector = EmotionDetector()
            
            # 初始化UI组件
            self.floating_window = FloatingEmojiWindow(
                llm_client=self.llm_client,
                emotion_detector=self.emotion_detector
            )
            
            # 连接信号
            # self.emotion_detector.emotion_detected.connect(
            #     self.floating_window.show_emotion_bubble
            # )
            
            print("✅ 组件初始化成功")
            
        except Exception as e:
            print(f"❌ 组件初始化失败: {e}")
            traceback.print_exc()
            raise
    
    def _setup_signal_handlers(self):
        """设置信号处理器"""
        try:
            signal.signal(signal.SIGINT, self.signal_handler)
            signal.signal(signal.SIGTERM, self.signal_handler)
            
            # 在macOS上处理额外的信号
            if hasattr(signal, 'SIGUSR1'):
                signal.signal(signal.SIGUSR1, self.signal_handler)
            if hasattr(signal, 'SIGUSR2'):
                signal.signal(signal.SIGUSR2, self.signal_handler)
                
        except Exception as e:
            print(f"⚠️ 信号处理器设置失败: {e}")
    
    def signal_handler(self, signum, frame):
        """信号处理器"""
        print(f"\n🛑 收到信号 {signum}，正在优雅退出...")
        self._cleanup()
        self.app.quit()
        sys.exit(0)
    
    def _cleanup(self):
        """清理资源"""
        try:
            print("🧹 正在清理资源...")
            
            # 停止线程
            if self.keyboard_thread and self.keyboard_thread.isRunning():
                self.keyboard_thread.quit()
                self.keyboard_thread.wait(3000)  # 等待3秒
                if self.keyboard_thread.isRunning():
                    self.keyboard_thread.terminate()
            
            # 关闭窗口
            if self.floating_window:
                self.floating_window.close()
            
            print("✅ 资源清理完成")
            
        except Exception as e:
            print(f"⚠️ 资源清理时出错: {e}")
    
    def start(self):
        """启动助手"""
        try:
            print("🚀 启动 Emoji 虚拟人桌面助手...")
            
            # 显示悬浮窗口
            if self.floating_window:
                self.floating_window.show()
                # 确保窗口在最顶层
                self.floating_window.raise_()
                self.floating_window.activateWindow()
            
            # 启动键盘监听
            if self.keyboard_thread:
                self.keyboard_thread.start()
            
            print("✅ Emoji 助手已启动，悬浮在屏幕右下角")
            print("💡 点击 Emoji 开始对话，或输入情绪关键词触发安慰")
            
            # 设置定时器检查程序状态
            self._setup_health_check()
            
            # 运行应用
            return self.app.exec_()
            
        except Exception as e:
            print(f"❌ 启动失败: {e}")
            traceback.print_exc()
            return 1
    
    def _setup_health_check(self):
        """设置健康检查定时器"""
        try:
            health_timer = QTimer()
            health_timer.timeout.connect(self._health_check)
            health_timer.start(30000)  # 每30秒检查一次
        except Exception as e:
            print(f"⚠️ 健康检查设置失败: {e}")
    
    def _health_check(self):
        """健康检查"""
        try:
            # 检查线程状态
            if self.keyboard_thread and not self.keyboard_thread.isRunning():
                print("⚠️ 键盘监听线程异常停止")
            
            # 检查悬浮窗口是否在最顶层
            if self.floating_window and self.floating_window.isVisible():
                # 确保悬浮窗口保持在最顶层
                self.floating_window.raise_()
                
        except Exception as e:
            print(f"⚠️ 健康检查失败: {e}")


def main():
    """主函数"""
    assistant = None
    try:
        assistant = EmojiAssistant()
        exit_code = assistant.start()
        sys.exit(exit_code)
        
    except KeyboardInterrupt:
        print("\n👋 用户中断，正在退出...")
        if assistant:
            assistant._cleanup()
        sys.exit(0)
        
    except Exception as e:
        print(f"❌ 程序异常退出: {e}")
        traceback.print_exc()
        if assistant:
            assistant._cleanup()
        sys.exit(1)


if __name__ == "__main__":
    main() 