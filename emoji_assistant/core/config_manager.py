"""
配置管理模块
"""

import os
import json
from typing import Dict, Optional


class ConfigManager:
    """配置管理器"""
    
    def __init__(self, config_file="api_config.json"):
        self.config_file = config_file
        self.config_dir = os.path.expanduser("~/.emoji_assistant")
        self.config_path = os.path.join(self.config_dir, config_file)
        self._config_cache = None
        self._config_checked = False
        self.ensure_config_dir()
    
    def ensure_config_dir(self):
        """确保配置目录存在"""
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)
    
    def save_config(self, config: Dict[str, str]):
        """
        保存配置到文件
        
        Args:
            config: 配置字典，包含 api_type, api_key, api_base, model_name
        """
        try:
            # 保存到文件
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            
            # 更新缓存
            self._config_cache = config.copy()
            
            # 设置环境变量
            os.environ['EMOJI_API_TYPE'] = config.get('api_type', '')
            os.environ['EMOJI_API_KEY'] = config.get('api_key', '')
            os.environ['EMOJI_API_BASE'] = config.get('api_base', '')
            os.environ['EMOJI_MODEL_NAME'] = config.get('model_name', '')
            
            print(f"✅ 配置已保存到: {self.config_path}")
            return True
        except Exception as e:
            print(f"❌ 保存配置失败: {e}")
            return False
    
    def load_config(self) -> Optional[Dict[str, str]]:
        """
        从文件加载配置（带缓存）
        
        Returns:
            配置字典或None
        """
        # 如果已经检查过且缓存为空，直接返回None
        if self._config_checked and self._config_cache is None:
            return None
        
        # 如果缓存存在，直接返回
        if self._config_cache is not None:
            return self._config_cache
        
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                self._config_cache = config
                print(f"✅ 配置已从文件加载: {self.config_path}")
                return config
            else:
                # 只在第一次检查时打印消息
                if not self._config_checked:
                    print("📝 配置文件不存在，将使用环境变量")
                self._config_checked = True
                return None
        except Exception as e:
            print(f"❌ 加载配置失败: {e}")
            self._config_checked = True
            return None
    
    def get_config_from_env(self) -> Dict[str, str]:
        """
        从环境变量获取配置
        
        Returns:
            配置字典
        """
        return {
            'api_type': os.environ.get('EMOJI_API_TYPE', ''),
            'api_key': os.environ.get('EMOJI_API_KEY', ''),
            'api_base': os.environ.get('EMOJI_API_BASE', ''),
            'model_name': os.environ.get('EMOJI_MODEL_NAME', '')
        }
    
    def has_valid_config(self) -> bool:
        """
        检查是否有有效的配置
        
        Returns:
            是否有有效配置
        """
        # 先尝试从文件加载
        file_config = self.load_config()
        if file_config and all(file_config.values()):
            return True
        
        # 再检查环境变量
        env_config = self.get_config_from_env()
        return all(env_config.values())
    
    def clear_config(self):
        """清除配置"""
        try:
            if os.path.exists(self.config_path):
                os.remove(self.config_path)
            
            # 清除缓存
            self._config_cache = None
            self._config_checked = False
            
            # 清除环境变量
            for key in ['EMOJI_API_TYPE', 'EMOJI_API_KEY', 'EMOJI_API_BASE', 'EMOJI_MODEL_NAME']:
                if key in os.environ:
                    del os.environ[key]
            
            print("✅ 配置已清除")
        except Exception as e:
            print(f"❌ 清除配置失败: {e}")


# 全局配置管理器实例
config_manager = ConfigManager() 