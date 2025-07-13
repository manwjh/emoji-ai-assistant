"""
Brain Agent - 类脑意图识别与执行系统

一个模仿人脑对外界输入反应模式的智能系统，采用类脑架构设计。
能够像人脑一样识别用户意图，并通过相应的技能模块进行执行。

主要特性：
- 类脑意图识别：模仿人脑的感知和认知过程
- 技能模块系统：类似人脑的技能网络
- 行为模式学习：基于交互历史优化反应
- 自适应执行：根据上下文调整执行策略
- 类脑缓存机制：模拟人脑的记忆和回忆机制

版本: 2.0.0
作者: Emoji AI Assistant Team
"""

__version__ = "2.0.0"
__author__ = "Emoji AI Assistant Team"
__description__ = "类脑意图识别与执行系统 - 模仿人脑的反应模式和行为模式"

# 核心组件
from .intent_engine import IntentEngine, IntentType
from .plugin_registry import PluginRegistry, plugin_registry

# 技能系统（原插件系统）
from .plugins.base_plugin import BasePlugin, PluginPriority
from .plugins.search_plugin import SearchPlugin
from .plugins.chat_plugin import ChatPlugin
from .plugins.config_plugin import ConfigPlugin
from .plugins.help_plugin import HelpPlugin
from .plugins.meditation_plugin import MeditationPlugin
from .plugins.system_plugin import SystemPlugin

# 便捷导入
__all__ = [
    # 核心组件
    "IntentEngine",
    "IntentType", 
    "PluginRegistry",
    "plugin_registry",
    
    # 技能基类
    "BasePlugin",
    "PluginPriority",
    
    # 内置技能
    "SearchPlugin",
    "ChatPlugin", 
    "ConfigPlugin",
    "HelpPlugin",
    "MeditationPlugin",
    "SystemPlugin",
]

# 版本信息
def get_version():
    """获取模块版本信息"""
    return {
        "version": __version__,
        "author": __author__,
        "description": __description__,
        "architecture": "类脑架构",
        "features": [
            "类脑意图识别",
            "技能模块系统", 
            "行为模式学习",
            "自适应执行",
            "类脑缓存机制"
        ]
    }

# 快速启动函数
def create_brain(api_key: str = None, auto_register_skills: bool = True):
    """
    快速创建类脑意图识别系统
    
    Args:
        api_key: API密钥，如果为None则从环境变量获取
        auto_register_skills: 是否自动注册所有内置技能
        
    Returns:
        IntentEngine: 配置好的类脑意图识别系统
    """
    engine = IntentEngine(api_key=api_key)
    
    if auto_register_skills:
        # 自动注册所有内置技能
        skills = [
            SearchPlugin(),
            ChatPlugin(),
            ConfigPlugin(),
            HelpPlugin(),
            MeditationPlugin(),
            SystemPlugin()
        ]
        
        for skill in skills:
            engine.register_plugin(skill)
    
    return engine

# 向后兼容的别名
create_engine = create_brain 