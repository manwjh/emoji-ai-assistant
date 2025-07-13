"""
核心模块 - 包含核心功能组件
"""

from .llm_client import LLMClient
# from .search_module import SearchModule, search_module  # 模块不存在，注释掉
# from .intent_recognition import IntentRecognition, IntentType, intent_recognition  # 模块不存在，注释掉
 
__all__ = ['LLMClient']  # 只导出存在的模块 