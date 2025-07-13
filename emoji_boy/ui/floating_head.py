"""
悬浮 Emoji 虚拟人窗口
"""

import sys
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, 
    QApplication, QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, pyqtSignal
from PyQt5.QtGui import QFont, QPainter, QColor, QPixmap, QIcon

from interaction.chat_input import ChatInputDialog
from core.chat_memory import chat_memory


class FloatingEmojiWindow(QWidget):
    """悬浮 Emoji 虚拟人窗口"""
    
    # 信号定义
    emoji_clicked = pyqtSignal()
    
    def __init__(self, llm_client=None):
        super().__init__()
        
        self.llm_client = llm_client
        
        # 窗口属性设置 - 优化以减少对其他程序的影响
        self.setWindowFlags(
            Qt.FramelessWindowHint |  # 无边框
            Qt.WindowStaysOnTopHint |  # 总在最前
            Qt.Tool |  # 不在任务栏显示，减少系统干扰
            Qt.WindowDoesNotAcceptFocus  # 不接受焦点
        )
        self.setAttribute(Qt.WA_TranslucentBackground)  # 透明背景
        self.setAttribute(Qt.WA_ShowWithoutActivating)  # 显示时不激活
        self.setAttribute(Qt.WA_NoSystemBackground)  # 无系统背景
        self.setAttribute(Qt.WA_TranslucentBackground)  # 确保完全透明
        
        # 窗口大小和位置
        self.resize(80, 80)
        self.move_to_bottom_right()
        
        # 初始化UI
        self.init_ui()
        
        # 动画效果
        self.setup_animations()
        
        # 聊天对话框
        self.chat_dialog = None
        
        # 拖拽相关
        self.dragging = False
        self.drag_position = None
        
        # 保持最顶层的定时器 - 降低频率以减少系统影响
        self.stay_on_top_timer = QTimer()
        self.stay_on_top_timer.timeout.connect(self.ensure_stay_on_top)
        self.stay_on_top_timer.start(2000)  # 每2秒检查一次，减少系统负担
        
        # 记录上次检查时间，避免频繁操作
        self.last_check_time = 0
    
    def init_ui(self):
        """初始化用户界面"""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Emoji 标签
        self.emoji_label = QLabel("😺")
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setFont(QFont("Arial", 40))
        self.emoji_label.setStyleSheet("""
            QLabel {
                color: #333333;
                background: transparent;
                border: none;
                background-color: transparent;
            }
        """)
        
        # 添加阴影效果（可选，如果不需要阴影可以注释掉）
        # shadow = QGraphicsDropShadowEffect()
        # shadow.setBlurRadius(15)
        # shadow.setColor(QColor(0, 0, 0, 80))
        # shadow.setOffset(0, 2)
        # self.emoji_label.setGraphicsEffect(shadow)
        
        layout.addWidget(self.emoji_label)
        self.setLayout(layout)
        
        # 设置鼠标样式
        self.setCursor(Qt.PointingHandCursor)
        
        # 设置窗口完全透明
        self.setStyleSheet("""
            QWidget {
                background: transparent;
                background-color: transparent;
                border: none;
            }
        """)
    
    def paintEvent(self, event):
        """重写paintEvent以确保完全透明"""
        # 不绘制任何背景，完全透明
        pass
    
    def setup_animations(self):
        """设置动画效果"""
        # 悬停动画
        self.hover_animation = QPropertyAnimation(self, b"geometry")
        self.hover_animation.setDuration(200)
        self.hover_animation.setEasingCurve(QEasingCurve.OutCubic)
        
        # 点击动画
        self.click_animation = QPropertyAnimation(self, b"geometry")
        self.click_animation.setDuration(100)
        self.click_animation.setEasingCurve(QEasingCurve.OutBounce)
    
    def move_to_bottom_right(self):
        """移动到屏幕右下角"""
        screen = QApplication.primaryScreen().geometry()
        x = screen.width() - self.width() - 20
        y = screen.height() - self.height() - 100
        self.move(x, y)
    
    def mousePressEvent(self, event):
        """鼠标按下事件"""
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        """鼠标移动事件"""
        if event.buttons() == Qt.LeftButton and self.dragging:
            self.move(event.globalPos() - self.drag_position)
            event.accept()
    
    def mouseReleaseEvent(self, event):
        """鼠标释放事件"""
        if event.button() == Qt.LeftButton:
            self.dragging = False
            # 检查是否为点击（非拖拽）
            if self.drag_position and (event.globalPos() - self.frameGeometry().topLeft() - self.drag_position).manhattanLength() < 5:
                self.on_emoji_clicked()
            event.accept()
    
    def on_emoji_clicked(self):
        """Emoji 被点击时的处理"""
        # 播放点击动画
        self.play_click_animation()
        
        # 发射信号
        self.emoji_clicked.emit()
        
        # 打开聊天输入对话框
        self.open_chat_dialog()
    
    def play_click_animation(self):
        """播放点击动画"""
        current_geometry = self.geometry()
        target_geometry = current_geometry.adjusted(2, 2, -2, -2)
        
        self.click_animation.setStartValue(current_geometry)
        self.click_animation.setEndValue(target_geometry)
        self.click_animation.start()
        
        # 动画结束后恢复
        QTimer.singleShot(100, lambda: self.click_animation.setDirection(QPropertyAnimation.Backward))
    
    def open_chat_dialog(self):
        """打开聊天输入对话框"""
        if self.llm_client:
            # 检查是否已经有对话窗口打开
            if self.chat_dialog is None or not self.chat_dialog.isVisible():
                # 开始新的对话会话（每次打开新窗口都开始新会话）
                chat_memory.start_new_session()
                
                self.chat_dialog = ChatInputDialog(self.llm_client, self)
                # 连接关闭信号，清理引用
                self.chat_dialog.finished.connect(self.on_chat_dialog_closed)
                self.chat_dialog.show()
            else:
                # 如果窗口已存在，将其激活并置顶
                self.chat_dialog.raise_()
                self.chat_dialog.activateWindow()
    
    def on_chat_dialog_closed(self, result):
        """聊天对话框关闭时的处理"""
        # 结束当前对话会话
        chat_memory.end_current_session()
        self.chat_dialog = None
    
    def enterEvent(self, event):
        """鼠标进入事件"""
        # 播放悬停动画
        current_geometry = self.geometry()
        target_geometry = current_geometry.adjusted(-2, -2, 2, 2)
        
        self.hover_animation.setStartValue(current_geometry)
        self.hover_animation.setEndValue(target_geometry)
        self.hover_animation.start()
    
    def leaveEvent(self, event):
        """鼠标离开事件"""
        # 恢复原始大小
        current_geometry = self.geometry()
        target_geometry = current_geometry.adjusted(2, 2, -2, -2)
        
        self.hover_animation.setStartValue(current_geometry)
        self.hover_animation.setEndValue(target_geometry)
        self.hover_animation.start()
    
    def ensure_stay_on_top(self):
        """确保窗口保持在最顶层，同时减少对其他程序的影响"""
        import time
        current_time = time.time()
        
        # 避免过于频繁的检查，至少间隔1秒
        if current_time - self.last_check_time < 1.0:
            return
        
        self.last_check_time = current_time
        
        # 只在窗口不可见时才进行恢复操作
        if not self.isVisible():
            self.show()
            return
        
        # 检查是否真的需要恢复最顶层状态
        # 只有在窗口被其他程序完全覆盖时才进行操作
        if not self.isActiveWindow() and not self.isVisible():
            # 使用更温和的方式保持最顶层，减少系统干扰
            self.setWindowFlags(
                Qt.FramelessWindowHint |
                Qt.WindowStaysOnTopHint |
                Qt.Tool |
                Qt.WindowDoesNotAcceptFocus
            )
            self.show()
            self.raise_() 