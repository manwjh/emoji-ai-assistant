"""
按照人类行为模式方式，构建一个全新的意图识别模块
	•	动机系统（我为什么要做这件事？）
	•	感知系统（我意识到对方在说什么？）
	•	记忆系统（我有没有遇到过类似的事情？）
	•	执行控制系统（我有没有能力去完成？）"""





import os
import json
import time
import requests
from typing import Dict, Any, List, Optional
from enum import Enum
import re


class IntentType(Enum):
    """意图类型枚举"""
    SEARCH = "search"           # 搜索意图
    CHAT = "chat"              # 普通聊天
    CONFIG = "config"          # 配置相关
    HELP = "help"              # 帮助请求
    MEDITATION = "meditation"  # 冥想相关
    UNKNOWN = "unknown"        # 未知意图


class IntentRecognition:
    """用户对话意图识别器"""
    
    def __init__(self, api_key: str = None, api_base: str = None):
        """
        初始化意图识别器
        
        Args:
            api_key: API密钥
            api_base: API基础URL
        """
        # 配置
        self.api_key = api_key or os.getenv("DOUBAO_API_KEY")
        self.api_base = api_base or "https://ark.cn-beijing.volces.com/api/v3"
        self.model_name = "doubao-1-5-lite-32k-250115"
        
        # 请求配置
        self.timeout = 10
        self.max_retries = 2
        self.retry_delay = 1
        
        # 意图识别提示词
        self.intent_prompt = self._get_intent_prompt()
        
        # 缓存配置
        self.cache = {}
        self.cache_size = 100
        self.cache_ttl = 300  # 5分钟缓存
        
        # 统计信息
        self.stats = {
            "total_requests": 0,
            "cache_hits": 0,
            "successful_recognitions": 0,
            "failed_recognitions": 0
        }
    
    def _get_intent_prompt(self) -> str:
        """获取意图识别提示词"""
        return """你是一个专业的用户意图识别助手。请分析用户输入的消息，识别其意图类型。

意图类型说明：
1. SEARCH - 用户需要搜索信息、查找资料、获取最新信息等
2. CHAT - 普通聊天、问候、闲聊、情感交流等
3. CONFIG - 配置相关、设置API、修改参数等
4. HELP - 请求帮助、查看说明、了解功能等
5. MEDITATION - 冥想相关、记忆编码、A2B/B2C等
6. UNKNOWN - 无法识别的意图

识别规则：
- 包含"搜索"、"查找"、"找"、"帮我找"等关键词 → SEARCH
- 包含"如何"、"怎么"、"什么是"、"最新"、"新闻"等 → SEARCH
- 包含"配置"、"设置"、"API"、"base_url"等 → CONFIG
- 包含"帮助"、"说明"、"怎么用"、"功能"等 → HELP
- 包含"冥想"、"编码"、"A2B"、"B2C"等 → MEDITATION
- 问候语、闲聊、情感表达 → CHAT

请只返回意图类型（SEARCH/CHAT/CONFIG/HELP/MEDITATION/UNKNOWN），不要包含其他内容。"""
    
    def recognize_intent(self, message: str) -> Dict[str, Any]:
        """
        识别用户消息的意图
        
        Args:
            message: 用户消息
            
        Returns:
            包含意图信息的字典
        """
        try:
            # 检查缓存
            cache_key = self._get_cache_key(message)
            if cache_key in self.cache:
                cached_result = self.cache[cache_key]
                if time.time() - cached_result['timestamp'] < self.cache_ttl:
                    self.stats["cache_hits"] += 1
                    return cached_result['result']
                else:
                    # 缓存过期，删除
                    del self.cache[cache_key]
            
            self.stats["total_requests"] += 1
            
            # 调用API进行意图识别
            intent_result = self._call_intent_api(message)
            
            # 处理结果
            result = self._process_intent_result(message, intent_result)
            
            # 缓存结果
            self._cache_result(cache_key, result)
            
            self.stats["successful_recognitions"] += 1
            return result
            
        except Exception as e:
            self.stats["failed_recognitions"] += 1
            print(f"❌ 意图识别失败: {e}")
            return self._get_fallback_result(message)
    
    def _call_intent_api(self, message: str) -> str:
        """调用意图识别API"""
        if not self.api_key:
            raise ValueError("API密钥未设置")
        
        # 构建请求数据
        data = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": self.intent_prompt},
                {"role": "user", "content": message}
            ],
            "max_tokens": 10,
            "temperature": 0.1,  # 低温度，提高一致性
            "top_p": 0.9
        }
        
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
                intent_text = result["choices"][0]["message"]["content"].strip()
                return intent_text
                
            except requests.exceptions.RequestException as e:
                if attempt == self.max_retries - 1:
                    raise e
                time.sleep(self.retry_delay * (attempt + 1))
    
    def _process_intent_result(self, message: str, intent_text: str) -> Dict[str, Any]:
        """处理意图识别结果"""
        # 解析意图类型
        intent_type = self._parse_intent_type(intent_text)
        
        # 提取搜索查询（如果是搜索意图）
        search_query = None
        if intent_type == IntentType.SEARCH:
            search_query = self._extract_search_query(message)
        
        return {
            "intent_type": intent_type.value,
            "confidence": self._calculate_confidence(message, intent_type),
            "search_query": search_query,
            "message": message,
            "timestamp": time.time()
        }
    
    def _parse_intent_type(self, intent_text: str) -> IntentType:
        """解析意图类型"""
        intent_text = intent_text.upper().strip()
        
        if "SEARCH" in intent_text:
            return IntentType.SEARCH
        elif "CHAT" in intent_text:
            return IntentType.CHAT
        elif "CONFIG" in intent_text:
            return IntentType.CONFIG
        elif "HELP" in intent_text:
            return IntentType.HELP
        elif "MEDITATION" in intent_text:
            return IntentType.MEDITATION
        else:
            return IntentType.UNKNOWN
    
    def _calculate_confidence(self, message: str, intent_type: IntentType) -> float:
        """计算意图识别的置信度"""
        # 基于关键词匹配计算置信度
        confidence = 0.5  # 基础置信度
        
        if intent_type == IntentType.SEARCH:
            search_keywords = ['搜索', '查找', '找', '帮我找', '如何', '怎么', '什么是', '最新', '新闻']
            if any(keyword in message for keyword in search_keywords):
                confidence += 0.3
        elif intent_type == IntentType.CHAT:
            chat_keywords = ['你好', '再见', '谢谢', '哈哈', '😊', '😄', '😍']
            if any(keyword in message for keyword in chat_keywords):
                confidence += 0.3
        elif intent_type == IntentType.CONFIG:
            config_keywords = ['配置', '设置', 'API', 'base_url', 'api_key']
            if any(keyword in message for keyword in config_keywords):
                confidence += 0.3
        elif intent_type == IntentType.HELP:
            help_keywords = ['帮助', '说明', '怎么用', '功能', '帮助']
            if any(keyword in message for keyword in help_keywords):
                confidence += 0.3
        elif intent_type == IntentType.MEDITATION:
            meditation_keywords = ['冥想', '编码', 'A2B', 'B2C', '记忆']
            if any(keyword in message for keyword in meditation_keywords):
                confidence += 0.3
        
        return min(confidence, 1.0)
    
    def _extract_search_query(self, message: str) -> str:
        """提取搜索查询"""
        # 移除搜索关键词
        search_keywords = [
            '搜索', '查找', '找', '帮我找', '帮我搜索', '帮我查找',
            'search', 'find', 'look for', 'help me find'
        ]
        
        query = message
        for keyword in search_keywords:
            if keyword in query.lower():
                query = query.replace(keyword, '').replace('帮我', '').strip()
                break
        
        return query
    
    def _get_cache_key(self, message: str) -> str:
        """生成缓存键"""
        return f"intent_{hash(message)}"
    
    def _cache_result(self, cache_key: str, result: Dict[str, Any]):
        """缓存结果"""
        # 限制缓存大小
        if len(self.cache) >= self.cache_size:
            # 删除最旧的缓存项
            oldest_key = min(self.cache.keys(), key=lambda k: self.cache[k]['timestamp'])
            del self.cache[oldest_key]
        
        self.cache[cache_key] = {
            'result': result,
            'timestamp': time.time()
        }
    
    def _get_fallback_result(self, message: str) -> Dict[str, Any]:
        """获取备用结果"""
        # 基于关键词的简单规则识别
        message_lower = message.lower()
        
        if any(keyword in message_lower for keyword in ['搜索', '查找', '找', '如何', '怎么', '什么是']):
            intent_type = IntentType.SEARCH
            search_query = self._extract_search_query(message)
        elif any(keyword in message_lower for keyword in ['配置', '设置', 'API']):
            intent_type = IntentType.CONFIG
            search_query = None
        elif any(keyword in message_lower for keyword in ['帮助', '说明', '怎么用']):
            intent_type = IntentType.HELP
            search_query = None
        elif any(keyword in message_lower for keyword in ['冥想', '编码', 'A2B', 'B2C']):
            intent_type = IntentType.MEDITATION
            search_query = None
        else:
            intent_type = IntentType.CHAT
            search_query = None
        
        return {
            "intent_type": intent_type.value,
            "confidence": 0.6,  # 备用识别置信度较低
            "search_query": search_query,
            "message": message,
            "timestamp": time.time(),
            "fallback": True
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            **self.stats,
            "cache_size": len(self.cache),
            "cache_hit_rate": self.stats["cache_hits"] / max(self.stats["total_requests"], 1)
        }
    
    def clear_cache(self):
        """清空缓存"""
        self.cache.clear()
    
    def test_connection(self) -> Dict[str, Any]:
        """测试API连接"""
        try:
            test_message = "你好"
            result = self.recognize_intent(test_message)
            return {
                "success": True,
                "message": "连接正常",
                "test_result": result
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


# 全局意图识别器实例
intent_recognition = IntentRecognition() 