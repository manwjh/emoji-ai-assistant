"""
Base Plugin - 插件基类

所有技能插件都应该继承这个基类，实现统一的接口。
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from enum import Enum


class PluginPriority(Enum):
    """插件优先级"""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


class BasePlugin(ABC):
    """插件基类"""
    
    def __init__(self, name: str, description: str = "", priority: PluginPriority = PluginPriority.NORMAL):
        """
        初始化插件
        
        Args:
            name: 插件名称
            description: 插件描述
            priority: 插件优先级
        """
        self.name = name
        self.description = description
        self.priority = priority
        self.enabled = True
        self.version = "1.0.0"
        
        # 插件元数据
        self.metadata = {
            "author": "Emoji Boy Team",
            "tags": [],
            "dependencies": [],
            "config_schema": {}
        }
    
    @abstractmethod
    def can_handle(self, intent_data: Dict[str, Any]) -> bool:
        """
        判断插件是否能处理该意图
        
        Args:
            intent_data: 意图识别结果
            
        Returns:
            bool: 是否能处理
        """
        pass
    
    @abstractmethod
    def handle(self, intent_data: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        处理意图
        
        Args:
            intent_data: 意图识别结果
            context: 上下文信息
            
        Returns:
            Dict: 处理结果
        """
        pass
    
    def get_help(self) -> str:
        """获取插件帮助信息"""
        return f"{self.name}: {self.description}"
    
    def get_config_schema(self) -> Dict[str, Any]:
        """获取配置模式"""
        return self.metadata.get("config_schema", {})
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """验证配置"""
        schema = self.get_config_schema()
        # 简单的配置验证逻辑
        for key, value in config.items():
            if key in schema:
                expected_type = schema[key].get("type")
                if expected_type and not isinstance(value, expected_type):
                    return False
        return True
    
    def enable(self):
        """启用插件"""
        self.enabled = True
    
    def disable(self):
        """禁用插件"""
        self.enabled = False
    
    def is_enabled(self) -> bool:
        """检查插件是否启用"""
        return self.enabled
    
    def get_stats(self) -> Dict[str, Any]:
        """获取插件统计信息"""
        return {
            "name": self.name,
            "enabled": self.enabled,
            "priority": self.priority.value,
            "version": self.version
        }
    
    def __str__(self) -> str:
        return f"{self.name} (v{self.version})"
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} name='{self.name}' enabled={self.enabled}>" 