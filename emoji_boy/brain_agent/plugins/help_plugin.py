"""
Help Plugin - 帮助插件

处理帮助请求、查看说明、了解功能等意图。
"""

from typing import Dict, Any, Optional, List
try:
    from .base_plugin import BasePlugin, PluginPriority
except (ImportError, SystemError):
    from brain_agent.plugins.base_plugin import BasePlugin, PluginPriority


class HelpPlugin(BasePlugin):
    """帮助插件"""
    
    def __init__(self):
        super().__init__(
            name="help_plugin",
            description="处理帮助请求、查看说明、了解功能等用户意图",
            priority=PluginPriority.NORMAL
        )
        
        # 插件元数据
        self.metadata.update({
            "tags": ["help", "support", "guide", "manual"],
            "dependencies": [],
            "config_schema": {
                "show_examples": {"type": bool, "default": True},
                "detailed_help": {"type": bool, "default": False}
            }
        })
        
        # 帮助关键词
        self.help_keywords = [
            '帮助', '说明', '怎么用', '功能', 'help', 'support',
            '指南', '手册', '教程', 'guide', 'manual', 'tutorial'
        ]
        
        # 帮助内容
        self.help_content = self._init_help_content()
    
    def can_handle(self, intent_data: Dict[str, Any]) -> bool:
        """判断是否能处理该意图"""
        intent_type = intent_data.get("intent_type", "")
        return intent_type == "help"
    
    def handle(self, intent_data: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """处理帮助意图"""
        try:
            message = intent_data.get("message", "")
            
            # 分析帮助类型
            help_type = self._analyze_help_type(message)
            
            # 生成帮助内容
            result = self._generate_help_content(help_type, message, context)
            
            return {
                "success": True,
                "help_type": help_type,
                "result": result,
                "message": message,
                "interaction_type": "help"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"帮助处理失败: {str(e)}"
            }
    
    def _analyze_help_type(self, message: str) -> str:
        """分析帮助类型"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['搜索', '查找', 'find', 'search']):
            return "search_help"
        
        elif any(word in message_lower for word in ['聊天', '对话', 'chat', 'conversation']):
            return "chat_help"
        
        elif any(word in message_lower for word in ['配置', '设置', 'config', 'settings']):
            return "config_help"
        
        elif any(word in message_lower for word in ['冥想', '编码', 'meditation', 'encoding']):
            return "meditation_help"
        
        elif any(word in message_lower for word in ['插件', 'plugin']):
            return "plugin_help"
        
        elif any(word in message_lower for word in ['全部', '所有', 'all', 'complete']):
            return "complete_help"
        
        else:
            return "general_help"
    
    def _generate_help_content(self, help_type: str, message: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """生成帮助内容"""
        if help_type == "search_help":
            return self._get_search_help()
        
        elif help_type == "chat_help":
            return self._get_chat_help()
        
        elif help_type == "config_help":
            return self._get_config_help()
        
        elif help_type == "meditation_help":
            return self._get_meditation_help()
        
        elif help_type == "plugin_help":
            return self._get_plugin_help()
        
        elif help_type == "complete_help":
            return self._get_complete_help()
        
        else:
            return self._get_general_help()
    
    def _get_search_help(self) -> Dict[str, Any]:
        """获取搜索帮助"""
        return {
            "title": "搜索功能帮助",
            "description": "搜索功能可以帮助您查找信息、获取资料等",
            "features": [
                "关键词搜索：搜索 [关键词]",
                "问题搜索：如何 [问题]",
                "信息查找：查找 [信息]",
                "最新信息：最新 [主题]"
            ],
            "examples": [
                "搜索Python教程",
                "如何学习机器学习",
                "查找最新科技新闻",
                "什么是人工智能"
            ],
            "tips": [
                "使用具体的关键词可以获得更准确的搜索结果",
                "可以组合多个关键词进行搜索",
                "支持中英文搜索"
            ]
        }
    
    def _get_chat_help(self) -> Dict[str, Any]:
        """获取聊天帮助"""
        return {
            "title": "聊天功能帮助",
            "description": "聊天功能支持日常对话、情感交流等",
            "features": [
                "问候语：你好、嗨、早上好等",
                "告别语：再见、拜拜、晚安等",
                "感谢语：谢谢、感谢等",
                "情感交流：开心、难过、生气等",
                "普通闲聊：日常对话"
            ],
            "examples": [
                "你好！",
                "今天很开心！",
                "谢谢你的帮助",
                "再见！"
            ],
            "tips": [
                "支持emoji表情符号",
                "可以表达各种情感",
                "会给出相应的情感回应"
            ]
        }
    
    def _get_config_help(self) -> Dict[str, Any]:
        """获取配置帮助"""
        return {
            "title": "配置功能帮助",
            "description": "配置功能用于设置系统参数和API配置",
            "features": [
                "API密钥设置：配置API访问密钥",
                "基础URL设置：配置API基础URL",
                "配置查看：显示当前配置信息",
                "配置重置：恢复默认配置",
                "配置备份：备份当前配置"
            ],
            "examples": [
                "设置API密钥为 sk-xxx",
                "设置基础URL为 https://api.example.com",
                "查看当前配置",
                "重置配置"
            ],
            "tips": [
                "API密钥是敏感信息，请妥善保管",
                "修改配置前建议先备份",
                "重置配置会丢失所有自定义设置"
            ]
        }
    
    def _get_meditation_help(self) -> Dict[str, Any]:
        """获取冥想帮助"""
        return {
            "title": "冥想功能帮助",
            "description": "冥想功能支持记忆编码和冥想练习",
            "features": [
                "A2B编码：执行A2B记忆编码",
                "B2C编码：执行B2C记忆编码",
                "自动编码：启动自动编码模式",
                "手动编码：启动手动编码模式",
                "冥想会话：开始冥想练习"
            ],
            "examples": [
                "执行A2B编码",
                "开始B2C编码",
                "启动自动编码",
                "开始冥想"
            ],
            "tips": [
                "编码功能需要MemABC模块支持",
                "冥想会话建议在安静环境中进行",
                "可以结合其他功能使用"
            ]
        }
    
    def _get_plugin_help(self) -> Dict[str, Any]:
        """获取插件帮助"""
        return {
            "title": "插件系统帮助",
            "description": "插件系统是brain_agent的核心架构",
            "features": [
                "模块化设计：每个功能都是独立插件",
                "可扩展性：轻松添加新功能",
                "优先级管理：插件按优先级执行",
                "热插拔：支持动态启用/禁用插件",
                "统计监控：提供详细的执行统计"
            ],
            "available_plugins": [
                "搜索插件 (search_plugin)",
                "聊天插件 (chat_plugin)",
                "配置插件 (config_plugin)",
                "冥想插件 (meditation_plugin)",
                "帮助插件 (help_plugin)"
            ],
            "tips": [
                "插件按优先级自动选择执行",
                "可以查看插件统计信息",
                "支持插件配置和自定义"
            ]
        }
    
    def _get_complete_help(self) -> Dict[str, Any]:
        """获取完整帮助"""
        return {
            "title": "Brain Agent 完整帮助",
            "description": "Brain Agent 是一个智能意图识别和处理系统",
            "system_overview": {
                "name": "Brain Agent",
                "version": "1.0.0",
                "architecture": "插件化架构",
                "core_components": [
                    "IntentEngine - 意图识别引擎",
                    "PluginRegistry - 插件注册表",
                    "Plugins - 技能插件集合"
                ]
            },
            "main_features": [
                "智能意图识别：基于AI的意图分析",
                "插件化处理：模块化的功能处理",
                "缓存优化：提高响应速度",
                "统计监控：详细的执行统计",
                "可扩展性：支持自定义插件"
            ],
            "usage_guide": {
                "basic_usage": "直接输入消息，系统会自动识别意图并处理",
                "advanced_usage": "可以指定具体的功能类型",
                "configuration": "通过配置插件设置系统参数"
            },
            "plugin_details": {
                "search_plugin": "处理搜索相关意图",
                "chat_plugin": "处理聊天和情感交流",
                "config_plugin": "处理配置和设置",
                "meditation_plugin": "处理冥想和记忆编码",
                "help_plugin": "处理帮助请求"
            }
        }
    
    def _get_general_help(self) -> Dict[str, Any]:
        """获取通用帮助"""
        return {
            "title": "Brain Agent 帮助",
            "description": "欢迎使用 Brain Agent！我是您的智能助手。",
            "quick_start": [
                "直接输入消息开始对话",
                "系统会自动识别您的意图",
                "选择合适的插件处理您的请求"
            ],
            "main_functions": [
                "🔍 搜索：查找信息、获取资料",
                "💬 聊天：日常对话、情感交流",
                "⚙️ 配置：设置参数、管理配置",
                "🧘 冥想：记忆编码、冥想练习",
                "❓ 帮助：查看说明、了解功能"
            ],
            "examples": [
                "搜索Python教程",
                "你好！",
                "设置API密钥",
                "开始冥想",
                "帮助"
            ],
            "tips": [
                "使用自然语言与我交流",
                "系统会智能识别您的意图",
                "如有问题可以随时寻求帮助"
            ]
        }
    
    def _init_help_content(self) -> Dict[str, Any]:
        """初始化帮助内容"""
        return {
            "system_info": {
                "name": "Brain Agent",
                "version": "1.0.0",
                "description": "智能意图识别和处理系统"
            },
            "plugins": [
                "search_plugin",
                "chat_plugin", 
                "config_plugin",
                "meditation_plugin",
                "help_plugin"
            ]
        }
    
    def get_help(self) -> str:
        """获取插件帮助信息"""
        return """
帮助插件功能：
- 提供系统功能说明
- 显示使用指南和示例
- 支持分类帮助查询
- 提供完整的系统介绍

使用方法：
- "帮助" - 获取通用帮助
- "搜索帮助" - 查看搜索功能说明
- "聊天帮助" - 查看聊天功能说明
- "配置帮助" - 查看配置功能说明
- "冥想帮助" - 查看冥想功能说明
- "完整帮助" - 查看系统完整说明
        """
    
    def get_stats(self) -> Dict[str, Any]:
        """获取插件统计信息"""
        base_stats = super().get_stats()
        base_stats.update({
            "help_keywords_count": len(self.help_keywords),
            "help_content_sections": len(self.help_content),
            "plugin_type": "help"
        })
        return base_stats 