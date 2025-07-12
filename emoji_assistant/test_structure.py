#!/usr/bin/env python3
"""
测试代码结构完整性
"""

import sys
import os

def test_imports():
    """测试模块导入"""
    print("🔍 测试模块导入...")
    
    try:
        # 测试UI模块
        from ui.floating_head import FloatingEmojiWindow
        from ui.speech_bubble import SpeechBubbleWidget
        print("✅ UI模块导入成功")
        
        # 测试交互模块
        from interaction.emotion_detector import EmotionDetector
        from interaction.keyboard_listener import KeyboardListener
        from interaction.chat_input import ChatInputDialog
        print("✅ 交互模块导入成功")
        
        # 测试核心模块
        from core.llm_client import LLMClient
        print("✅ 核心模块导入成功")
        
        # 测试配置
        import config
        print("✅ 配置模块导入成功")
        
        return True
        
    except ImportError as e:
        print(f"❌ 模块导入失败: {e}")
        return False

def test_class_instantiation():
    """测试类实例化"""
    print("\n🔍 测试类实例化...")
    
    try:
        # 测试情绪检测器
        from interaction.emotion_detector import EmotionDetector
        emotion_detector = EmotionDetector()
        print("✅ EmotionDetector 实例化成功")
        
        # 测试LLM客户端
        from core.llm_client import LLMClient
        llm_client = LLMClient(api_type="mock")
        print("✅ LLMClient 实例化成功")
        
        # 测试键盘监听器
        from interaction.keyboard_listener import KeyboardListener
        keyboard_listener = KeyboardListener(emotion_detector)
        print("✅ KeyboardListener 实例化成功")
        
        return True
        
    except Exception as e:
        print(f"❌ 类实例化失败: {e}")
        return False

def test_basic_functionality():
    """测试基本功能"""
    print("\n🔍 测试基本功能...")
    
    try:
        # 测试情绪检测
        from interaction.emotion_detector import EmotionDetector
        emotion_detector = EmotionDetector()
        emotion_detector.add_text("我今天很烦很累")
        print("✅ 情绪检测功能正常")
        
        # 测试LLM客户端
        from core.llm_client import LLMClient
        llm_client = LLMClient(api_type="mock")
        response = llm_client.get_response("你好")
        print(f"✅ LLM响应功能正常: {response[:20]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ 基本功能测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 开始测试 Emoji 助手代码结构...\n")
    
    tests = [
        test_imports,
        test_class_instantiation,
        test_basic_functionality
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！代码结构完整。")
        return 0
    else:
        print("⚠️ 部分测试失败，请检查代码。")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 