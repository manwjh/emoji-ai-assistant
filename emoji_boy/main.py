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

from core.llm_client import LLMClient
from core.auto_encoder import AutoEncoderScheduler
import config


class EmojiAssistant:
    """Emoji 助手主控制器"""
    
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)
        
        # 设置应用程序属性
        self.app.setApplicationName("Emoji Assistant")
        self.app.setApplicationVersion("0.1.1")
        
        # 配置字体，避免字体警告
        self._setup_fonts()
        
        # 初始化核心组件
        self.llm_client = None
        self.floating_window = None
        self.auto_encoder_scheduler = None
        
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
            
            # 根据操作系统选择合适的字体
            import platform
            system = platform.system()
            
            if system == "Darwin":  # macOS
                system_font.setFamily("SF Pro Display")  # macOS 系统字体
            elif system == "Windows":
                system_font.setFamily("Segoe UI")  # Windows 系统字体
            else:  # Linux 或其他
                system_font.setFamily("DejaVu Sans")  # Linux 通用字体
            
            # 如果系统字体不可用，回退到通用字体
            if not system_font.exactMatch():
                system_font.setFamily("Arial")
            
            self.app.setFont(system_font)
            
            # 设置字体大小
            system_font.setPointSize(9)
            
        except Exception as e:
            print(f"⚠️ 字体设置失败: {e}")
            # 使用最基本的字体设置
            try:
                basic_font = QFont("Arial", 9)
                self.app.setFont(basic_font)
            except:
                pass
    
    def _init_components(self):
        """初始化组件"""
        try:
            # 初始化核心组件
            self.llm_client = LLMClient()
            
            # 初始化UI组件
            self.floating_window = FloatingEmojiWindow(
                llm_client=self.llm_client
            )
            
            # 初始化自动编码调度器
            self.auto_encoder_scheduler = AutoEncoderScheduler()
                        
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
            
            # 程序退出前执行编码（如果今天还没执行过）
            if self.auto_encoder_scheduler:
                self.auto_encoder_scheduler.run_on_exit()
            
            
            # 关闭窗口
            if self.floating_window:
                self.floating_window.close()
            
            # 停止自动编码调度器
            if self.auto_encoder_scheduler:
                self.auto_encoder_scheduler.stop()
            
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
        
            # 启动自动编码调度器
            if self.auto_encoder_scheduler:
                self.auto_encoder_scheduler.start()
            
            print("✅ Emoji 助手已启动，悬浮在屏幕右下角")
            print("💡 点击 Emoji 开始对话")
            print("🔄 自动编码调度器已启动，每天凌晨3点自动执行编码")
            
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