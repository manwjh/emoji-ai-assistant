"""
聊天状态机
"""

from enum import Enum
from typing import Optional, Callable
from PyQt5.QtCore import QObject, pyqtSignal


class ChatState(Enum):
    """聊天状态枚举"""
    INIT = "init"                    # 初始化状态（临时对话）
    CHECKING = "checking"            # 检查连接与令牌（临时对话）
    CONFIGURING = "configuring"      # 配置API状态（临时对话）
    NORMAL = "normal"                # 正常对话状态
    ERROR = "error"                  # 错误状态（临时对话）


class ChatStateMachine(QObject):
    """聊天状态机"""
    
    # 状态变化信号
    state_changed = pyqtSignal(ChatState, ChatState)  # old_state, new_state
    
    def __init__(self):
        super().__init__()
        self.current_state = ChatState.INIT
        self.state_handlers = {}
        self._is_transitioning = False  # 防止状态转换期间的重复调用
        self.setup_state_handlers()
    
    def setup_state_handlers(self):
        """设置状态处理器"""
        self.state_handlers = {
            ChatState.INIT: self.handle_init,
            ChatState.CHECKING: self.handle_checking,
            ChatState.CONFIGURING: self.handle_configuring,
            ChatState.NORMAL: self.handle_normal,
            ChatState.ERROR: self.handle_error
        }
    
    def change_state(self, new_state: ChatState):
        """改变状态"""
        # 防止重复进入同一状态
        if self.current_state == new_state:
            print(f"⚠️ 已在目标状态，忽略重复状态变化: {new_state.value}")
            return
        
        old_state = self.current_state
        self._is_transitioning = True
        
        try:
            self.current_state = new_state
            self.state_changed.emit(old_state, new_state)
            print(f"🔄 状态变化: {old_state.value} → {new_state.value}")
        finally:
            self._is_transitioning = False
    
    def handle_init(self, context):
        """处理初始化状态"""
        print("🚀 进入初始化状态")
        # 自动进入检查状态
        self.change_state(ChatState.CHECKING)
    
    def handle_checking(self, context):
        """处理检查状态"""
        print("🔍 进入检查状态")
        try:
            # 检查API连接
            result = context.llm_client.test_connection()
            if result["success"]:
                self.change_state(ChatState.NORMAL)
            else:
                self.change_state(ChatState.CONFIGURING)
        except Exception as e:
            print(f"❌ 检查状态处理异常: {e}")
            import traceback
            traceback.print_exc()
            self.change_state(ChatState.ERROR)
    
    def handle_configuring(self, context):
        """处理配置状态"""
        print("⚙️ 进入配置状态")
        # 显示配置提示，等待用户输入
    
    def handle_normal(self, context):
        """处理正常对话状态"""
        print("✅ 进入正常对话状态")
        # 正常对话模式
    
    def handle_error(self, context):
        """处理错误状态"""
        print("❌ 进入错误状态")
        # 错误状态下的特殊命令处理已在handle_special_command中实现
    
    def process_message(self, message: str, context) -> bool:
        """
        处理用户消息
        
        Args:
            message: 用户消息
            context: 上下文对象（包含llm_client等）
            
        Returns:
            bool: 是否已处理（True表示已处理，False表示需要继续处理）
        """
        # 检查特殊命令
        if self.is_special_command(message):
            return self.handle_special_command(message, context)
        
        # 根据当前状态处理消息
        handler = self.state_handlers.get(self.current_state)
        if handler:
            handler(context)
        
        return False
    
    def is_special_command(self, message: str) -> bool:
        """检查是否为特殊命令"""
        special_commands = ["@退出", "@检查", "@重置", "@帮助", "@状态"]
        return message.strip() in special_commands
    
    def handle_special_command(self, message: str, context) -> bool:
        """处理特殊命令"""
        command = message.strip()
        
        if command == "@退出":
            print("👋 收到退出命令")
            context.quit_application()
            return True
            
        elif command == "@检查":
            print("🔍 收到检查命令")
            # 清空当前对话历史（如果从错误状态切换）
            if self.current_state == ChatState.ERROR:
                context.clear_temp_dialog_history()
            self.change_state(ChatState.CHECKING)
            return True
            
        elif command == "@重置":
            print("🔄 收到重置命令")
            context.clear_chat_history()
            return True
            
        elif command == "@帮助":
            print("📖 收到帮助命令")
            help_text = """🤖 Emoji 助手帮助信息

特殊命令：
@退出 - 退出程序
@检查 - 检查连接与令牌
@重置 - 重置对话历史
@帮助 - 显示此帮助信息
@状态 - 显示当前连接状态

正常对话：
直接输入消息即可与AI助手对话

配置API：
如果连接失败，请按以下格式输入配置：
base_url="https://ark.cn-beijing.volces.com/api/v3"
api_key=41a9d475-45a9-****-****-bbb75505e9bf
model="doubao-seed-1-6-flash-250615"

配置成功后会自动保存，下次启动无需重新配置。"""
            context.show_help_message(help_text)
            return True
            
        elif command == "@状态":
            print("📊 收到状态命令")
            status = context.llm_client.get_status()
            status_text = f"""📊 当前状态信息

状态: {self.current_state.value}
API类型: {status.get('api_type', '未知')}
模型: {status.get('model_name', '未知')}
API密钥: {'已设置' if status.get('has_api_key') else '未设置'}
对话历史: {status.get('history_length', 0)} 条消息"""
            context.show_status_message(status_text)
            return True
        
        return False
    
    def get_current_state(self) -> ChatState:
        """获取当前状态"""
        return self.current_state
    
    def is_in_normal_state(self) -> bool:
        """是否处于正常对话状态"""
        return self.current_state == ChatState.NORMAL
    
    def is_in_configuring_state(self) -> bool:
        """是否处于配置状态"""
        return self.current_state == ChatState.CONFIGURING
    
    def is_normal_dialog_state(self) -> bool:
        """是否处于正常对话状态"""
        return self.current_state == ChatState.NORMAL
    
    def is_temp_dialog_state(self) -> bool:
        """是否处于临时对话状态"""
        temp_states = [ChatState.INIT, ChatState.CHECKING, ChatState.CONFIGURING, ChatState.ERROR]
        return self.current_state in temp_states
    
    def get_state_type(self) -> str:
        """获取状态类型"""
        if self.current_state == ChatState.NORMAL:
            return "normal"  # 正常对话
        else:
            return "temp"    # 临时对话 