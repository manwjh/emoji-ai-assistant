#!/usr/bin/env python3
"""
测试意图识别模块与主对话的集成
"""

import os
import sys
from core.llm_client import LLMClient

def test_intent_integration():
    """测试意图识别集成"""
    print("🧪 测试意图识别模块与主对话的集成")
    print("=" * 50)
    
    # 创建LLM客户端
    llm_client = LLMClient(api_type="openai")
    
    # 测试用例
    test_cases = [
        "今天几号",
        "现在什么时候", 
        "你好，好烦",
        "系统信息",
        "帮我计算1+1等于多少",
        "开始冥想"
    ]
    
    for i, message in enumerate(test_cases, 1):
        print(f"\n{i}. 测试消息: {message}")
        print("-" * 30)
        
        try:
            # 使用意图识别增强的响应方法
            response = llm_client.get_response_with_intent(message)
            print(f"✅ 响应: {response}")
        except Exception as e:
            print(f"❌ 错误: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_intent_integration() 