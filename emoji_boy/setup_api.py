#!/usr/bin/env python3
"""
API配置脚本

帮助用户设置各种API令牌，特别是Brain Agent需要的豆包API。
"""

import os
import sys
from typing import Optional


def setup_doubao_api():
    """设置豆包API"""
    print("🔧 配置豆包API（Brain Agent使用）")
    print("=" * 40)
    print("豆包API用于Brain Agent的意图识别功能")
    print("获取地址: https://ark.cn-beijing.volces.com/")
    print()
    
    # 检查是否已有环境变量
    current_key = os.getenv("DOUBAO_API_KEY")
    if current_key and current_key != "your_doubao_api_key_here":
        print(f"✅ 已检测到豆包API密钥: {current_key[:8]}...")
        choice = input("是否要更新API密钥？(y/N): ").strip().lower()
        if choice != 'y':
            return current_key
    
    # 获取新的API密钥
    api_key = input("请输入豆包API密钥: ").strip()
    
    if not api_key:
        print("❌ API密钥不能为空")
        return None
    
    if api_key == "your_doubao_api_key_here":
        print("❌ 请使用真实的API密钥，而不是占位符")
        return None
    
    # 设置环境变量
    os.environ["DOUBAO_API_KEY"] = api_key
    print(f"✅ 豆包API密钥已设置: {api_key[:8]}...")
    
    return api_key


def setup_openai_api():
    """设置OpenAI API"""
    print("\n🔧 配置OpenAI API")
    print("=" * 30)
    print("OpenAI API用于其他AI功能")
    print("获取地址: https://platform.openai.com/")
    print()
    
    current_key = os.getenv("OPENAI_API_KEY")
    if current_key and current_key != "your_openai_api_key_here":
        print(f"✅ 已检测到OpenAI API密钥: {current_key[:8]}...")
        choice = input("是否要更新API密钥？(y/N): ").strip().lower()
        if choice != 'y':
            return current_key
    
    api_key = input("请输入OpenAI API密钥: ").strip()
    
    if not api_key:
        print("❌ API密钥不能为空")
        return None
    
    if api_key == "your_openai_api_key_here":
        print("❌ 请使用真实的API密钥，而不是占位符")
        return None
    
    os.environ["OPENAI_API_KEY"] = api_key
    print(f"✅ OpenAI API密钥已设置: {api_key[:8]}...")
    
    return api_key


def setup_huggingface_api():
    """设置HuggingFace API"""
    print("\n🔧 配置HuggingFace API")
    print("=" * 35)
    print("HuggingFace API用于模型推理")
    print("获取地址: https://huggingface.co/settings/tokens")
    print()
    
    current_key = os.getenv("HUGGINGFACE_API_KEY")
    if current_key and current_key != "your_huggingface_api_key_here":
        print(f"✅ 已检测到HuggingFace API密钥: {current_key[:8]}...")
        choice = input("是否要更新API密钥？(y/N): ").strip().lower()
        if choice != 'y':
            return current_key
    
    api_key = input("请输入HuggingFace API密钥: ").strip()
    
    if not api_key:
        print("❌ API密钥不能为空")
        return None
    
    if api_key == "your_huggingface_api_key_here":
        print("❌ 请使用真实的API密钥，而不是占位符")
        return None
    
    os.environ["HUGGINGFACE_API_KEY"] = api_key
    print(f"✅ HuggingFace API密钥已设置: {api_key[:8]}...")
    
    return api_key


def test_api_connection(api_type: str, api_key: str):
    """测试API连接"""
    print(f"\n🧪 测试{api_type} API连接...")
    
    if api_type == "doubao":
        try:
            # 导入并测试豆包API
            from brain_agent import IntentEngine
            engine = IntentEngine(api_key=api_key)
            result = engine.test_connection()
            
            if result["success"]:
                print("✅ 豆包API连接成功！")
                return True
            else:
                print(f"❌ 豆包API连接失败: {result.get('error', '未知错误')}")
                return False
                
        except Exception as e:
            print(f"❌ 豆包API测试异常: {e}")
            return False
    
    elif api_type == "openai":
        try:
            import requests
            headers = {"Authorization": f"Bearer {api_key}"}
            response = requests.get("https://api.openai.com/v1/models", headers=headers)
            
            if response.status_code == 200:
                print("✅ OpenAI API连接成功！")
                return True
            else:
                print(f"❌ OpenAI API连接失败: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ OpenAI API测试异常: {e}")
            return False
    
    elif api_type == "huggingface":
        try:
            import requests
            headers = {"Authorization": f"Bearer {api_key}"}
            response = requests.get("https://huggingface.co/api/whoami", headers=headers)
            
            if response.status_code == 200:
                print("✅ HuggingFace API连接成功！")
                return True
            else:
                print(f"❌ HuggingFace API连接失败: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ HuggingFace API测试异常: {e}")
            return False
    
    return False


def save_to_env_file():
    """保存配置到.env文件"""
    print("\n💾 保存配置到.env文件...")
    
    env_content = """# Emoji 虚拟人桌面助手 - 环境变量配置
# 请填入你的API密钥

# OpenAI API配置
OPENAI_API_KEY={openai_key}

# HuggingFace API配置
HUGGINGFACE_API_KEY={huggingface_key}

# 豆包API配置（Brain Agent使用）
DOUBAO_API_KEY={doubao_key}

# 其他配置（可选）
DEBUG_MODE=true
LOG_LEVEL=DEBUG
""".format(
        openai_key=os.getenv("OPENAI_API_KEY", "your_openai_api_key_here"),
        huggingface_key=os.getenv("HUGGINGFACE_API_KEY", "your_huggingface_api_key_here"),
        doubao_key=os.getenv("DOUBAO_API_KEY", "your_doubao_api_key_here")
    )
    
    try:
        with open(".env", "w", encoding="utf-8") as f:
            f.write(env_content)
        print("✅ 配置已保存到.env文件")
        return True
    except Exception as e:
        print(f"❌ 保存.env文件失败: {e}")
        return False


def main():
    """主函数"""
    print("🚀 Emoji AI Assistant - API配置工具")
    print("=" * 50)
    print("此工具将帮助您配置各种API密钥")
    print()
    
    # 设置豆包API（Brain Agent必需）
    doubao_key = setup_doubao_api()
    if doubao_key:
        test_api_connection("doubao", doubao_key)
    
    # 设置其他API（可选）
    print("\n" + "=" * 50)
    print("其他API配置（可选）")
    print("=" * 50)
    
    choice = input("是否配置OpenAI API？(y/N): ").strip().lower()
    if choice == 'y':
        openai_key = setup_openai_api()
        if openai_key:
            test_api_connection("openai", openai_key)
    
    choice = input("是否配置HuggingFace API？(y/N): ").strip().lower()
    if choice == 'y':
        huggingface_key = setup_huggingface_api()
        if huggingface_key:
            test_api_connection("huggingface", huggingface_key)
    
    # 保存配置
    print("\n" + "=" * 50)
    save_choice = input("是否保存配置到.env文件？(Y/n): ").strip().lower()
    if save_choice != 'n':
        save_to_env_file()
    
    print("\n🎉 API配置完成！")
    print("现在可以运行 test_brain_agent.py 来测试Brain Agent功能")


if __name__ == "__main__":
    main() 