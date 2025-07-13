"""
Meditation Plugin - 冥想插件

处理冥想相关、记忆编码、A2B/B2C等意图。
"""

from typing import Dict, Any, Optional
import os
import subprocess
try:
    from .base_plugin import BasePlugin, PluginPriority
except (ImportError, SystemError):
    from brain_agent.plugins.base_plugin import BasePlugin, PluginPriority


class MeditationPlugin(BasePlugin):
    """冥想插件"""
    
    def __init__(self):
        super().__init__(
            name="meditation_plugin",
            description="处理冥想相关、记忆编码、A2B/B2C等用户意图",
            priority=PluginPriority.HIGH
        )
        
        # 插件元数据
        self.metadata.update({
            "tags": ["meditation", "memory", "encoding", "A2B", "B2C"],
            "dependencies": [],
            "config_schema": {
                "memabc_path": {"type": str, "default": "../MemABC"},
                "enable_auto_encoding": {"type": bool, "default": True}
            }
        })
        
        # 冥想相关关键词
        self.meditation_keywords = [
            '冥想', '编码', 'A2B', 'B2C', '记忆', 'meditation', 'encoding',
            '记忆编码', '自动编码', '手动编码'
        ]
        
        # 获取MemABC路径
        self.memabc_path = self._get_memabc_path()
    
    def can_handle(self, intent_data: Dict[str, Any]) -> bool:
        """判断是否能处理该意图"""
        intent_type = intent_data.get("intent_type", "")
        return intent_type == "meditation"
    
    def handle(self, intent_data: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """处理冥想意图"""
        try:
            message = intent_data.get("message", "")
            
            # 分析冥想类型
            meditation_type = self._analyze_meditation_type(message)
            
            # 执行相应的冥想功能
            result = self._execute_meditation(meditation_type, message, context)
            
            return {
                "success": True,
                "meditation_type": meditation_type,
                "result": result,
                "message": message,
                "interaction_type": "meditation"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"冥想处理失败: {str(e)}"
            }
    
    def _analyze_meditation_type(self, message: str) -> str:
        """分析冥想类型"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['A2B', 'a2b', 'a2b编码']):
            return "A2B"
        
        elif any(word in message_lower for word in ['B2C', 'b2c', 'b2c编码']):
            return "B2C"
        
        elif any(word in message_lower for word in ['自动编码', 'auto', '自动']):
            return "auto_encoding"
        
        elif any(word in message_lower for word in ['手动编码', 'manual', '手动']):
            return "manual_encoding"
        
        elif any(word in message_lower for word in ['冥想', 'meditation']):
            return "meditation"
        
        else:
            return "general_meditation"
    
    def _execute_meditation(self, meditation_type: str, message: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """执行冥想功能"""
        if meditation_type == "A2B":
            return self._execute_a2b_encoding()
        
        elif meditation_type == "B2C":
            return self._execute_b2c_encoding()
        
        elif meditation_type == "auto_encoding":
            return self._execute_auto_encoding()
        
        elif meditation_type == "manual_encoding":
            return self._execute_manual_encoding()
        
        elif meditation_type == "meditation":
            return self._execute_meditation_session()
        
        else:
            return self._execute_general_meditation(message)
    
    def _execute_a2b_encoding(self) -> Dict[str, Any]:
        """执行A2B编码"""
        try:
            if not self.memabc_path:
                return {
                    "success": False,
                    "error": "MemABC路径未找到"
                }
            
            a2b_script = os.path.join(self.memabc_path, "a2b.sh")
            if not os.path.exists(a2b_script):
                return {
                    "success": False,
                    "error": "A2B脚本未找到"
                }
            
            # 执行A2B脚本
            result = subprocess.run(
                [a2b_script],
                capture_output=True,
                text=True,
                cwd=self.memabc_path
            )
            
            if result.returncode == 0:
                return {
                    "success": True,
                    "message": "A2B编码执行成功",
                    "output": result.stdout,
                    "type": "A2B"
                }
            else:
                return {
                    "success": False,
                    "error": f"A2B编码执行失败: {result.stderr}",
                    "output": result.stdout
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"A2B编码执行异常: {str(e)}"
            }
    
    def _execute_b2c_encoding(self) -> Dict[str, Any]:
        """执行B2C编码"""
        try:
            if not self.memabc_path:
                return {
                    "success": False,
                    "error": "MemABC路径未找到"
                }
            
            b2c_script = os.path.join(self.memabc_path, "b2c.sh")
            if not os.path.exists(b2c_script):
                return {
                    "success": False,
                    "error": "B2C脚本未找到"
                }
            
            # 执行B2C脚本
            result = subprocess.run(
                [b2c_script],
                capture_output=True,
                text=True,
                cwd=self.memabc_path
            )
            
            if result.returncode == 0:
                return {
                    "success": True,
                    "message": "B2C编码执行成功",
                    "output": result.stdout,
                    "type": "B2C"
                }
            else:
                return {
                    "success": False,
                    "error": f"B2C编码执行失败: {result.stderr}",
                    "output": result.stdout
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"B2C编码执行异常: {str(e)}"
            }
    
    def _execute_auto_encoding(self) -> Dict[str, Any]:
        """执行自动编码"""
        try:
            # 这里可以集成自动编码逻辑
            return {
                "success": True,
                "message": "自动编码功能已启动",
                "type": "auto_encoding",
                "status": "running"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"自动编码执行失败: {str(e)}"
            }
    
    def _execute_manual_encoding(self) -> Dict[str, Any]:
        """执行手动编码"""
        try:
            # 这里可以集成手动编码逻辑
            return {
                "success": True,
                "message": "手动编码模式已启动",
                "type": "manual_encoding",
                "status": "ready"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"手动编码执行失败: {str(e)}"
            }
    
    def _execute_meditation_session(self) -> Dict[str, Any]:
        """执行冥想会话"""
        try:
            return {
                "success": True,
                "message": "冥想会话已开始，请深呼吸，放松身心...",
                "type": "meditation",
                "duration": "10分钟",
                "status": "active"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"冥想会话启动失败: {str(e)}"
            }
    
    def _execute_general_meditation(self, message: str) -> Dict[str, Any]:
        """执行通用冥想功能"""
        try:
            return {
                "success": True,
                "message": "冥想功能已激活，请选择具体的冥想类型",
                "type": "general",
                "available_types": ["A2B", "B2C", "auto_encoding", "manual_encoding", "meditation"],
                "suggestion": "您可以尝试：A2B编码、B2C编码、自动编码、手动编码或冥想会话"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"通用冥想功能执行失败: {str(e)}"
            }
    
    def _get_memabc_path(self) -> str:
        """获取MemABC路径"""
        # 尝试多个可能的路径
        possible_paths = [
            "../MemABC",
            "../../MemABC",
            "emoji_boy/MemABC",
            "MemABC"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return os.path.abspath(path)
        
        return ""
    
    def get_help(self) -> str:
        """获取插件帮助信息"""
        return """
冥想插件帮助：
- A2B编码：执行A2B记忆编码
- B2C编码：执行B2C记忆编码
- 自动编码：启动自动编码模式
- 手动编码：启动手动编码模式
- 冥想会话：开始冥想练习

示例：
- "执行A2B编码"
- "开始B2C编码"
- "启动自动编码"
- "开始冥想"
        """
    
    def get_stats(self) -> Dict[str, Any]:
        """获取插件统计信息"""
        base_stats = super().get_stats()
        base_stats.update({
            "meditation_keywords_count": len(self.meditation_keywords),
            "memabc_path": self.memabc_path,
            "memabc_available": bool(self.memabc_path),
            "plugin_type": "meditation"
        })
        return base_stats 