"""
聊天输入对话框
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTextEdit, 
    QPushButton, QLabel, QProgressBar, QFrame, QApplication,
    QScrollArea, QWidget, QSizePolicy, QPlainTextEdit
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QThread, QSize
from PyQt5.QtGui import QFont, QIcon, QKeyEvent, QTextCursor
import re
from .chat_state_machine import ChatStateMachine, ChatState
from core.config_manager import config_manager
from core.chat_memory import chat_memory


class MessageWidget(QWidget):
    """单条消息组件，支持左/右侧emoji头像+气泡布局，气泡内容自适应高度"""
    def __init__(self, text, is_user=True, avatar_emoji=None, parent=None):
        super().__init__(parent)
        self.text = text
        self.is_user = is_user
        self.avatar_emoji = avatar_emoji or ("😺" if is_user else "🤖")
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(8)

        # 头像
        avatar_label = QLabel(self.avatar_emoji)
        avatar_label.setFixedSize(36, 36)
        avatar_label.setAlignment(Qt.AlignCenter)
        avatar_label.setStyleSheet("""
            QLabel {
                font-size: 28px;
                border-radius: 18px;
                background: transparent;
            }
        """)

        # 气泡内容 QLabel
        self.bubble = QLabel(self.text)
        self.bubble.setWordWrap(True)
        self.bubble.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.bubble.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        self.bubble.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.bubble.setMinimumHeight(28)
        # 区分用户/助手气泡样式
        if self.is_user:
            self.bubble.setStyleSheet("""
                QLabel {
                    background: #1aad19;
                    color: white;
                    border-radius: 16px;
                    padding: 10px 16px;
                    font-size: 15px;
                }
            """)
        else:
            self.bubble.setStyleSheet("""
                QLabel {
                    background: #333333;
                    color: white;
                    border-radius: 16px;
                    padding: 10px 16px;
                    font-size: 15px;
                }
            """)
        self.bubble.adjustSize()

        # 左右布局：用户右侧，助手左侧
        if self.is_user:
            layout.addStretch()
            layout.addWidget(self.bubble)
            layout.addWidget(avatar_label)
        else:
            layout.addWidget(avatar_label)
            layout.addWidget(self.bubble)
            layout.addStretch()

        self.setLayout(layout)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.update_bubble_width()

    def update_bubble_width(self):
        """
        气泡宽度自适应：
        - 单行内容：宽度自适应内容
        - 多行内容：宽度拉满最大宽度
        """
        parent = self.parentWidget()
        if parent is not None:
            parent_width = parent.width()
            avatar_width = 36
            layout_spacing = 8
            margin = 10  # layout左右margin
            max_bubble_width = parent_width - avatar_width - layout_spacing - margin * 2
            if max_bubble_width > 80:
                metrics = self.bubble.fontMetrics()
                text = self.bubble.text()
                single_line_width = metrics.width(text)
                rect = metrics.boundingRect(0, 0, max_bubble_width, 1000, Qt.TextWordWrap, text)
                line_height = metrics.lineSpacing()
                num_lines = rect.height() // line_height
                if single_line_width <= max_bubble_width and '\n' not in text and num_lines <= 1:
                    # 单行，内容宽度自适应
                    bubble_width = single_line_width + 32  # padding: 16*2
                    bubble_width = min(bubble_width, max_bubble_width)
                    self.bubble.setMinimumWidth(0)
                    self.bubble.setMaximumWidth(max_bubble_width)
                    self.bubble.resize(bubble_width, self.bubble.height())
                else:
                    # 多行，宽度拉满
                    self.bubble.setMinimumWidth(max_bubble_width)
                    self.bubble.setMaximumWidth(max_bubble_width)
            self.bubble.adjustSize()

    def resizeEvent(self, event):
        self.update_bubble_width()
        super().resizeEvent(event)


class CustomPlainTextEdit(QPlainTextEdit):
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
        
        # 让主窗口全透明
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background: transparent;")
        
        # 初始化状态机
        self.state_machine = ChatStateMachine()
        self.state_machine.state_changed.connect(self.on_state_changed)
        
        # self.setWindowTitle("Emoji 助手")  # 移除窗口标题
        self.setWindowFlags(
            Qt.FramelessWindowHint |  # 无边框
            Qt.WindowStaysOnTopHint |  # 总在最前
            Qt.Window  # 独立窗口
        )
        self.setModal(False)
        self.resize(500, 600)
        self.init_ui()
        self.setup_styles()

    def paintEvent(self, event):
        # 不绘制任何背景，保持全透明
        pass

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

        # 自定义标题栏（用于关闭按钮）
        title_bar = QFrame()
        title_bar.setStyleSheet("""
            QFrame {
                background: transparent;
                border: none;
            }
        """)
        title_bar.setFixedHeight(40)
        
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(15, 5, 15, 5)
        
        # 标题
        title_label = QLabel("😺 Emoji 助手")
        title_label.setStyleSheet("""
            QLabel {
                color: rgba(255,255,255,0.8);
                font-size: 14px;
                font-weight: bold;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            }
        """)
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        
        # 关闭按钮
        close_button = QPushButton("×")
        close_button.setFixedSize(24, 24)
        close_button.setStyleSheet("""
            QPushButton {
                background: rgba(255,255,255,0.2);
                border: none;
                border-radius: 12px;
                color: rgba(255,255,255,0.8);
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: rgba(255,255,255,0.3);
                color: white;
            }
            QPushButton:pressed {
                background: rgba(255,255,255,0.4);
            }
        """)
        close_button.clicked.connect(self.reject)
        title_layout.addWidget(close_button)
        
        layout.addWidget(title_bar)

        # 主聊天区域 - 类似命令行风格
        chat_container = QFrame()
        chat_container.setStyleSheet("""
            QFrame {
                background: rgba(0,0,0,0.7);
                border: 1px solid rgba(255,255,255,0.2);
                border-radius: 8px;
                margin: 10px;
            }
        """)
        chat_layout = QVBoxLayout(chat_container)
        chat_layout.setContentsMargins(10, 10, 10, 10)
        chat_layout.setSpacing(5)

        # 消息历史区域 - 占据大部分空间
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                background: transparent;
                width: 6px;
                border-radius: 3px;
            }
            QScrollBar::handle:vertical {
                background: rgba(255,255,255,0.3);
                border-radius: 3px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: rgba(255,255,255,0.5);
            }
        """)
        
        self.messages_widget = QWidget()
        self.messages_widget.setStyleSheet("""
            QWidget {
                background: transparent;
                border: none;
            }
        """)
        self.messages_layout = QVBoxLayout(self.messages_widget)
        self.messages_layout.setContentsMargins(5, 5, 5, 5)
        self.messages_layout.setSpacing(3)
        self.messages_layout.addStretch()
        
        self.scroll_area.setWidget(self.messages_widget)
        self.scroll_area.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        chat_layout.addWidget(self.scroll_area)

        # 输入区域 - 固定在底部
        input_frame = QFrame()
        input_frame.setStyleSheet("""
            QFrame {
                background: rgba(255,255,255,0.1);
                border: 1px solid rgba(255,255,255,0.2);
                border-radius: 6px;
                margin-top: 5px;
            }
        """)
        input_frame.setFixedHeight(60)
        
        input_layout = QHBoxLayout(input_frame)
        input_layout.setContentsMargins(10, 8, 10, 8)
        input_layout.setAlignment(Qt.AlignVCenter)
        
        # 输入提示符
        prompt_label = QLabel(">>> ")
        prompt_label.setStyleSheet("""
            QLabel {
                color: rgba(0,255,0,0.8);
                font-family: 'Courier New', monospace;
                font-size: 14px;
                font-weight: bold;
            }
        """)
        input_layout.addWidget(prompt_label)
        
        # 输入框
        self.input_text = CustomPlainTextEdit()
        self.input_text.setPlaceholderText("输入消息... (回车发送，ESC退出)")
        self.input_text.setFont(QFont("Courier New", 13))
        self.input_text.setMinimumHeight(36)
        self.input_text.setMaximumHeight(120)  # 约5行
        self.input_text.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.input_text.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.input_text.setStyleSheet("""
            QPlainTextEdit {
                border: none;
                background: transparent;
                color: rgba(255,255,255,0.9);
                font-family: 'Courier New', monospace;
                font-size: 13px;
                padding: 8px 5px;
            }
            QPlainTextEdit:focus {
                outline: none;
                border: none;
            }
        """)
        # 自动高度调整
        self.input_text.textChanged.connect(self.adjust_input_text_height)
        
        input_layout.addWidget(self.input_text)
        chat_layout.addWidget(input_frame)
        
        layout.addWidget(chat_container)
        
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
                background: rgba(0, 0, 0, 0.8);
                border-radius: 12px;
                border: 1px solid rgba(255,255,255,0.3);
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
                border: none;
                background: transparent;
                color: rgba(255,255,255,0.9);
                font-family: 'Courier New', monospace;
                font-size: 13px;
                padding: 2px 5px;
            }
            QTextEdit:focus {
                outline: none;
                border: none;
            }
            QScrollBar:vertical {
                background: transparent;
                width: 6px;
                border-radius: 3px;
            }
            QScrollBar::handle:vertical {
                background: rgba(255,255,255,0.3);
                border-radius: 3px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: rgba(255,255,255,0.5);
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
            try:
                self.show_temp_message("连接🧠...")
                self.input_text.setEnabled(False)
                
                # 检查API连接
                result = self.llm_client.test_connection()
                self.remove_temp_message()
                
                if result["success"]:
                    self.state_machine.change_state(ChatState.NORMAL)
                    # 让LLM自己生成初始对话
                    self._generate_initial_greeting()
                else:
                    self.state_machine.change_state(ChatState.CONFIGURING)
                    config_message = """抱歉啦，我没法联通主机。小主请检查一下网络，和告诉我令牌配置，格式如下：

base_url="https://ark.cn-beijing.volces.com/api/v3"
api_key=your_api_key_here
model="doubao-seed-1-6-flash-250615"

请按照上面的格式输入您的API配置信息。"""
                    self.add_message(config_message, False)
                
                self.input_text.setEnabled(True)
                self.input_text.setFocus()
            except Exception as e:
                print(f"❌ 状态检查时发生异常: {e}")
                import traceback
                traceback.print_exc()
                self.remove_temp_message()
                self.state_machine.change_state(ChatState.ERROR)
                self.add_message(f"❌ 连接检查失败: {str(e)}", False)
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
    
    def start_a2b_meditation(self):
        """启动A2B冥想"""
        try:
            self.add_message("🧠 开始A2B冥想...", False)
            self.show_temp_message("正在执行A2B编码...")
            
            # 导入A2B编码模块
            import sys
            import os
            sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'MemABC'))
            
            from encoding_a2b import encode_a2b
            
            # 执行A2B编码
            result = encode_a2b()
            
            self.remove_temp_message()
            
            if result:
                self.add_message("✅ A2B冥想完成！记忆已从原始状态编码到处理状态。", False)
            else:
                self.add_message("⚠️ A2B冥想过程中遇到一些问题，请检查日志。", False)
                
        except Exception as e:
            self.remove_temp_message()
            self.add_message(f"❌ A2B冥想失败：{str(e)}", False)
            print(f"A2B冥想异常：{e}")
            import traceback
            traceback.print_exc()
    
    def start_a2c_meditation(self):
        """启动A2C深度冥想"""
        try:
            self.add_message("🧠 开始A2C深度冥想...", False)
            self.show_temp_message("正在执行A2C深度编码...")
            
            # 导入A2C编码模块
            import sys
            import os
            sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'MemABC'))
            
            from encoding_a2c import encode_a2c
            
            # 执行A2C编码
            result = encode_a2c()
            
            self.remove_temp_message()
            
            if result:
                self.add_message("✅ A2C深度冥想完成！重要记忆已编码到深层记忆。", False)
            else:
                self.add_message("⚠️ A2C深度冥想过程中遇到一些问题，请检查日志。", False)
                
        except Exception as e:
            self.remove_temp_message()
            self.add_message(f"❌ A2C深度冥想失败：{str(e)}", False)
            print(f"A2C深度冥想异常：{e}")
            import traceback
            traceback.print_exc()
    
    def start_b2c_meditation(self):
        """启动B2C全面冥想"""
        try:
            self.add_message("🧠 开始B2C全面冥想...", False)
            self.show_temp_message("正在执行B2C全面编码...")
            
            # 导入B2C编码模块
            import sys
            import os
            sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'MemABC'))
            
            from encoding_b2c import encode_b2c
            
            # 执行B2C编码
            result = encode_b2c()
            
            self.remove_temp_message()
            
            if result:
                self.add_message("✅ B2C全面冥想完成！处理记忆已全面编码到深层记忆。", False)
            else:
                self.add_message("⚠️ B2C全面冥想过程中遇到一些问题，请检查日志。", False)
                
        except Exception as e:
            self.remove_temp_message()
            self.add_message(f"❌ B2C全面冥想失败：{str(e)}", False)
            print(f"B2C全面冥想异常：{e}")
            import traceback
            traceback.print_exc()
    
    def _generate_initial_greeting(self):
        """让LLM自己生成初始对话"""
        try:
            # 显示临时状态
            self.show_temp_message("正在生成个性化问候...")
            
            # 创建响应线程来生成初始问候
            self.response_thread = InitialGreetingThread(self.llm_client)
            self.response_thread.response_received.connect(self._on_initial_greeting_received)
            self.response_thread.error_occurred.connect(self._on_initial_greeting_error)
            self.response_thread.start()
            
        except Exception as e:
            print(f"❌ 生成初始问候失败: {e}")
            # 如果生成失败，使用默认问候
            self.remove_temp_message()
            self.add_message("你好呀！我是小喵，很高兴见到你 😺", False)
    
    def _on_initial_greeting_received(self, greeting):
        """接收到初始问候"""
        self.remove_temp_message()
        self.add_message(greeting, False)
    
    def _on_initial_greeting_error(self, error_message):
        """初始问候生成错误"""
        print(f"❌ 初始问候生成错误: {error_message}")
        self.remove_temp_message()
        # 使用默认问候作为备选
        self.add_message("你好呀！我是小喵，很高兴见到你 😺", False)
    

    
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
        
        # 记录用户消息到对话记录
        chat_memory.record_user_message(message)
        
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
                    self.add_message(f"❌ API配置失败：{error_msg}\n\n请检查配置信息是否正确，格式如下：\n\nbase_url=\"https://ark.cn-beijing.volces.com/api/v3\"\napi_key=your_api_key_here\nmodel=\"doubao-seed-1-6-flash-250615\"", False)
                
                self.input_text.setEnabled(True)
                self.input_text.setFocus()
                return
            else:
                # 配置格式不正确
                self.add_message("❌ 配置格式不正确。请按照以下格式输入：\n\nbase_url=\"https://ark.cn-beijing.volces.com/api/v3\"\napi_key=your_api_key_here\nmodel=\"doubao-seed-1-6-flash-250615\"", False)
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
        
        # 记录AI回复到对话记录
        chat_memory.record_ai_message(response)
        
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

    def adjust_input_text_height(self):
        doc = self.input_text.document()
        font_metrics = self.input_text.fontMetrics()
        line_height = font_metrics.lineSpacing()
        num_lines = doc.blockCount()
        padding = 16
        min_height = 36
        max_height = 120
        new_height = min_height + (num_lines - 1) * line_height + padding
        new_height = max(min_height, min(new_height, max_height))
        self.input_text.setFixedHeight(new_height)
        # 移除 setViewportMargins，保持顶部对齐


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
            # 使用意图识别增强的响应方法
            response = self.llm_client.get_response_with_intent(self.message)
            self.response_received.emit(self.message, response)
        except Exception as e:
            self.error_occurred.emit(str(e)) 


class InitialGreetingThread(QThread):
    """初始问候生成线程"""
    
    response_received = pyqtSignal(str)  # greeting
    error_occurred = pyqtSignal(str)  # error_message
    
    def __init__(self, llm_client):
        super().__init__()
        self.llm_client = llm_client
    
    def run(self):
        """运行线程"""
        try:
            # 生成个性化的初始问候
            greeting_prompt = "请根据你的人格特征和记忆，生成一个自然、个性化的开场白来问候用户。要体现你的性格特点，如果有记忆中的用户信息也要体现出来。保持温暖、友好的语气。"
            greeting = self.llm_client.get_response(greeting_prompt)
            self.response_received.emit(greeting)
        except Exception as e:
            self.error_occurred.emit(str(e))