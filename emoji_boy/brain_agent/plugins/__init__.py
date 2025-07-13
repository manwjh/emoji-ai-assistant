"""
Brain Agent Plugins - 插件系统

提供各种功能插件，用于处理不同类型的用户意图。
所有插件都继承自BasePlugin基类，遵循统一的接口规范。
"""

# 插件基类
from .base_plugin import BasePlugin, PluginPriority

# 内置插件
from .search_plugin import SearchPlugin
from .chat_plugin import ChatPlugin
from .config_plugin import ConfigPlugin
from .help_plugin import HelpPlugin
from .meditation_plugin import MeditationPlugin
from .system_plugin import SystemPlugin

# 导出所有插件
__all__ = [
    # 基类
    "BasePlugin",
    "PluginPriority",
    
    # 内置插件
    "SearchPlugin",
    "ChatPlugin", 
    "ConfigPlugin",
    "HelpPlugin",
    "MeditationPlugin",
    "SystemPlugin",
]

# 插件信息
PLUGIN_INFO = {
    "search": {
        "name": "SearchPlugin",
        "description": "处理搜索相关的用户意图",
        "priority": "HIGH",
        "intent_types": ["search"]
    },
    "chat": {
        "name": "ChatPlugin", 
        "description": "处理普通聊天、问候、情感交流",
        "priority": "NORMAL",
        "intent_types": ["chat"]
    },
    "config": {
        "name": "ConfigPlugin",
        "description": "处理配置相关、设置API、修改参数",
        "priority": "HIGH", 
        "intent_types": ["config"]
    },
    "help": {
        "name": "HelpPlugin",
        "description": "处理帮助请求、查看说明、了解功能",
        "priority": "NORMAL",
        "intent_types": ["help"]
    },
    "meditation": {
        "name": "MeditationPlugin",
        "description": "处理冥想相关、记忆编码、A2B/B2C",
        "priority": "HIGH",
        "intent_types": ["meditation"]
    },
    "system": {
        "name": "SystemPlugin",
        "description": "处理系统相关查询和命令执行",
        "priority": "HIGH",
        "intent_types": ["system"]
    }
}

def get_all_plugins():
    """
    获取所有内置插件实例
    
    Returns:
        List[BasePlugin]: 插件实例列表
    """
    return [
        SearchPlugin(),
        ChatPlugin(),
        ConfigPlugin(),
        HelpPlugin(),
        MeditationPlugin(),
        SystemPlugin()
    ]

def get_plugin_by_name(name: str):
    """
    根据名称获取插件实例
    
    Args:
        name: 插件名称
        
    Returns:
        BasePlugin: 插件实例，如果不存在返回None
    """
    plugin_map = {
        "search": SearchPlugin,
        "chat": ChatPlugin,
        "config": ConfigPlugin,
        "help": HelpPlugin,
        "meditation": MeditationPlugin,
        "system": SystemPlugin
    }
    
    plugin_class = plugin_map.get(name.lower())
    if plugin_class:
        return plugin_class()
    
    return None

def get_plugin_info():
    """
    获取所有插件信息
    
    Returns:
        Dict: 插件信息字典
    """
    return PLUGIN_INFO.copy() 