"""
聊天输入对话框
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTextEdit, 
    QPushButton, QLabel, QProgressBar, QFrame, QApplication,
    QScrollArea, QWidget, QSizePolicy
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QThread, QSize
from PyQt5.QtGui import QFont, QIcon, QKeyEvent, QTextCursor
import re
from .chat_state_machine import ChatStateMachine, ChatState
from core.config_manager import config_manager


class MessageWidget(QWidget):
    """单条消息组件"""
    
    def __init__(self, text, is_user=True, parent=None):
        super().__init__(parent)
        self.text = text
        self.is_user = is_user
        self.init_ui()
    
    def init_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 5, 10, 5)
        
        # 使用QTextEdit替代QLabel以支持文本选择和复制
        message_text = QTextEdit()
        message_text.setPlainText(self.text)
        message_text.setReadOnly(True)
        message_text.setMaximumWidth(400)
        message_text.setMaximumHeight(200)  # 限制最大高度
        message_text.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        message_text.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        message_text.setStyleSheet(f"""
            QTextEdit {{
                background: {'#007AFF' if self.is_user else '#E5E5EA'};
                color: {'white' if self.is_user else 'black'};
                border-radius: 18px;
                padding: 12px 16px;
                font-size: 14px;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                border: none;
                selection-background-color: {'rgba(255,255,255,0.3)' if self.is_user else 'rgba(0,0,0,0.1)'};
            }}
            QTextEdit:focus {{
                outline: none;
                border: none;
            }}
        """)
        
        # 根据消息类型调整布局
        if self.is_user:
            layout.addStretch()
            layout.addWidget(message_text)
        else:
            layout.addWidget(message_text)
            layout.addStretch()
        
        self.setLayout(layout)


class CustomTextEdit(QTextEdit):
    """自定义文本编辑器，处理回车键事件"""
    enter_pressed = pyqtSignal()
    escape_pressed = pyqtSignal()
    
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Return and event.modifiers() == Qt.NoModifier:
            self.enter_pressed.emit()
        elif event.key() == Qt.Key_Escape:
            self.escape_pressed.emit()
        else:
            super().keyPressEvent(event)


class ChatDialog(QDialog):
    """微信风格的聊天对话框"""
    message_sent = pyqtSignal(str, str)  # message, response

    def __init__(self, llm_client, parent=None):
        super().__init__(parent)
        self.llm_client = llm_client
        self.response_thread = None
        self.messages = []  # 存储消息历史
        self.temp_message_widget = None  # 临时状态消息组件
        self.drag_pos = None  # 拖动支持
        
        # 初始化状态机
        self.state_machine = ChatStateMachine()
        self.state_machine.state_changed.connect(self.on_state_changed)
        
        # self.setWindowTitle("Emoji 助手")  # 移除窗口标题
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
        self.setModal(False)
        self.resize(500, 600)
        self.init_ui()
        self.setup_styles()

    def paintEvent(self, event):
        from PyQt5.QtGui import QPainter, QColor, QBrush, QPen
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        color = QColor(255, 255, 255, 40)  # 半透明白色
        painter.setBrush(QBrush(color))
        painter.setPen(QPen(QColor(255, 255, 255, 80), 1))  # 半透明描边
        rect = self.rect().adjusted(0, 0, -1, -1)
        painter.drawRoundedRect(rect, 18, 18)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.drag_pos:
            self.move(event.globalPos() - self.drag_pos)
            event.accept()
        super().mouseMoveEvent(event)

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 移除标题栏
        # 标题栏代码已被注释或删除
        # title_bar = QFrame()
        # title_bar.setStyleSheet("""
        #     QFrame {
        #         background: #007AFF;
        #         border: none;
        #     }
        # """)
        # title_bar.setFixedHeight(50)
        
        # title_layout = QHBoxLayout(title_bar)
        # title_label = QLabel("😺 Emoji 助手")
        # title_label.setStyleSheet("""
        #     QLabel {
        #         color: white;
        #         font-size: 16px;
        #         font-weight: bold;
        #         font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        #     }
        # """)
        # title_layout.addWidget(title_label)
        # title_layout.addStretch()
        
        # layout.addWidget(title_bar)

        # 消息历史区域
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background: #F2F2F7;
            }
            QScrollBar:vertical {
                background: #F2F2F7;
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: #C7C7CC;
                border-radius: 4px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #A8A8AD;
            }
        """)
        
        self.messages_widget = QWidget()
        self.messages_layout = QVBoxLayout(self.messages_widget)
        self.messages_layout.setContentsMargins(10, 10, 10, 10)
        self.messages_layout.setSpacing(8)
        self.messages_layout.addStretch()
        
        self.scroll_area.setWidget(self.messages_widget)
        layout.addWidget(self.scroll_area)

        # 输入区域
        input_frame = QFrame()
        input_frame.setStyleSheet("""
            QFrame {
                background: white;
                border-top: 1px solid #E5E5EA;
            }
        """)
        input_frame.setFixedHeight(80)
        
        input_layout = QVBoxLayout(input_frame)
        input_layout.setContentsMargins(15, 10, 15, 15)
        
        # 输入框
        self.input_text = CustomTextEdit()
        self.input_text.setPlaceholderText("输入消息... (回车发送，ESC退出)")
        self.input_text.setFont(QFont("Arial", 14))
        self.input_text.setMaximumHeight(50)
        self.input_text.setStyleSheet("""
            QTextEdit {
                border: 1px solid #E5E5EA;
                border-radius: 20px;
                padding: 8px 15px;
                background: #F2F2F7;
                color: #333333;
                font-size: 14px;
            }
            QTextEdit:focus {
                border-color: #007AFF;
                background: white;
            }
        """)
        
        input_layout.addWidget(self.input_text)
        layout.addWidget(input_frame)
        
        self.setLayout(layout)
        self.input_text.setFocus()
        
        # 连接信号
        self.input_text.enter_pressed.connect(self.send_message)
        self.input_text.escape_pressed.connect(self.reject)
        
        # 启动状态机
        QTimer.singleShot(100, self.start_state_machine)

    def setup_styles(self):
        self.setStyleSheet("""
            QDialog {
                background: rgba(255, 255, 255, 0.55);
                border-radius: 18px;
                border: 1.5px solid rgba(255,255,255,0.35);
            }
            QScrollArea {
                border: none;
                background: transparent;
            }
            QFrame {
                background: transparent;
                border: none;
            }
            QTextEdit {
                border: 1.5px solid rgba(255,255,255,0.25);
                border-radius: 16px;
                background: rgba(255,255,255,0.35);
                color: #222;
                font-size: 15px;
                padding: 8px 15px;
            }
            QTextEdit:focus {
                border-color: #7ecfff;
                background: rgba(255,255,255,0.55);
            }
            QScrollBar:vertical {
                background: transparent;
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: rgba(200,200,200,0.4);
                border-radius: 4px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: rgba(160,160,160,0.5);
            }
        """)

    def add_message(self, text, is_user=True):
        """添加消息到对话历史"""
        message_widget = MessageWidget(text, is_user)
        self.messages.append(message_widget)
        
        # 在 stretch 之前插入消息
        self.messages_layout.insertWidget(len(self.messages) - 1, message_widget)
        
        # 滚动到底部
        QTimer.singleShot(100, self.scroll_to_bottom)
    
    def scroll_to_bottom(self):
        """滚动到消息历史底部"""
        scrollbar = self.scroll_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def show_temp_message(self, text):
        """显示临时状态消息（不记录在历史中）"""
        # 移除之前的临时消息
        self.remove_temp_message()
        
        # 创建新的临时消息
        self.temp_message_widget = MessageWidget(text, False)
        
        # 在 stretch 之前插入临时消息
        self.messages_layout.insertWidget(self.messages_layout.count() - 1, self.temp_message_widget)
        
        # 滚动到底部
        QTimer.singleShot(100, self.scroll_to_bottom)
    
    def remove_temp_message(self):
        """移除临时状态消息"""
        if self.temp_message_widget:
            self.temp_message_widget.deleteLater()
            self.temp_message_widget = None
    
    def start_state_machine(self):
        """启动状态机"""
        # 触发初始状态
        self.state_machine.process_message("", self)
    
    def on_state_changed(self, old_state: ChatState, new_state: ChatState):
        """状态变化处理"""
        print(f"状态变化: {old_state.value} → {new_state.value}")
        
        # 检查是否从临时对话切换到正常对话
        if (old_state in [ChatState.INIT, ChatState.CHECKING, ChatState.CONFIGURING, ChatState.ERROR] and 
            new_state == ChatState.NORMAL):
            # 清空临时对话历史，开始正常对话
            self.clear_temp_dialog_history()
        
        if new_state == ChatState.CHECKING:
            self.show_temp_message("连接🧠...")
            self.input_text.setEnabled(False)
            
            # 检查API连接
            result = self.llm_client.test_connection()
            self.remove_temp_message()
            
            if result["success"]:
                self.state_machine.change_state(ChatState.NORMAL)
                self.add_message("你好！我是你的 Emoji 助手，有什么可以帮助你的吗？", False)
            else:
                self.state_machine.change_state(ChatState.CONFIGURING)
                config_message = """抱歉啦，我没法联通主机。小主请检查一下网络，和告诉我令牌配置，格式如下：

base_url="https://ark.cn-beijing.volces.com/api/v3"
api_key=41a9d475-45a9-****-****-bbb75505e9bf
model="doubao-seed-1-6-flash-250615"

请按照上面的格式输入您的API配置信息。"""
                self.add_message(config_message, False)
            
            self.input_text.setEnabled(True)
            self.input_text.setFocus()
        
        elif new_state == ChatState.NORMAL:
            # 正常对话状态，确保输入框可用
            self.input_text.setEnabled(True)
            self.input_text.setFocus()
        
        elif new_state == ChatState.CONFIGURING:
            # 配置状态，确保输入框可用
            self.input_text.setEnabled(True)
            self.input_text.setFocus()
        
        elif new_state == ChatState.ERROR:
            # 错误状态，显示错误提示
            self.input_text.setEnabled(True)
            self.input_text.setFocus()
    
    # 状态机上下文方法
    def quit_application(self):
        """退出应用程序"""
        print("👋 收到退出命令，正在关闭程序...")
        self.accept()
        QApplication.instance().quit()
    
    def clear_chat_history(self):
        """清空对话历史"""
        # 清空消息列表
        for message in self.messages:
            message.deleteLater()
        self.messages.clear()
        
        # 移除临时消息
        self.remove_temp_message()
        
        # 添加重置确认消息
        self.add_message("✅ 对话历史已清空", False)
    
    def clear_temp_dialog_history(self):
        """清空临时对话历史（从临时状态切换到正常状态时调用）"""
        # 清空消息列表
        for message in self.messages:
            message.deleteLater()
        self.messages.clear()
        
        # 移除临时消息
        self.remove_temp_message()
        
        print("🧹 已清空临时对话历史，开始正常对话")
    
    def show_help_message(self, help_text: str):
        """显示帮助信息"""
        self.add_message(help_text, False)
    
    def show_status_message(self, status_text: str):
        """显示状态信息"""
        self.add_message(status_text, False)
    

    
    def parse_config_message(self, message):
        """解析配置消息"""
        # 使用正则表达式提取配置信息，支持带引号和不带引号的格式
        url_match = re.search(r'base_url\s*=\s*["\']?([^"\'\n]+)["\']?', message, re.IGNORECASE)
        api_key_match = re.search(r'api_key\s*=\s*["\']?([^"\'\n]+)["\']?', message, re.IGNORECASE)
        model_match = re.search(r'model\s*=\s*["\']?([^"\'\n]+)["\']?', message, re.IGNORECASE)
        
        if url_match and api_key_match and model_match:
            url = url_match.group(1).strip()
            api_key = api_key_match.group(1).strip()
            model = model_match.group(1).strip()
            
            # 确定API类型
            api_type = "openai"
            if "huggingface" in url.lower():
                api_type = "huggingface"
            elif "mock" in model.lower():
                api_type = "mock"
            
            return {
                "api_type": api_type,
                "api_key": api_key,
                "api_base": url,
                "model_name": model
            }
        
        return None

    def send_message(self):
        message = self.input_text.toPlainText().strip()
        if not message:
            return
        
        # 添加用户消息
        self.add_message(message, True)
        
        # 清空输入框
        self.input_text.clear()
        self.input_text.setEnabled(False)
        
        # 先让状态机处理消息（检查特殊命令）
        if self.state_machine.process_message(message, self):
            # 状态机已处理（特殊命令），重新启用输入框
            self.input_text.setEnabled(True)
            self.input_text.setFocus()
            return
        
        # 根据当前状态处理消息
        current_state = self.state_machine.get_current_state()
        
        if current_state == ChatState.CONFIGURING:
            # 配置状态，尝试解析配置信息
            config_info = self.parse_config_message(message)
            if config_info:
                # 显示"正在配置"状态
                self.show_temp_message("连接🧠...")
                
                # 更新LLM客户端配置
                self.llm_client.update_config(
                    config_info["api_type"],
                    config_info["api_key"],
                    config_info["api_base"],
                    config_info["model_name"]
                )
                
                # 测试新配置
                result = self.llm_client.test_connection()
                self.remove_temp_message()
                
                if result["success"]:
                    # 配置成功，保存配置
                    config_to_save = {
                        "api_type": config_info["api_type"],
                        "api_key": config_info["api_key"],
                        "api_base": config_info["api_base"],
                        "model_name": config_info["model_name"]
                    }
                    if config_manager.save_config(config_to_save):
                        self.add_message("💾 配置已保存，下次启动将自动使用", False)
                    
                    # 进入正常状态
                    self.state_machine.change_state(ChatState.NORMAL)
                    self.add_message("✅ API配置成功！现在我可以和你聊天了。你好！我是你的 Emoji 助手，有什么可以帮助你的吗？", False)
                else:
                    # 配置失败，保持配置状态
                    error_msg = result.get("error", "未知错误")
                    self.add_message(f"❌ API配置失败：{error_msg}\n\n请检查配置信息是否正确，格式如下：\n\nbase_url=\"https://ark.cn-beijing.volces.com/api/v3\"\napi_key=41a9d475-45a9-46a2-90bd-bbb75505e9bf\nmodel=\"doubao-seed-1-6-flash-250615\"", False)
                
                self.input_text.setEnabled(True)
                self.input_text.setFocus()
                return
            else:
                # 配置格式不正确
                self.add_message("❌ 配置格式不正确。请按照以下格式输入：\n\nbase_url=\"https://ark.cn-beijing.volces.com/api/v3\"\napi_key=41a9d475-45a9-46a2-90bd-bbb75505e9bf\nmodel=\"doubao-seed-1-6-flash-250615\"", False)
                self.input_text.setEnabled(True)
                self.input_text.setFocus()
                return
        
        elif current_state == ChatState.NORMAL:
            # 正常对话状态
            self.show_temp_message("🤔...")
            
            # 发送消息到LLM
            self.response_thread = ResponseThread(self.llm_client, message)
            self.response_thread.response_received.connect(self.on_response_received)
            self.response_thread.error_occurred.connect(self.on_error_occurred)
            self.response_thread.start()
        
        else:
            # 其他状态，重新启用输入框
            self.input_text.setEnabled(True)
            self.input_text.setFocus()

    def on_response_received(self, message, response):
        # 移除临时状态消息
        self.remove_temp_message()
        
        # 添加AI回复
        self.add_message(response, False)
        
        # 重新启用输入框
        self.input_text.setEnabled(True)
        self.input_text.setFocus()

    def on_error_occurred(self, error_message):
        # 移除临时状态消息
        self.remove_temp_message()
        
        # 显示错误消息和操作提示
        error_text = f"""❌ 对话出现异常：{error_message}

请选择操作：
@检查 - 重新检查连接
@重置 - 清空对话历史
@帮助 - 查看帮助信息"""
        
        self.add_message(error_text, False)
        
        # 对话异常，跳转到错误状态
        self.state_machine.change_state(ChatState.ERROR)
        
        # 重新启用输入框
        self.input_text.setEnabled(True)
        self.input_text.setFocus()

    def closeEvent(self, event):
        if self.response_thread and self.response_thread.isRunning():
            self.response_thread.terminate()
            self.response_thread.wait()
        event.accept()


# 保持向后兼容性
ChatInputDialog = ChatDialog


class ResponseThread(QThread):
    """响应线程"""
    
    response_received = pyqtSignal(str, str)  # message, response
    error_occurred = pyqtSignal(str)  # error_message
    
    def __init__(self, llm_client, message):
        super().__init__()
        self.llm_client = llm_client
        self.message = message
    
    def run(self):
        """运行线程"""
        try:
            response = self.llm_client.get_response(self.message)
            self.response_received.emit(self.message, response)
        except Exception as e:
            self.error_occurred.emit(str(e)) 