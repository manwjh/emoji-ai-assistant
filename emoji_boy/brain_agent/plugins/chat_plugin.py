"""
Chat Plugin - 聊天插件

处理普通聊天、问候、情感交流等意图。
"""

from typing import Dict, Any, Optional
try:
    from .base_plugin import BasePlugin, PluginPriority
except (ImportError, SystemError):
    from brain_agent.plugins.base_plugin import BasePlugin, PluginPriority
import random


class ChatPlugin(BasePlugin):
    """聊天插件"""
    
    def __init__(self):
        super().__init__(
            name="chat_plugin",
            description="处理普通聊天、问候、情感交流等用户意图",
            priority=PluginPriority.NORMAL
        )
        
        # 插件元数据
        self.metadata.update({
            "tags": ["chat", "conversation", "greeting", "emotion"],
            "dependencies": [],
            "config_schema": {
                "enable_emotion": {"type": bool, "default": True},
                "response_style": {"type": str, "default": "friendly"}
            }
        })
        
        # 问候语模板
        self.greetings = {
            "hello": [
                "你好！😊 很高兴见到你！",
                "嗨！👋 今天过得怎么样？",
                "你好呀！✨ 有什么我可以帮助你的吗？"
            ],
            "goodbye": [
                "再见！👋 期待下次聊天！",
                "拜拜！😊 记得保持好心情哦！",
                "下次见！✨ 祝你有美好的一天！"
            ],
            "thanks": [
                "不客气！😊 很高兴能帮到你！",
                "应该的！✨ 有什么需要随时找我！",
                "不用谢！👋 为你服务是我的荣幸！"
            ]
        }
        
        # 情感回应模板
        self.emotion_responses = {
            "happy": [
                "看到你开心我也很开心！😄",
                "太棒了！继续保持好心情！✨",
                "你的快乐感染了我！😊"
            ],
            "sad": [
                "别难过，一切都会好起来的！🤗",
                "我在这里陪着你，有什么想说的吗？💕",
                "困难是暂时的，你一定能度过难关！💪"
            ],
            "angry": [
                "冷静一下，深呼吸！😌",
                "我理解你的感受，需要聊聊吗？🤗",
                "生气对身体不好，让我们一起想办法！💪"
            ]
        }
        
        # 闲聊回应
        self.casual_responses = [
            "嗯嗯，我在听！😊",
            "很有趣呢！继续说说看！✨",
            "哈哈，你说得对！😄",
            "确实如此！👌",
            "我明白你的意思！👍"
        ]
    
    def can_handle(self, intent_data: Dict[str, Any]) -> bool:
        """判断是否能处理该意图"""
        intent_type = intent_data.get("intent_type", "")
        return intent_type == "chat"
    
    def handle(self, intent_data: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """处理聊天意图"""
        try:
            message = intent_data.get("message", "")
            
            # 分析消息类型
            message_type = self._analyze_message_type(message)
            
            # 生成回应
            response = self._generate_response(message, message_type, context)
            
            return {
                "success": True,
                "response": response,
                "message_type": message_type,
                "emotion": self._detect_emotion(message),
                "interaction_type": "chat"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"聊天处理失败: {str(e)}"
            }
    
    def _analyze_message_type(self, message: str) -> str:
        """分析消息类型"""
        message_lower = message.lower()
        
        # 问候语检测
        if any(word in message_lower for word in ['你好', '嗨', 'hello', 'hi', '早上好', '下午好', '晚上好']):
            return "greeting"
        
        # 告别语检测
        if any(word in message_lower for word in ['再见', '拜拜', 'goodbye', 'bye', '晚安']):
            return "goodbye"
        
        # 感谢语检测
        if any(word in message_lower for word in ['谢谢', '感谢', 'thank', 'thanks']):
            return "thanks"
        
        # 情感表达检测
        if any(word in message_lower for word in ['开心', '高兴', '快乐', 'happy', '😊', '😄', '😍']):
            return "emotion_happy"
        
        if any(word in message_lower for word in ['难过', '伤心', '悲伤', 'sad', '😢', '😭', '😔']):
            return "emotion_sad"
        
        if any(word in message_lower for word in ['生气', '愤怒', 'angry', '😠', '😡', '💢']):
            return "emotion_angry"
        
        # 默认闲聊
        return "casual"
    
    def _detect_emotion(self, message: str) -> str:
        """检测情感"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['开心', '高兴', '快乐', 'happy', '😊', '😄', '😍']):
            return "happy"
        elif any(word in message_lower for word in ['难过', '伤心', '悲伤', 'sad', '😢', '😭', '😔']):
            return "sad"
        elif any(word in message_lower for word in ['生气', '愤怒', 'angry', '😠', '😡', '💢']):
            return "angry"
        else:
            return "neutral"
    
    def _generate_response(self, message: str, message_type: str, context: Dict[str, Any] = None) -> str:
        """生成回应"""
        if message_type == "greeting":
            return random.choice(self.greetings["hello"])
        
        elif message_type == "goodbye":
            return random.choice(self.greetings["goodbye"])
        
        elif message_type == "thanks":
            return random.choice(self.greetings["thanks"])
        
        elif message_type == "emotion_happy":
            return random.choice(self.emotion_responses["happy"])
        
        elif message_type == "emotion_sad":
            return random.choice(self.emotion_responses["sad"])
        
        elif message_type == "emotion_angry":
            return random.choice(self.emotion_responses["angry"])
        
        else:
            # 闲聊回应
            return random.choice(self.casual_responses)
    
    def get_help(self) -> str:
        """获取插件帮助信息"""
        return """
聊天插件帮助：
- 支持问候：你好、嗨、早上好等
- 支持告别：再见、拜拜、晚安等
- 支持感谢：谢谢、感谢等
- 支持情感交流：开心、难过、生气等
- 支持普通闲聊

示例：
- "你好！"
- "今天很开心！"
- "谢谢你的帮助"
- "再见！"
        """
    
    def get_stats(self) -> Dict[str, Any]:
        """获取插件统计信息"""
        base_stats = super().get_stats()
        base_stats.update({
            "greeting_templates": len(self.greetings),
            "emotion_responses": len(self.emotion_responses),
            "casual_responses": len(self.casual_responses),
            "plugin_type": "chat"
        })
        return base_stats 