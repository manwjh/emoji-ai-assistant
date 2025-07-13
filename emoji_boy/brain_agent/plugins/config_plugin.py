"""
Config Plugin - 配置插件

处理配置相关、设置API、修改参数等意图。
"""

from typing import Dict, Any, Optional
import os
import json
try:
    from .base_plugin import BasePlugin, PluginPriority
except (ImportError, SystemError):
    from brain_agent.plugins.base_plugin import BasePlugin, PluginPriority


class ConfigPlugin(BasePlugin):
    """配置插件"""
    
    def __init__(self):
        super().__init__(
            name="config_plugin",
            description="处理配置相关、设置API、修改参数等用户意图",
            priority=PluginPriority.HIGH
        )
        
        # 插件元数据
        self.metadata.update({
            "tags": ["config", "settings", "api", "parameter"],
            "dependencies": [],
            "config_schema": {
                "config_file": {"type": str, "default": "config.json"},
                "backup_enabled": {"type": bool, "default": True}
            }
        })
        
        # 配置关键词
        self.config_keywords = [
            '配置', '设置', 'API', 'base_url', 'api_key', '参数',
            'config', 'settings', 'parameter', 'setup'
        ]
        
        # 配置文件路径
        self.config_file = "config.json"
        self.config_data = self._load_config()
    
    def can_handle(self, intent_data: Dict[str, Any]) -> bool:
        """判断是否能处理该意图"""
        intent_type = intent_data.get("intent_type", "")
        return intent_type == "config"
    
    def handle(self, intent_data: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """处理配置意图"""
        try:
            message = intent_data.get("message", "")
            
            # 分析配置类型
            config_type = self._analyze_config_type(message)
            
            # 执行相应的配置操作
            result = self._execute_config_operation(config_type, message, context)
            
            return {
                "success": True,
                "config_type": config_type,
                "result": result,
                "message": message,
                "interaction_type": "config"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"配置处理失败: {str(e)}"
            }
    
    def _analyze_config_type(self, message: str) -> str:
        """分析配置类型"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['api_key', 'apikey', '密钥']):
            return "api_key"
        
        elif any(word in message_lower for word in ['base_url', 'baseurl', '基础url']):
            return "base_url"
        
        elif any(word in message_lower for word in ['查看', '显示', 'show', 'list']):
            return "show_config"
        
        elif any(word in message_lower for word in ['重置', '恢复', 'reset', 'restore']):
            return "reset_config"
        
        elif any(word in message_lower for word in ['备份', 'backup']):
            return "backup_config"
        
        else:
            return "general_config"
    
    def _execute_config_operation(self, config_type: str, message: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """执行配置操作"""
        if config_type == "api_key":
            return self._handle_api_key_config(message)
        
        elif config_type == "base_url":
            return self._handle_base_url_config(message)
        
        elif config_type == "show_config":
            return self._show_config()
        
        elif config_type == "reset_config":
            return self._reset_config()
        
        elif config_type == "backup_config":
            return self._backup_config()
        
        else:
            return self._handle_general_config(message)
    
    def _handle_api_key_config(self, message: str) -> Dict[str, Any]:
        """处理API密钥配置"""
        try:
            # 提取API密钥（这里需要更复杂的解析逻辑）
            api_key = self._extract_api_key(message)
            
            if api_key:
                # 更新配置
                self.config_data["api_key"] = api_key
                self._save_config()
                
                return {
                    "success": True,
                    "message": "API密钥已更新",
                    "type": "api_key",
                    "status": "updated"
                }
            else:
                return {
                    "success": False,
                    "error": "未找到有效的API密钥",
                    "suggestion": "请提供正确的API密钥格式"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"API密钥配置失败: {str(e)}"
            }
    
    def _handle_base_url_config(self, message: str) -> Dict[str, Any]:
        """处理基础URL配置"""
        try:
            # 提取基础URL
            base_url = self._extract_base_url(message)
            
            if base_url:
                # 更新配置
                self.config_data["base_url"] = base_url
                self._save_config()
                
                return {
                    "success": True,
                    "message": "基础URL已更新",
                    "type": "base_url",
                    "status": "updated"
                }
            else:
                return {
                    "success": False,
                    "error": "未找到有效的基础URL",
                    "suggestion": "请提供正确的URL格式"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"基础URL配置失败: {str(e)}"
            }
    
    def _show_config(self) -> Dict[str, Any]:
        """显示配置"""
        try:
            # 隐藏敏感信息
            safe_config = self.config_data.copy()
            if "api_key" in safe_config:
                safe_config["api_key"] = "***" + safe_config["api_key"][-4:] if len(safe_config["api_key"]) > 4 else "***"
            
            return {
                "success": True,
                "message": "当前配置信息",
                "config": safe_config,
                "type": "show_config"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"显示配置失败: {str(e)}"
            }
    
    def _reset_config(self) -> Dict[str, Any]:
        """重置配置"""
        try:
            # 备份当前配置
            if self.metadata["config_schema"]["backup_enabled"]["default"]:
                self._backup_config()
            
            # 重置为默认配置
            self.config_data = self._get_default_config()
            self._save_config()
            
            return {
                "success": True,
                "message": "配置已重置为默认值",
                "type": "reset_config"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"重置配置失败: {str(e)}"
            }
    
    def _backup_config(self) -> Dict[str, Any]:
        """备份配置"""
        try:
            backup_file = f"{self.config_file}.backup"
            
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(self.config_data, f, indent=2, ensure_ascii=False)
            
            return {
                "success": True,
                "message": f"配置已备份到 {backup_file}",
                "backup_file": backup_file,
                "type": "backup_config"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"备份配置失败: {str(e)}"
            }
    
    def _handle_general_config(self, message: str) -> Dict[str, Any]:
        """处理通用配置"""
        try:
            return {
                "success": True,
                "message": "配置功能已激活，请选择具体的配置操作",
                "type": "general",
                "available_operations": [
                    "设置API密钥",
                    "设置基础URL", 
                    "查看配置",
                    "重置配置",
                    "备份配置"
                ],
                "suggestion": "您可以尝试：设置API密钥、设置基础URL、查看配置等"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"通用配置处理失败: {str(e)}"
            }
    
    def _extract_api_key(self, message: str) -> str:
        """提取API密钥"""
        # 简单的API密钥提取逻辑
        # 实际应用中需要更复杂的解析
        import re
        
        # 匹配可能的API密钥格式
        patterns = [
            r'sk-[a-zA-Z0-9]{32,}',
            r'[a-zA-Z0-9]{32,}',
            r'api_key[:\s]+([a-zA-Z0-9]+)',
            r'密钥[:\s]+([a-zA-Z0-9]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                return match.group(1) if len(match.groups()) > 0 else match.group(0)
        
        return ""
    
    def _extract_base_url(self, message: str) -> str:
        """提取基础URL"""
        import re
        
        # 匹配URL格式
        url_pattern = r'https?://[^\s]+'
        match = re.search(url_pattern, message)
        
        if match:
            return match.group(0)
        
        return ""
    
    def _load_config(self) -> Dict[str, Any]:
        """加载配置"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return self._get_default_config()
        except Exception:
            return self._get_default_config()
    
    def _save_config(self):
        """保存配置"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"保存配置失败: {e}")
    
    def _get_default_config(self) -> Dict[str, Any]:
        """获取默认配置"""
        return {
            "api_key": "",
            "base_url": "https://ark.cn-beijing.volces.com/api/v3",
            "model_name": "doubao-1-5-lite-32k-250115",
            "timeout": 10,
            "max_retries": 2
        }
    
    def get_help(self) -> str:
        """获取插件帮助信息"""
        return """
配置插件帮助：
- 设置API密钥：配置API访问密钥
- 设置基础URL：配置API基础URL
- 查看配置：显示当前配置信息
- 重置配置：恢复默认配置
- 备份配置：备份当前配置

示例：
- "设置API密钥为 sk-xxx"
- "设置基础URL为 https://api.example.com"
- "查看当前配置"
- "重置配置"
        """
    
    def get_stats(self) -> Dict[str, Any]:
        """获取插件统计信息"""
        base_stats = super().get_stats()
        base_stats.update({
            "config_keywords_count": len(self.config_keywords),
            "config_file": self.config_file,
            "config_loaded": bool(self.config_data),
            "plugin_type": "config"
        })
        return base_stats 