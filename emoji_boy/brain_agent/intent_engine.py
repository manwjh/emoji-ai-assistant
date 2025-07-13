"""
Intent Engine - 类脑意图识别引擎

这是brain_agent的核心模块，模仿人脑的感知和认知过程：
1. 感知输入：接收和处理用户输入信息
2. 意图识别：模仿人脑的认知过程识别意图
3. 技能选择：类似人脑的技能网络选择和执行
4. 行为模式：基于历史交互优化反应策略
5. 记忆机制：模拟人脑的记忆和回忆过程
"""

import os
import json
import time
import requests
import logging
from typing import Dict, Any, List, Optional, Union
from enum import Enum
import re
from collections import OrderedDict

try:
    from .plugin_registry import PluginRegistry, plugin_registry
except (ImportError, SystemError):
    from brain_agent.plugin_registry import PluginRegistry, plugin_registry

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class IntentType(Enum):
    """意图类型枚举 - 模仿人脑的认知分类"""
    SEARCH = "search"           # 搜索意图 - 信息获取需求
    CHAT = "chat"              # 聊天意图 - 社交交流需求
    CONFIG = "config"          # 配置意图 - 系统调整需求
    HELP = "help"              # 帮助意图 - 学习指导需求
    MEDITATION = "meditation"  # 冥想意图 - 专注训练需求
    SYSTEM = "system"          # 系统意图 - 系统操作需求
    UNKNOWN = "unknown"        # 未知意图 - 未识别需求


class IntentEngine:
    """类脑意图识别引擎 - 模仿人脑的感知和认知系统"""
    
    def __init__(self, api_key: str = None, api_base: str = None, 
                 cache_size: int = 100, cache_ttl: int = 300):
        """
        初始化类脑意图识别引擎
        
        Args:
            api_key: API密钥
            api_base: API基础URL
            cache_size: 记忆容量（模拟人脑的记忆容量）
            cache_ttl: 记忆保持时间（模拟人脑的记忆衰减）
        """
        # 配置
        self.api_key = api_key or os.getenv("DOUBAO_API_KEY")
        self.api_base = api_base or "https://ark.cn-beijing.volces.com/api/v3"
        self.model_name = "doubao-1-5-lite-32k-250115"
        
        # 请求配置
        self.timeout = 10
        self.max_retries = 2
        self.retry_delay = 1
        
        # 类脑意图识别提示词
        self.intent_prompt = self._get_intent_prompt()
        
        # 技能匹配提示词
        self.skill_matching_prompt = self._get_skill_matching_prompt()
        
        # 代码生成提示词
        self.code_generation_prompt = self._get_code_generation_prompt()
        
        # 类脑记忆机制 - 使用OrderedDict实现LRU记忆
        self.cache_size = cache_size
        self.cache_ttl = cache_ttl
        self.cache = OrderedDict()
        
        # 行为模式统计
        self.stats = {
            "total_requests": 0,
            "cache_hits": 0,
            "successful_recognitions": 0,
            "failed_recognitions": 0,
            "plugin_executions": 0,
            "api_errors": 0,
            "average_response_time": 0.0,
            "code_executions": 0,
            "skill_matches": 0
        }
        
        # 技能网络（原插件注册表）
        self.plugin_registry = plugin_registry
        
        logger.info("类脑意图识别引擎初始化成功")
    
    def _get_intent_prompt(self) -> str:
        """获取类脑意图识别提示词"""
        return """你是一个模仿人脑认知过程的意图识别助手。请像人脑一样分析用户输入，识别其意图类型。

人脑认知分类：
1. SEARCH - 信息获取需求（类似人脑的求知欲）
2. CHAT - 社交交流需求（类似人脑的社交本能）
3. CONFIG - 系统调整需求（类似人脑的适应能力）
4. HELP - 学习指导需求（类似人脑的学习能力）
5. MEDITATION - 专注训练需求（类似人脑的专注力）
6. SYSTEM - 系统操作需求（类似人脑的自主控制）
7. UNKNOWN - 未识别需求（类似人脑的困惑状态）

认知识别规则：
- 包含"搜索"、"查找"、"找"、"帮我找"等 → SEARCH（求知欲）
- 包含"如何"、"怎么"、"什么是"、"最新"、"新闻"等 → SEARCH（信息需求）
- 包含"配置"、"设置"、"API"、"base_url"等 → CONFIG（适应调整）
- 包含"帮助"、"说明"、"怎么用"、"功能"等 → HELP（学习需求）
- 包含"冥想"、"编码"、"A2B"、"B2C"等 → MEDITATION（专注训练）
- 包含"今天几号"、"现在时间"、"几点"、"日期"、"时间"等 → SYSTEM（时间查询）
- 包含"系统信息"、"系统版本"、"操作系统"等 → SYSTEM（系统信息）
- 包含"执行"、"运行"、"命令"等 → SYSTEM（命令执行）
- 问候语、闲聊、情感表达 → CHAT（社交需求）

请只返回意图类型（SEARCH/CHAT/CONFIG/HELP/MEDITATION/SYSTEM/UNKNOWN），不要包含其他内容。"""
    
    def _get_skill_matching_prompt(self) -> str:
        """获取技能匹配提示词"""
        return """你是一个技能匹配专家。根据用户意图和可用技能列表，选择最合适的技能来处理用户请求。

可用技能列表：
1. search_plugin - 处理搜索相关请求，如"搜索Python教程"、"查找最新新闻"
2. chat_plugin - 处理聊天交流，如"你好"、"今天天气怎么样"
3. config_plugin - 处理配置设置，如"设置API密钥"、"配置系统参数"
4. help_plugin - 处理帮助请求，如"帮助"、"怎么使用"
5. meditation_plugin - 处理冥想相关，如"开始冥想"、"A2B编码"
6. system_plugin - 处理系统操作，如"今天几号"、"系统信息"、"执行命令"

匹配规则：
- 如果用户请求需要搜索信息，选择search_plugin
- 如果用户请求是聊天交流，选择chat_plugin
- 如果用户请求涉及配置设置，选择config_plugin
- 如果用户请求需要帮助说明，选择help_plugin
- 如果用户请求涉及冥想或记忆编码，选择meditation_plugin
- 如果用户请求涉及系统操作（时间、系统信息、命令执行），选择system_plugin

请只返回技能名称（如：system_plugin），如果不需要技能则返回NONE。"""
    
    def _get_code_generation_prompt(self) -> str:
        """获取代码生成提示词"""
        return """你是一个Python代码生成专家。根据用户请求，生成简洁、安全的Python代码来完成任务。

代码生成规则：
1. 只使用Python标准库，不要使用第三方库
2. 代码要简洁明了，只包含必要的功能
3. 确保代码安全，不要执行危险操作
4. 使用print()输出结果
5. 代码要能直接运行，不需要额外配置

示例：
用户请求："现在什么时候"
生成代码：
```python
import time
current_time = time.localtime()
print("当前时间：", time.strftime("%Y-%m-%d %H:%M:%S", current_time))
```

用户请求："今天几号"
生成代码：
```python
import datetime
today = datetime.datetime.now()
print("今天是：", today.strftime("%Y年%m月%d日"))
```

请只返回Python代码，不要包含其他说明文字。"""
    
    def recognize_intent(self, message: str) -> Dict[str, Any]:
        """
        类脑意图识别 - 模仿人脑的感知和认知过程
        
        Args:
            message: 用户输入信息
            
        Returns:
            包含意图信息的字典
        """
        if not message or not message.strip():
            logger.warning("接收到空输入信息")
            return self._get_fallback_result("")
        
        message = message.strip()
        start_time = time.time()
        
        try:
            # 检查记忆缓存（模拟人脑的记忆回忆）
            cache_key = self._get_cache_key(message)
            if cache_key in self.cache:
                cached_result = self.cache[cache_key]
                if time.time() - cached_result['timestamp'] < self.cache_ttl:
                    self.stats["cache_hits"] += 1
                    logger.debug(f"记忆命中: {message[:20]}...")
                    return cached_result['result']
                else:
                    # 记忆衰减，删除
                    del self.cache[cache_key]
            
            self.stats["total_requests"] += 1
            
            # 调用认知API进行意图识别
            intent_result = self._call_intent_api(message)
            
            # 处理认知结果
            result = self._process_intent_result(message, intent_result)
            
            # 存储到记忆（模拟人脑的记忆存储）
            self._cache_result(cache_key, result)
            
            # 更新行为模式统计
            response_time = time.time() - start_time
            self.stats["successful_recognitions"] += 1
            self._update_average_response_time(response_time)
            
            logger.info(f"意图识别成功: {result.get('intent_type')} (置信度: {result.get('confidence', 0):.2f})")
            return result
            
        except Exception as e:
            self.stats["failed_recognitions"] += 1
            logger.error(f"意图识别失败: {e}")
            return self._get_fallback_result(message)
    
    def match_skill(self, message: str, intent_type: str) -> str:
        """
        技能匹配 - 根据意图选择最合适的技能
        
        Args:
            message: 用户消息
            intent_type: 意图类型
            
        Returns:
            技能名称或NONE
        """
        try:
            # 构建技能匹配请求
            skill_prompt = f"{self.skill_matching_prompt}\n\n用户消息: {message}\n意图类型: {intent_type}\n\n请选择最合适的技能:"
            
            skill_result = self._call_llm_api(skill_prompt, max_tokens=20)
            skill_name = skill_result.strip().lower()
            
            # 验证技能名称
            available_skills = ["search_plugin", "chat_plugin", "config_plugin", "help_plugin", "meditation_plugin", "system_plugin"]
            if skill_name in available_skills:
                self.stats["skill_matches"] += 1
                logger.info(f"技能匹配成功: {skill_name}")
                return skill_name
            else:
                logger.info(f"无需技能匹配，直接回答")
                return "NONE"
                
        except Exception as e:
            logger.error(f"技能匹配失败: {e}")
            return "NONE"
    
    def generate_code(self, message: str, skill_name: str) -> str:
        """
        代码生成 - 根据用户请求生成可执行的Python代码
        
        Args:
            message: 用户消息
            skill_name: 技能名称
            
        Returns:
            生成的Python代码
        """
        try:
            # 构建代码生成请求
            code_prompt = f"{self.code_generation_prompt}\n\n用户请求: {message}\n技能: {skill_name}\n\n请生成Python代码:"
            
            code_result = self._call_llm_api(code_prompt, max_tokens=200)
            
            # 提取代码块
            code_match = re.search(r'```python\s*(.*?)\s*```', code_result, re.DOTALL)
            if code_match:
                code = code_match.group(1).strip()
            else:
                # 如果没有代码块标记，直接使用结果
                code = code_result.strip()
            
            logger.info(f"代码生成成功: {len(code)} 字符")
            return code
            
        except Exception as e:
            logger.error(f"代码生成失败: {e}")
            return ""
    
    def execute_code(self, code: str) -> Dict[str, Any]:
        """
        执行代码 - 安全执行生成的Python代码
        
        Args:
            code: Python代码
            
        Returns:
            执行结果
        """
        try:
            # 安全检查
            if not self._is_safe_code(code):
                return {
                    "success": False,
                    "error": "代码包含不安全操作",
                    "output": ""
                }
            
            # 创建安全的执行环境
            import io
            import sys
            from contextlib import redirect_stdout
            
            # 捕获输出
            output_buffer = io.StringIO()
            
            # 创建安全的全局环境，只允许安全的函数
            safe_globals = {
                "__builtins__": {
                    "print": print,
                    "len": len,
                    "str": str,
                    "int": int,
                    "float": float,
                    "list": list,
                    "dict": dict,
                    "tuple": tuple,
                    "set": set,
                    "bool": bool,
                    "type": type,
                    "isinstance": isinstance,
                    "range": range,
                    "enumerate": enumerate,
                    "zip": zip,
                    "map": map,
                    "filter": filter,
                    "sum": sum,
                    "max": max,
                    "min": min,
                    "abs": abs,
                    "round": round,
                    "sorted": sorted,
                    "reversed": reversed,
                    "any": any,
                    "all": all,
                    "chr": chr,
                    "ord": ord,
                    "hex": hex,
                    "oct": oct,
                    "bin": bin,
                    "pow": pow,
                    "divmod": divmod,
                    "hash": hash,
                    "id": id,
                    "repr": repr,
                    "ascii": ascii,
                    "format": format,
                    "vars": vars,
                    "dir": dir,
                    "getattr": getattr,
                    "hasattr": hasattr,
                    "callable": callable,
                    "issubclass": issubclass,
                    "super": super,
                    "property": property,
                    "staticmethod": staticmethod,
                    "classmethod": classmethod,
                    "compile": compile,
                    "eval": eval,
                    "exec": exec,
                    "__import__": __import__
                }
            }
            
            with redirect_stdout(output_buffer):
                exec(code, safe_globals, {})
            
            output = output_buffer.getvalue().strip()
            self.stats["code_executions"] += 1
            
            return {
                "success": True,
                "output": output,
                "code": code
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "output": ""
            }
    
    def _is_safe_code(self, code: str) -> bool:
        """检查代码安全性"""
        dangerous_patterns = [
            r'import\s+os\s*$',
            r'import\s+subprocess',
            r'import\s+sys\s*$',
            r'os\.',
            r'subprocess\.',
            r'sys\.',
            r'open\s*\(',
            r'file\s*\(',
            r'input\s*\(',
            r'raw_input\s*\(',
            r'globals\s*\(',
            r'locals\s*\(',
            r'setattr\s*\(',
            r'delattr\s*\(',
            r'__\w+__\s*\(',
            r'__\w+__\s*=',
            r'__\w+__\s*\.',
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, code, re.MULTILINE | re.IGNORECASE):
                return False
        
        return True
    
    def process_message(self, message: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        处理用户消息（类脑感知-认知-执行循环）
        
        Args:
            message: 用户输入信息
            context: 上下文信息
            
        Returns:
            Dict: 处理结果
        """
        start_time = time.time()
        
        # 感知阶段：识别意图
        intent_data = self.recognize_intent(message)
        intent_type = intent_data.get("intent_type", "unknown")
        
        # 认知阶段：技能匹配
        skill_name = self.match_skill(message, intent_type)
        
        result = {
            "success": False,
            "intent_data": intent_data,
            "skill_name": skill_name,
            "message": message,
            "timestamp": time.time(),
            "processing_time": time.time() - start_time
        }
        
        # 执行阶段：根据技能类型处理
        if skill_name == "NONE":
            # 直接回答，不需要技能
            result["response_type"] = "direct_answer"
            result["success"] = True
            result["response"] = "我理解你的请求，但暂时无法提供具体帮助。"
            
        else:
            # 需要技能处理
            result["response_type"] = "skill_execution"
            
            # 生成代码
            code = self.generate_code(message, skill_name)
            if code:
                # 执行代码
                execution_result = self.execute_code(code)
                result.update(execution_result)
                
                if execution_result["success"]:
                    result["success"] = True
                    result["response"] = execution_result["output"]
                else:
                    result["response"] = f"执行失败: {execution_result['error']}"
            else:
                # 代码生成失败，使用传统插件方式
                plugin_result = self.plugin_registry.execute_intent(intent_data, context)
                result.update(plugin_result)
                result["response"] = plugin_result.get("message", "处理失败")
        
        # 更新统计
        self.stats["plugin_executions"] += 1
        
        logger.info(f"类脑处理完成: {result['success']}")
        return result
    
    def _call_llm_api(self, prompt: str, max_tokens: int = 100) -> str:
        """调用LLM API"""
        if not self.api_key:
            raise ValueError("API密钥未设置，请设置DOUBAO_API_KEY环境变量")
        
        # 构建请求数据
        data = {
            "model": self.model_name,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": max_tokens,
            "temperature": 0.1,
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
                    json=data,
                    headers=headers,
                    timeout=self.timeout
                )
                response.raise_for_status()
                
                result = response.json()
                return result["choices"][0]["message"]["content"].strip()
                
            except requests.exceptions.RequestException as e:
                self.stats["api_errors"] += 1
                logger.warning(f"LLM API调用尝试 {attempt + 1} 失败: {e}")
                
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (attempt + 1))
                else:
                    raise Exception(f"LLM API调用失败，已重试{self.max_retries}次: {e}")
    
    def _call_intent_api(self, message: str) -> str:
        """调用认知API进行意图识别"""
        return self._call_llm_api(self.intent_prompt + f"\n\n用户输入: {message}\n\n意图类型:", max_tokens=10)
    
    def _process_intent_result(self, message: str, intent_text: str) -> Dict[str, Any]:
        """处理认知识别结果"""
        try:
            # 解析意图类型
            intent_type = self._parse_intent_type(intent_text)
            
            # 计算认知置信度
            confidence = self._calculate_confidence(message, intent_type)
            
            # 提取搜索查询（如果是搜索意图）
            search_query = ""
            if intent_type == IntentType.SEARCH:
                search_query = self._extract_search_query(message)
            
            result = {
                "intent_type": intent_type.value,
                "confidence": confidence,
                "message": message,
                "timestamp": time.time()
            }
            
            if search_query:
                result["search_query"] = search_query
            
            return result
            
        except Exception as e:
            logger.error(f"处理认知结果时出错: {e}")
            return self._get_fallback_result(message)
    
    def _parse_intent_type(self, intent_text: str) -> IntentType:
        """解析意图类型"""
        intent_text = intent_text.strip().upper()
        
        # 意图类型映射
        intent_mapping = {
            "SEARCH": IntentType.SEARCH,
            "CHAT": IntentType.CHAT,
            "CONFIG": IntentType.CONFIG,
            "HELP": IntentType.HELP,
            "MEDITATION": IntentType.MEDITATION,
            "SYSTEM": IntentType.SYSTEM,
            "UNKNOWN": IntentType.UNKNOWN
        }
        
        return intent_mapping.get(intent_text, IntentType.UNKNOWN)
    
    def _calculate_confidence(self, message: str, intent_type: IntentType) -> float:
        """计算认知置信度"""
        confidence = 0.5  # 基础置信度
        
        # 根据关键词匹配调整置信度
        if intent_type == IntentType.SEARCH:
            search_keywords = ["搜索", "查找", "找", "帮我找", "如何", "怎么", "什么是", "最新", "新闻"]
            if any(keyword in message for keyword in search_keywords):
                confidence += 0.3
        
        elif intent_type == IntentType.CHAT:
            chat_keywords = ["你好", "谢谢", "再见", "拜拜", "早上好", "晚上好"]
            if any(keyword in message for keyword in chat_keywords):
                confidence += 0.3
        
        elif intent_type == IntentType.CONFIG:
            config_keywords = ["配置", "设置", "API", "base_url", "密钥"]
            if any(keyword in message for keyword in config_keywords):
                confidence += 0.3
        
        elif intent_type == IntentType.HELP:
            help_keywords = ["帮助", "说明", "怎么用", "功能", "指南"]
            if any(keyword in message for keyword in help_keywords):
                confidence += 0.3
        
        elif intent_type == IntentType.MEDITATION:
            meditation_keywords = ["冥想", "编码", "A2B", "B2C", "记忆"]
            if any(keyword in message for keyword in meditation_keywords):
                confidence += 0.3
        
        elif intent_type == IntentType.SYSTEM:
            system_keywords = ["今天几号", "现在时间", "几点", "日期", "时间", "系统信息", "系统版本", "执行", "运行", "命令"]
            if any(keyword in message for keyword in system_keywords):
                confidence += 0.3
        
        return min(confidence, 1.0)  # 确保不超过1.0
    
    def _extract_search_query(self, message: str) -> str:
        """提取搜索查询"""
        # 移除搜索相关词汇
        search_prefixes = ["搜索", "查找", "找", "帮我找", "如何", "怎么", "什么是"]
        
        query = message
        for prefix in search_prefixes:
            if query.startswith(prefix):
                query = query[len(prefix):].strip()
                break
        
        return query if query else message
    
    def _get_cache_key(self, message: str) -> str:
        """生成记忆键"""
        return f"intent:{hash(message)}"
    
    def _cache_result(self, cache_key: str, result: Dict[str, Any]):
        """存储到记忆"""
        # 实现LRU记忆机制
        if cache_key in self.cache:
            # 移动到末尾（最近使用）
            self.cache.move_to_end(cache_key)
        else:
            # 检查记忆容量
            if len(self.cache) >= self.cache_size:
                # 移除最旧的记忆
                self.cache.popitem(last=False)
        
        # 添加新记忆
        self.cache[cache_key] = {
            "result": result,
            "timestamp": time.time()
        }
    
    def _get_fallback_result(self, message: str) -> Dict[str, Any]:
        """获取降级处理结果"""
        return {
            "intent_type": IntentType.UNKNOWN.value,
            "confidence": 0.0,
            "message": message,
            "timestamp": time.time(),
            "error": "意图识别失败"
        }
    
    def _update_average_response_time(self, response_time: float):
        """更新平均响应时间"""
        total_requests = self.stats["successful_recognitions"]
        current_avg = self.stats["average_response_time"]
        
        # 计算新的平均值
        new_avg = (current_avg * (total_requests - 1) + response_time) / total_requests
        self.stats["average_response_time"] = new_avg
    
    def get_stats(self) -> Dict[str, Any]:
        """获取行为模式统计信息"""
        stats = self.stats.copy()
        
        # 计算记忆命中率
        if stats["total_requests"] > 0:
            stats["cache_hit_rate"] = stats["cache_hits"] / stats["total_requests"]
        else:
            stats["cache_hit_rate"] = 0.0
        
        # 计算成功率
        if stats["total_requests"] > 0:
            stats["success_rate"] = stats["successful_recognitions"] / stats["total_requests"]
        else:
            stats["success_rate"] = 0.0
        
        # 添加记忆信息
        stats["cache_size"] = len(self.cache)
        stats["cache_max_size"] = self.cache_size
        
        return stats
    
    def clear_cache(self):
        """清空记忆"""
        self.cache.clear()
        logger.info("记忆已清空")
    
    def test_connection(self) -> Dict[str, Any]:
        """测试认知API连接"""
        start_time = time.time()
        
        try:
            # 发送简单测试请求
            test_message = "你好"
            intent_result = self._call_intent_api(test_message)
            
            response_time = time.time() - start_time
            
            return {
                "success": True,
                "model": self.model_name,
                "response_time": response_time,
                "test_result": intent_result
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "response_time": time.time() - start_time
            }
    
    def register_plugin(self, plugin) -> bool:
        """注册技能"""
        return self.plugin_registry.register_plugin(plugin)
    
    def get_available_plugins(self) -> List[Dict[str, Any]]:
        """获取可用技能列表"""
        return self.plugin_registry.list_plugins() 