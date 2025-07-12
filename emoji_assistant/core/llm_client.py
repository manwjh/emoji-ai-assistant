"""
大模型接口模块
"""

import os
import json
import time
import requests
from typing import Optional, Dict, Any
import config
from .config_manager import config_manager


class LLMClient:
    """大模型客户端"""
    
    def __init__(self, api_type="openai", model_name=None):
        """
        初始化LLM客户端
        
        Args:
            api_type: API类型 ("openai", "huggingface", "mock")
            model_name: 模型名称
        """
        self.api_type = api_type
        
        # 配置缓存 - 必须在其他方法调用之前初始化
        self._config_cache = None
        self._config_loaded = False
        
        # 现在可以安全调用依赖配置的方法
        self.model_name = model_name or self._get_default_model()
        
        # API配置
        self.api_key = self._get_api_key()
        self.api_base = self._get_api_base()
        
        # 请求配置
        self.timeout = 30
        self.max_retries = 3
        self.retry_delay = 1
        
        # 会话历史
        self.conversation_history = []
        self.max_history = 10
        
        # 系统提示词
        self.system_prompt = self._get_system_prompt()
    
    def _get_default_model(self) -> str:
        """获取默认模型名称"""
        # 优先从配置管理器获取
        saved_config = self._get_cached_config()
        if saved_config and saved_config.get('model_name'):
            return saved_config['model_name']
        
        # 从默认配置获取
        model_map = {
            "openai": "gpt-3.5-turbo",
            "huggingface": "gpt2",
            "mock": "mock-model"
        }
        return model_map.get(self.api_type, "gpt-3.5-turbo")
    
    def _get_api_key(self) -> Optional[str]:
        """获取API密钥"""
        # 优先从配置管理器获取
        saved_config = self._get_cached_config()
        if saved_config and saved_config.get('api_key'):
            return saved_config['api_key']
        
        # 从环境变量获取
        if self.api_type == "openai":
            return os.getenv("OPENAI_API_KEY") or config.OPENAI_API_KEY
        elif self.api_type == "huggingface":
            return os.getenv("HUGGINGFACE_API_KEY") or config.HUGGINGFACE_API_KEY
        return None
    
    def _get_api_base(self) -> str:
        """获取API基础URL"""
        # 优先从配置管理器获取
        saved_config = self._get_cached_config()
        if saved_config and saved_config.get('api_base'):
            return saved_config['api_base']
        
        # 从默认配置获取
        if self.api_type == "openai":
            return "https://api.openai.com/v1"
        elif self.api_type == "huggingface":
            return "https://api-inference.huggingface.co"
        return ""
    
    def _get_cached_config(self) -> Optional[Dict[str, str]]:
        """获取缓存的配置"""
        if not self._config_loaded:
            self._config_cache = config_manager.load_config()
            self._config_loaded = True
        return self._config_cache
    
    def _get_system_prompt(self) -> str:
        """获取系统提示词"""
        return """你是一个可爱的Emoji虚拟人助手，名字叫小喵。你的性格特点：
1. 友善、温暖、充满爱心
2. 说话简洁明了，经常使用emoji表情
3. 会安慰人，给出积极正面的建议
4. 回答要实用且有趣
5. 保持对话的连贯性和友好性

请用轻松愉快的语气回答用户的问题，并在适当的时候使用emoji表情。"""
    
    def get_response(self, message: str) -> str:
        """
        获取模型响应
        
        Args:
            message: 用户消息
            
        Returns:
            模型响应文本
        """
        try:
            if self.api_type == "openai":
                return self._call_openai_api(message)
            elif self.api_type == "huggingface":
                return self._call_huggingface_api(message)
            elif self.api_type == "mock":
                return self._get_mock_response(message)
            else:
                raise ValueError(f"不支持的API类型: {self.api_type}")
                
        except Exception as e:
            print(f"❌ 获取模型响应失败: {e}")
            return self._get_fallback_response(message)
    
    def _call_openai_api(self, message: str) -> str:
        """调用OpenAI API"""
        if not self.api_key:
            raise ValueError("OpenAI API密钥未设置")
        
        # 构建消息列表
        messages = [{"role": "system", "content": self.system_prompt}]
        
        # 添加历史对话
        for hist in self.conversation_history[-self.max_history:]:
            messages.append(hist)
        
        # 添加当前消息
        messages.append({"role": "user", "content": message})
        
        # 构建请求数据
        data = {
            "model": self.model_name,
            "messages": messages,
            "max_tokens": 500,
            "temperature": 0.7,
            "top_p": 0.9
        }
        
        # 发送请求
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        for attempt in range(self.max_retries):
            try:
                response = requests.post(
                    f"{self.api_base}/chat/completions",
                    headers=headers,
                    json=data,
                    timeout=self.timeout
                )
                response.raise_for_status()
                
                result = response.json()
                assistant_message = result["choices"][0]["message"]["content"]
                
                # 更新对话历史
                self._update_conversation_history(message, assistant_message)
                
                return assistant_message
                
            except requests.exceptions.RequestException as e:
                if attempt == self.max_retries - 1:
                    raise e
                time.sleep(self.retry_delay * (attempt + 1))
    
    def _call_huggingface_api(self, message: str) -> str:
        """调用HuggingFace API"""
        if not self.api_key:
            raise ValueError("HuggingFace API密钥未设置")
        
        # 构建提示词
        prompt = f"{self.system_prompt}\n\n用户: {message}\n小喵:"
        
        # 构建请求数据
        data = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 200,
                "temperature": 0.7,
                "top_p": 0.9,
                "do_sample": True
            }
        }
        
        # 发送请求
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        for attempt in range(self.max_retries):
            try:
                response = requests.post(
                    f"{self.api_base}/models/{self.model_name}",
                    headers=headers,
                    json=data,
                    timeout=self.timeout
                )
                response.raise_for_status()
                
                result = response.json()
                assistant_message = result[0]["generated_text"]
                
                # 提取回复部分
                if "小喵:" in assistant_message:
                    assistant_message = assistant_message.split("小喵:")[-1].strip()
                
                # 更新对话历史
                self._update_conversation_history(message, assistant_message)
                
                return assistant_message
                
            except requests.exceptions.RequestException as e:
                if attempt == self.max_retries - 1:
                    raise e
                time.sleep(self.retry_delay * (attempt + 1))
    
    def _get_mock_response(self, message: str) -> str:
        """获取模拟响应"""
        import random
        
        # 模拟响应模板
        responses = [
            "喵~ 我理解你的想法呢 😊",
            "这个问题很有趣，让我想想... 🤔",
            "你说得对，我也这么觉得！ 👍",
            "哈哈，你真是太可爱了 😄",
            "我在这里陪着你哦 💕",
            "让我们一起想想办法吧 💡",
            "你说得很棒呢！ 🌟",
            "我完全理解你的感受 🤗",
            "这确实是个好问题 ✨",
            "你的想法很有创意呢 🎨"
        ]
        
        # 根据消息内容选择响应
        if any(word in message.lower() for word in ['你好', 'hello', 'hi']):
            return "你好呀！我是小喵，很高兴见到你 😺"
        elif any(word in message.lower() for word in ['谢谢', '感谢', 'thank']):
            return "不客气！能帮到你是我的荣幸 💖"
        elif any(word in message.lower() for word in ['再见', '拜拜', 'bye']):
            return "再见啦！记得想我哦 👋"
        else:
            return random.choice(responses)
    
    def _get_fallback_response(self, message: str) -> str:
        """获取备用响应"""
        return "抱歉，我现在有点小问题，稍后再和你聊天吧 😅"
    
    def _update_conversation_history(self, user_message: str, assistant_message: str):
        """更新对话历史"""
        self.conversation_history.extend([
            {"role": "user", "content": user_message},
            {"role": "assistant", "content": assistant_message}
        ])
        
        # 保持历史记录在限制范围内
        if len(self.conversation_history) > self.max_history * 2:
            self.conversation_history = self.conversation_history[-self.max_history * 2:]
    
    def clear_history(self):
        """清空对话历史"""
        self.conversation_history.clear()
    
    def set_system_prompt(self, prompt: str):
        """设置系统提示词"""
        self.system_prompt = prompt
    
    def get_status(self) -> Dict[str, Any]:
        """获取客户端状态"""
        return {
            "api_type": self.api_type,
            "model_name": self.model_name,
            "has_api_key": bool(self.api_key),
            "history_length": len(self.conversation_history),
            "max_history": self.max_history
        }
    
    def test_connection(self) -> Dict[str, Any]:
        """
        测试API连接
        
        Returns:
            包含连接状态的字典
        """
        result = {
            "success": False,
            "error": None,
            "details": {}
        }
        
        try:
            # 检查基本配置
            if not self.api_key:
                result["error"] = "API密钥未设置"
                return result
            
            if not self.api_base:
                result["error"] = "API基础URL未设置"
                return result
            
            # 根据API类型进行测试
            if self.api_type == "openai":
                result = self._test_openai_connection()
            elif self.api_type == "huggingface":
                result = self._test_huggingface_connection()
            elif self.api_type == "mock":
                result = {
                    "success": True,
                    "error": None,
                    "details": {"message": "Mock模式无需连接测试"}
                }
            else:
                result["error"] = f"不支持的API类型: {self.api_type}"
                
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    def _test_openai_connection(self) -> Dict[str, Any]:
        """测试OpenAI API连接"""
        result = {
            "success": False,
            "error": None,
            "details": {}
        }
        
        try:
            # 发送一个简单的测试请求
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": self.model_name,
                "messages": [{"role": "user", "content": "Hello"}],
                "max_tokens": 10
            }
            
            response = requests.post(
                f"{self.api_base}/chat/completions",
                headers=headers,
                json=data,
                timeout=10
            )
            
            if response.status_code == 200:
                result["success"] = True
                result["details"] = {"status_code": response.status_code}
            else:
                result["error"] = f"API请求失败，状态码: {response.status_code}"
                result["details"] = {"status_code": response.status_code, "response": response.text}
                
        except requests.exceptions.RequestException as e:
            result["error"] = f"网络请求失败: {str(e)}"
        except Exception as e:
            result["error"] = f"连接测试失败: {str(e)}"
        
        return result
    
    def _test_huggingface_connection(self) -> Dict[str, Any]:
        """测试HuggingFace API连接"""
        result = {
            "success": False,
            "error": None,
            "details": {}
        }
        
        try:
            # 发送一个简单的测试请求
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "inputs": "Hello",
                "parameters": {
                    "max_new_tokens": 10,
                    "temperature": 0.7
                }
            }
            
            response = requests.post(
                f"{self.api_base}/models/{self.model_name}",
                headers=headers,
                json=data,
                timeout=10
            )
            
            if response.status_code == 200:
                result["success"] = True
                result["details"] = {"status_code": response.status_code}
            else:
                result["error"] = f"API请求失败，状态码: {response.status_code}"
                result["details"] = {"status_code": response.status_code, "response": response.text}
                
        except requests.exceptions.RequestException as e:
            result["error"] = f"网络请求失败: {str(e)}"
        except Exception as e:
            result["error"] = f"连接测试失败: {str(e)}"
        
        return result
    
    def update_config(self, api_type: str, api_key: str, api_base: str, model_name: str):
        """
        更新API配置
        
        Args:
            api_type: API类型
            api_key: API密钥
            api_base: API基础URL
            model_name: 模型名称
        """
        self.api_type = api_type
        self.api_key = api_key
        self.api_base = api_base
        self.model_name = model_name
        
        # 清除配置缓存，强制重新加载
        self._config_cache = None
        self._config_loaded = False 