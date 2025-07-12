#!/usr/bin/env python3
"""
简化的代码结构测试（不依赖PyQt5）
"""

import sys
import os

def test_core_modules():
    """测试核心模块（不依赖PyQt5）"""
    print("🔍 测试核心模块...")
    
    try:
        # 测试配置模块
        import config
        print("✅ 配置模块导入成功")
        
        # 测试LLM客户端（不依赖PyQt5的部分）
        from core.llm_client import LLMClient
        print("✅ LLM客户端导入成功")
        
        # 测试情绪检测器（不依赖PyQt5的部分）
        from interaction.emotion_detector import EmotionDetector
        print("✅ 情绪检测器导入成功")
        
        return True
        
    except ImportError as e:
        print(f"❌ 核心模块导入失败: {e}")
        return False

def test_class_instantiation():
    """测试类实例化（不依赖PyQt5）"""
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
        
        return True
        
    except Exception as e:
        print(f"❌ 类实例化失败: {e}")
        return False

def test_basic_functionality():
    """测试基本功能（不依赖PyQt5）"""
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

def test_file_structure():
    """测试文件结构"""
    print("\n🔍 测试文件结构...")
    
    required_files = [
        "main.py",
        "config.py", 
        "run.py",
        "requirements.txt",
        "README.md",
        "env_example.txt",
        "__init__.py",
        "ui/__init__.py",
        "ui/floating_head.py",
        "ui/speech_bubble.py",
        "interaction/__init__.py",
        "interaction/emotion_detector.py",
        "interaction/keyboard_listener.py",
        "interaction/chat_input.py",
        "core/__init__.py",
        "core/llm_client.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ 缺少文件: {missing_files}")
        return False
    else:
        print("✅ 所有必需文件都存在")
        return True

def test_import_structure():
    """测试导入结构"""
    print("\n🔍 测试导入结构...")
    
    try:
        # 测试包导入
        import emoji_assistant
        print("✅ 主包导入成功")
        
        # 测试子包导入
        from emoji_assistant import ui, interaction, core
        print("✅ 子包导入成功")
        
        return True
        
    except ImportError as e:
        print(f"❌ 导入结构测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 开始测试 Emoji 助手代码结构（简化版）...\n")
    
    tests = [
        test_file_structure,
        test_import_structure,
        test_core_modules,
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
        print("\n📝 下一步:")
        print("1. 安装依赖: pip install PyQt5 pynput requests typing-extensions")
        print("2. 运行完整测试: python test_structure.py")
        print("3. 启动程序: python run.py")
        return 0
    else:
        print("⚠️ 部分测试失败，请检查代码。")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 