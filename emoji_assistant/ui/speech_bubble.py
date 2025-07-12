"""
对话气泡组件
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QGraphicsDropShadowEffect,
    QApplication
)
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt5.QtGui import QFont, QPainter, QColor, QPen, QPainterPath


class SpeechBubbleWidget(QWidget):
    """对话气泡组件"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 窗口属性设置
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # 初始化UI
        self.init_ui()
        
        # 设置动画
        self.setup_animations()
        
        # 自动隐藏定时器
        self.auto_hide_timer = QTimer()
        self.auto_hide_timer.timeout.connect(self.hide_bubble)
        
        # 当前消息
        self.current_message = ""
        
        # 透明度属性（用于动画）
        self._opacity = 1.0
    
    def init_ui(self):
        """初始化用户界面"""
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 10, 15, 10)
        
        # 消息标签
        self.message_label = QLabel()
        self.message_label.setWordWrap(True)
        self.message_label.setFont(QFont("Arial", 13))
        self.message_label.setStyleSheet("""
            QLabel {
                color: #222;
                background: transparent;
                border: none;
                padding: 5px;
                text-shadow: 0 1px 2px rgba(255,255,255,0.2);
            }
        """)
        
        # 添加阴影效果
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(18)
        shadow.setColor(QColor(0, 0, 0, 40))
        shadow.setOffset(0, 4)
        self.message_label.setGraphicsEffect(shadow)
        
        layout.addWidget(self.message_label)
        self.setLayout(layout)
        
        # 设置样式
        self.setStyleSheet("""
            SpeechBubbleWidget {
                background: rgba(255,255,255,0.65);
                border-radius: 16px;
                border: 1.2px solid rgba(255,255,255,0.35);
            }
        """)
    
    def setup_animations(self):
        """设置动画效果"""
        # 淡入动画
        self.fade_in_animation = QPropertyAnimation(self, b"opacity")
        self.fade_in_animation.setDuration(300)
        self.fade_in_animation.setEasingCurve(QEasingCurve.OutCubic)
        
        # 淡出动画
        self.fade_out_animation = QPropertyAnimation(self, b"opacity")
        self.fade_out_animation.setDuration(300)
        self.fade_out_animation.setEasingCurve(QEasingCurve.InCubic)
        self.fade_out_animation.finished.connect(self.hide)
    
    def show_message(self, message, auto_hide=True, duration=5000):
        """显示消息"""
        self.current_message = message
        self.message_label.setText(message)
        
        # 调整窗口大小以适应内容
        self.adjustSize()
        
        # 定位到Emoji窗口旁边
        self.position_next_to_emoji()
        
        # 显示窗口
        self.show()
        
        # 播放淡入动画
        self.fade_in_animation.setStartValue(0.0)
        self.fade_in_animation.setEndValue(1.0)
        self.fade_in_animation.start()
        
        # 设置自动隐藏
        if auto_hide:
            self.auto_hide_timer.start(duration)
    
    def position_next_to_emoji(self):
        """定位到Emoji窗口旁边"""
        if self.parent():
            parent_geometry = self.parent().geometry()
            parent_center = parent_geometry.center()
            
            # 计算气泡位置（在Emoji左侧）
            bubble_x = parent_geometry.left() - self.width() - 10
            bubble_y = parent_center.y() - self.height() // 2
            
            # 确保气泡不超出屏幕边界
            screen = QApplication.primaryScreen().geometry()
            if bubble_x < screen.left():
                # 如果左侧空间不够，放在右侧
                bubble_x = parent_geometry.right() + 10
            
            if bubble_y < screen.top():
                bubble_y = screen.top() + 10
            elif bubble_y + self.height() > screen.bottom():
                bubble_y = screen.bottom() - self.height() - 10
            
            self.move(bubble_x, bubble_y)
    
    def hide_bubble(self):
        """隐藏气泡"""
        self.auto_hide_timer.stop()
        
        # 播放淡出动画
        self.fade_out_animation.setStartValue(1.0)
        self.fade_out_animation.setEndValue(0.0)
        self.fade_out_animation.start()
    
    def paintEvent(self, event):
        """绘制事件"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 设置透明度
        painter.setOpacity(self._opacity)
        
        # 绘制气泡背景
        rect = self.rect()
        painter.setBrush(QColor(255, 255, 255, 240))
        painter.setPen(QPen(QColor(0, 0, 0, 30), 1))
        
        # 绘制圆角矩形
        path = QPainterPath()
        path.addRoundedRect(rect, 15, 15)
        painter.drawPath(path)
        
        # 绘制小尾巴（指向Emoji）
        if self.parent():
            self.draw_tail(painter, rect)
    
    def draw_tail(self, painter, rect):
        """绘制气泡尾巴"""
        # 计算尾巴位置（指向Emoji）
        if self.parent():
            parent_center = self.parent().geometry().center()
            bubble_center = self.geometry().center()
            
            # 确定尾巴方向
            if self.x() < self.parent().x():
                # 气泡在Emoji左侧，尾巴向右
                tail_x = rect.right() - 5
                tail_y = rect.center().y()
                points = [
                    (tail_x, tail_y - 8),
                    (tail_x + 10, tail_y),
                    (tail_x, tail_y + 8)
                ]
            else:
                # 气泡在Emoji右侧，尾巴向左
                tail_x = rect.left() + 5
                tail_y = rect.center().y()
                points = [
                    (tail_x, tail_y - 8),
                    (tail_x - 10, tail_y),
                    (tail_x, tail_y + 8)
                ]
            
            # 绘制尾巴
            painter.setBrush(QColor(255, 255, 255, 240))
            painter.setPen(QPen(QColor(0, 0, 0, 30), 1))
            
            path = QPainterPath()
            path.moveTo(points[0][0], points[0][1])
            path.lineTo(points[1][0], points[1][1])
            path.lineTo(points[2][0], points[2][1])
            path.closeSubpath()
            
            painter.drawPath(path)
    
    # 透明度属性（用于动画）
    def get_opacity(self):
        return self._opacity
    
    def set_opacity(self, opacity):
        self._opacity = opacity
        self.update()
    
    opacity = pyqtProperty(float, get_opacity, set_opacity) 