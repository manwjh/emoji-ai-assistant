"""
大模型接口模块
"""

import os
import json
import time
import requests
from typing import Optional, Dict, Any, List
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
        
        # system_prompt 不再在init时静态赋值
        # self.system_prompt = self._get_system_prompt()
    
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
        """获取完整的系统提示词，包含AI灵魂（systemprompt.txt）和潜意识（memC.txt）"""
        import os
        import sys
        
        # 1. 加载AI灵魂（系统提示词）
        system_prompt = self._load_ai_soul()
        
        # 2. 加载AI潜意识（memC记忆）
        memc_content = self._load_ai_subconscious()
        
        # 3. 组合完整的系统提示词
        if memc_content:
            complete_prompt = f"{system_prompt}\n\n# 潜意识记忆\n{memc_content}"
            print(f"✅ 完整系统提示词: AI灵魂({len(system_prompt)}字符) + 潜意识({len(memc_content)}字符)")
        else:
            complete_prompt = system_prompt
            print(f"✅ 系统提示词: AI灵魂({len(system_prompt)}字符) + 无潜意识记忆")
        
        return complete_prompt
    
    def _load_ai_soul(self) -> str:
        """加载AI灵魂（系统提示词）"""
        import os
        import sys
        
        system_prompt_path = os.path.join(os.path.dirname(__file__), '../MemABC/systemprompt.txt')
        
        try:
            with open(system_prompt_path, 'r', encoding='utf-8') as f:
                system_prompt = f.read().strip()
            
            if system_prompt:
                return system_prompt
            else:
                print("❌ 系统提示词文件为空")
                sys.exit(1)
                
        except FileNotFoundError:
            print("❌ 系统提示词文件不存在: systemprompt.txt")
            print("💡 请先运行以下命令生成系统提示词：")
            print("   cd emoji_boy/MemABC && ./memC_to_system_prompt.sh --init")
            print("   或者从memC生成个性化系统提示词：")
            print("   cd emoji_boy/MemABC && ./memC_to_system_prompt.sh")
            sys.exit(1)
        except Exception as e:
            print(f"❌ 读取系统提示词失败: {e}")
            sys.exit(1)
    
    def _load_ai_subconscious(self) -> str:
        """加载AI潜意识（memC记忆）"""
        import os
        
        memc_path = os.path.join(os.path.dirname(__file__), '../MemABC/memC/memC.txt')
        
        try:
            with open(memc_path, 'r', encoding='utf-8') as f:
                memc_content = f.read().strip()
            
            if memc_content:
                # 去掉头部标志
                if memc_content.startswith('# memC记忆'):
                    memc_content = memc_content.split('\n', 1)[-1].strip()
                return memc_content
            else:
                print("⚠️ memC记忆文件为空，将只使用AI灵魂")
                return ""
                
        except FileNotFoundError:
            print("⚠️ memC记忆文件不存在，将只使用AI灵魂")
            return ""
        except Exception as e:
            print(f"⚠️ 读取memC记忆失败: {e}，将只使用AI灵魂")
            return ""
    
    @property
    def system_prompt(self):
        """
        每次访问都动态读取memC内容，保证潜意识最新
        """
        return self._get_system_prompt()
    
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
    
    def get_response_with_intent(self, message: str) -> str:
        """
        获取模型响应，支持意图识别和执行功能
        
        流程：用户输入 → 意图识别 → 功能执行 → 原始输入+执行结果 → LLM对话
        
        Args:
            message: 用户消息
            
        Returns:
            模型响应文本
        """
        try:
            print(f"📝 用户输入: {message}")
            
            # 第一步：使用新的意图引擎进行意图识别和执行
            import sys
            import os
            
            # 添加brain_agent到Python路径
            brain_agent_path = os.path.join(os.path.dirname(__file__), '..', 'brain_agent')
            if brain_agent_path not in sys.path:
                sys.path.insert(0, brain_agent_path)
            
            # 导入意图引擎
            from intent_engine import IntentEngine
            
            # 创建意图引擎实例
            # 优先使用当前LLM客户端的API密钥，如果没有则从环境变量获取
            api_key = self.api_key or os.getenv("DOUBAO_API_KEY")
            intent_engine = IntentEngine(api_key=api_key)
            
            # 处理消息（意图识别 + 执行）
            process_result = intent_engine.process_message(message)
            
            intent_type = process_result.get('intent_data', {}).get('intent_type', 'unknown')
            confidence = process_result.get('intent_data', {}).get('confidence', 0.0)
            success = process_result.get('success', False)
            execution_result = process_result.get('response', '')
            
            print(f"🧠 意图识别: {intent_type} (置信度: {confidence:.2f})")
            print(f"⚡ 执行结果: {'成功' if success else '失败'}")
            
            # 第二步：构建增强的输入
            enhanced_message = message
            
            # 如果有执行结果，将其添加到原始输入中
            if success and execution_result:
                enhanced_message = f"{message}\n\n[系统执行结果]: {execution_result}"
                print(f"🔗 增强输入: {enhanced_message[:100]}...")
            elif not success:
                # 执行失败，添加错误信息
                error_msg = process_result.get('error', '执行失败')
                enhanced_message = f"{message}\n\n[系统执行失败]: {error_msg}"
                print(f"⚠️ 执行失败: {error_msg}")
            
            # 第三步：使用增强的输入生成LLM回复
            final_response = self.get_response(enhanced_message)
            
            print(f"💬 生成回复: {final_response[:100]}...")
            return final_response
                
        except Exception as e:
            print(f"❌ 意图识别响应失败: {e}")
            import traceback
            traceback.print_exc()
            return self.get_response(message)
    
    def _generate_comprehensive_response(self, user_message: str, intent_type: str, search_reference: str = None, search_content: List[Dict[str, str]] = None) -> str:
        """
        生成综合回复
        
        Args:
            user_message: 用户消息
            intent_type: 意图类型
            search_reference: 搜索参考资料
            search_content: 爬取的搜索结果内容
            
        Returns:
            综合回复文本
        """
        try:
            # 构建增强的系统提示词
            enhanced_system_prompt = self._build_enhanced_system_prompt(intent_type, search_reference, search_content)
            
            # 临时设置增强的系统提示词
            original_prompt = self.system_prompt
            self.system_prompt = enhanced_system_prompt
            
            # 生成回复
            response = self.get_response(user_message)
            
            # 恢复原始系统提示词
            self.system_prompt = original_prompt
            
            return response
            
        except Exception as e:
            print(f"❌ 综合回复生成失败: {e}")
            return self.get_response(user_message)
    
    def _build_enhanced_system_prompt(self, intent_type: str, search_reference: str = None, search_content: List[Dict[str, str]] = None) -> str:
        """
        构建增强的系统提示词
        
        Args:
            intent_type: 意图类型
            search_reference: 搜索参考资料
            search_content: 爬取的搜索结果内容
            
        Returns:
            增强的系统提示词
        """
        base_prompt = self.system_prompt
        
        # 根据意图类型添加特定指导
        intent_guidance = ""
        if intent_type == 'search':
            intent_guidance = """
搜索意图指导：
- 用户需要查找信息或获取最新资料
- 请基于搜索结果提供准确、有用的信息
- 如果搜索结果不够准确，请说明并提供建议
- 保持友好和专业的语气
- 引用具体的搜索结果来源
"""
        elif intent_type == 'chat':
            intent_guidance = """
聊天意图指导：
- 用户希望进行轻松愉快的对话
- 保持温暖、友善的语气
- 适当使用emoji表情
- 关注用户的情感需求
"""
        elif intent_type == 'config':
            intent_guidance = """
配置意图指导：
- 用户需要配置系统参数
- 提供清晰的配置指导
- 确保配置信息的安全性
- 验证配置的有效性
"""
        elif intent_type == 'help':
            intent_guidance = """
帮助意图指导：
- 用户需要了解功能或使用方法
- 提供详细、易懂的说明
- 使用具体的例子
- 引导用户正确使用功能
"""
        elif intent_type == 'meditation':
            intent_guidance = """
冥想意图指导：
- 用户需要进行记忆编码或冥想
- 提供专业的冥想指导
- 确保冥想过程的安全性
- 关注用户的身心状态
"""
        
        # 添加搜索参考资料
        search_context = ""
        if search_reference:
            search_context = f"""
搜索参考资料：
{search_reference}
"""
        
        # 添加爬取的搜索结果内容
        if search_content:
            from .search_module import search_module
            search_summary = search_module.get_search_summary(search_content)
            search_context += f"""

详细搜索结果：
{search_summary}

请基于以上搜索结果回答用户问题，确保信息的准确性和时效性。可以引用具体的搜索结果来源。
"""
        elif search_reference:
            search_context += """

请基于以上搜索结果回答用户问题，确保信息的准确性和时效性。
"""
        
        # 组合最终的提示词
        enhanced_prompt = f"{base_prompt}\n\n{intent_guidance}\n{search_context}"
        
        return enhanced_prompt.strip()
    
    def get_response_with_search(self, message: str) -> str:
        """
        获取模型响应，支持搜索功能（向后兼容）
        
        Args:
            message: 用户消息
            
        Returns:
            模型响应文本
        """
        return self.get_response_with_intent(message)
    
    def _should_search(self, message: str) -> bool:
        """判断是否需要搜索"""
        search_keywords = [
            '搜索', '查找', '找', '帮我找', '帮我搜索', '帮我查找',
            'search', 'find', 'look for', 'help me find'
        ]
        
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in search_keywords)
    
    def _perform_search_with_query(self, query: str) -> Dict[str, Any]:
        """使用指定查询执行搜索"""
        try:
            from .search_module import search_module
            
            if not query:
                return {
                    'success': False,
                    'error': '搜索查询为空',
                    'message': '❌ 搜索查询不能为空'
                }
            
            # 执行智能搜索
            result = search_module.smart_search(query)
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': f'❌ 搜索执行失败: {str(e)}'
            }
    
    def _perform_search(self, message: str) -> Dict[str, Any]:
        """执行搜索（向后兼容）"""
        try:
            from .search_module import search_module
            
            # 提取搜索查询
            query = self._extract_search_query(message)
            if not query:
                return {
                    'success': False,
                    'error': '无法提取搜索查询',
                    'message': '❌ 无法理解搜索请求'
                }
            
            # 执行智能搜索
            result = search_module.smart_search(query)
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': f'❌ 搜索执行失败: {str(e)}'
            }
    
    def _extract_search_query(self, message: str) -> str:
        """从消息中提取搜索查询"""
        # 移除搜索关键词
        search_keywords = [
            '搜索', '查找', '找', '帮我找', '帮我搜索', '帮我查找',
            'search', 'find', 'look for', 'help me find'
        ]
        
        query = message
        for keyword in search_keywords:
            if keyword in query.lower():
                # 移除关键词及其前后的空格
                query = query.replace(keyword, '').replace('帮我', '').strip()
                break
        
        return query 