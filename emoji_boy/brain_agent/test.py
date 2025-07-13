#!/usr/bin/env python3
"""
Brain Agent 统一测试入口

整合所有测试功能，提供统一的测试接口。
支持快速测试、交互式测试、完整测试等多种模式。
"""

import os
import sys
import argparse
import time
import json
from typing import List, Dict, Any

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# 检查必要的依赖
def check_dependencies():
    """检查必要的依赖包"""
    missing_deps = []
    
    try:
        import requests
    except ImportError:
        missing_deps.append("requests")
    
    try:
        from dotenv import load_dotenv
    except ImportError:
        missing_deps.append("python-dotenv")
    
    if missing_deps:
        print("❌ 缺少必要的依赖包:")
        for dep in missing_deps:
            print(f"   - {dep}")
        print("\n请运行以下命令安装依赖:")
        print("   pip install " + " ".join(missing_deps))
        print("\n或者使用 test.sh 脚本自动安装依赖:")
        print("   ./test.sh quick")
        sys.exit(1)

# 检查依赖
check_dependencies()

# 尝试加载.env文件
env_file = os.path.join(project_root, ".env")
if os.path.exists(env_file):
    try:
        from dotenv import load_dotenv
        load_dotenv(env_file)
        print(f"✅ 已加载.env文件: {env_file}")
    except ImportError:
        print("⚠️  未安装python-dotenv，跳过.env文件加载")

try:
    from config import get_api_key
    from brain_agent import IntentEngine, create_engine
    from brain_agent.plugin_registry import PluginRegistry
    from brain_agent.plugins import (
        SearchPlugin, 
        ChatPlugin, 
        ConfigPlugin, 
        HelpPlugin, 
        MeditationPlugin,
        SystemPlugin
    )
except ImportError as e:
    print(f"❌ 导入模块失败: {e}")
    print("请确保在正确的虚拟环境中运行，或使用 test.sh 脚本:")
    print("   ./test.sh quick")
    sys.exit(1)


class BrainAgentTester:
    """Brain Agent 测试器"""
    
    def __init__(self):
        """初始化测试器"""
        self.api_key = None
        self.engine = None
        self.registry = None
        self.test_results = []
        
    def setup(self):
        """设置测试环境"""
        print("🔧 设置测试环境...")
        
        # 获取API密钥
        self.api_key = get_api_key("doubao")
        if not self.api_key or self.api_key == "your_doubao_api_key_here":
            print("❌ 未找到豆包API密钥")
            print("请使用以下方法之一设置API密钥:")
            print("1. 环境变量: export DOUBAO_API_KEY='your_api_key'")
            print("2. .env文件: 在项目根目录创建.env文件")
            print("3. 配置脚本: cd .. && python setup_api.py")
            return False
        
        print(f"✅ API密钥已配置: {self.api_key[:10]}...")
        
        # 创建意图引擎
        try:
            self.engine = create_engine(api_key=self.api_key, auto_register_skills=True)
            print("✅ 意图引擎创建成功")
        except Exception as e:
            print(f"❌ 意图引擎创建失败: {e}")
            return False
        
        # 创建插件注册表
        self.registry = PluginRegistry()
        
        # 注册所有插件
        plugins = [
            SearchPlugin(),
            ChatPlugin(),
            ConfigPlugin(),
            HelpPlugin(),
            MeditationPlugin(),
            SystemPlugin()
        ]
        
        for plugin in plugins:
            self.registry.register_plugin(plugin)
        
        print(f"✅ 已注册 {len(plugins)} 个插件")
        return True
    
    def test_api_connection(self):
        """测试API连接"""
        print("\n🔗 测试API连接...")
        
        try:
            result = self.engine.test_connection()
            if result["success"]:
                print("✅ API连接测试成功")
                print(f"   模型: {result.get('model', 'unknown')}")
                print(f"   响应时间: {result.get('response_time', 0):.2f}秒")
                return True
            else:
                print(f"❌ API连接测试失败: {result.get('error', 'unknown error')}")
                return False
        except Exception as e:
            print(f"❌ API连接测试异常: {e}")
            return False
    
    def quick_test(self):
        """快速测试 - 只测试意图识别"""
        print("\n⚡ 快速测试 - 意图识别")
        print("=" * 50)
        
        # 从test_vectors.txt读取测试案例
        test_messages = self._load_test_vectors()
        if not test_messages:
            print("❌ 无法加载测试向量文件")
            return False
        
        print(f"🔍 测试 {len(test_messages)} 条消息的意图识别:")
        print("-" * 50)
        
        success_count = 0
        total_time = 0
        
        for i, message in enumerate(test_messages, 1):
            print(f"\n{i:2d}. 消息: {message}")
            
            try:
                start_time = time.time()
                
                # 识别意图
                intent_data = self.engine.recognize_intent(message)
                
                # 显示结果
                intent_type = intent_data.get("intent_type", "unknown")
                confidence = intent_data.get("confidence", 0)
                search_query = intent_data.get("search_query", "")
                
                response_time = time.time() - start_time
                total_time += response_time
                
                print(f"   意图类型: {intent_type}")
                print(f"   置信度: {confidence:.2f}")
                print(f"   响应时间: {response_time:.3f}秒")
                
                if search_query:
                    print(f"   搜索查询: {search_query}")
                
                success_count += 1
                    
            except Exception as e:
                print(f"   ❌ 识别失败: {e}")
        
        # 显示统计信息
        stats = self.engine.get_stats()
        print(f"\n📊 测试统计:")
        print(f"   成功识别: {success_count}/{len(test_messages)}")
        print(f"   平均响应时间: {total_time/len(test_messages):.3f}秒")
        print(f"   总请求数: {stats.get('total_requests', 0)}")
        print(f"   缓存命中: {stats.get('cache_hits', 0)}")
        print(f"   成功率: {stats.get('success_rate', 0):.2%}")
        
        print("\n✅ 快速测试完成！")
        return success_count == len(test_messages)
        
        print(f"🔍 测试 {len(test_messages)} 条消息的意图识别:")
        print("-" * 50)
        
        success_count = 0
        total_time = 0
        
        for i, message in enumerate(test_messages, 1):
            print(f"\n{i:2d}. 消息: {message}")
            
            try:
                start_time = time.time()
                
                # 识别意图
                intent_data = self.engine.recognize_intent(message)
                
                # 显示结果
                intent_type = intent_data.get("intent_type", "unknown")
                confidence = intent_data.get("confidence", 0)
                search_query = intent_data.get("search_query", "")
                
                response_time = time.time() - start_time
                total_time += response_time
                
                print(f"   意图类型: {intent_type}")
                print(f"   置信度: {confidence:.2f}")
                print(f"   响应时间: {response_time:.3f}秒")
                
                if search_query:
                    print(f"   搜索查询: {search_query}")
                
                success_count += 1
                    
            except Exception as e:
                print(f"   ❌ 识别失败: {e}")
        
        # 显示统计信息
        stats = self.engine.get_stats()
        print(f"\n📊 测试统计:")
        print(f"   成功识别: {success_count}/{len(test_messages)}")
        print(f"   平均响应时间: {total_time/len(test_messages):.3f}秒")
        print(f"   总请求数: {stats.get('total_requests', 0)}")
        print(f"   缓存命中: {stats.get('cache_hits', 0)}")
        print(f"   成功率: {stats.get('success_rate', 0):.2%}")
        
        print("\n✅ 快速测试完成！")
        return success_count == len(test_messages)
    
    def interactive_test(self):
        """交互式测试"""
        print("\n💬 交互式测试")
        print("=" * 50)
        print("输入消息进行意图识别测试，输入 'quit' 或 'exit' 退出")
        print("输入 'stats' 查看统计信息，输入 'help' 查看帮助")
        print()
        
        while True:
            try:
                message = input("请输入消息: ").strip()
                
                if not message:
                    continue
                
                if message.lower() in ['quit', 'exit', 'q']:
                    print("👋 退出交互式测试")
                    break
                
                if message.lower() == 'stats':
                    self._show_stats()
                    continue
                
                if message.lower() == 'help':
                    self._show_help()
                    continue
                
                # 处理消息
                start_time = time.time()
                result = self.engine.process_message(message)
                processing_time = time.time() - start_time
                
                # 显示结果
                self._display_result(message, result, processing_time)
                
            except KeyboardInterrupt:
                print("\n👋 退出交互式测试")
                break
            except Exception as e:
                print(f"❌ 处理失败: {e}")
    
    def full_test(self):
        """完整测试 - 测试意图识别和执行"""
        print("\n🧪 完整测试 - 意图识别和执行")
        print("=" * 50)
        
        # 1. API连接测试
        print("1️⃣ API连接测试")
        if not self.test_api_connection():
            print("❌ API连接测试失败，跳过后续测试")
            return False
        
        # 2. 从test_vectors.txt读取测试案例
        print("\n2️⃣ 加载测试向量")
        test_messages = self._load_test_vectors()
        if not test_messages:
            print("❌ 无法加载测试向量文件")
            return False
        
        print(f"   加载了 {len(test_messages)} 条测试案例")
        
        # 3. 意图识别和执行测试
        print("\n3️⃣ 意图识别和执行测试")
        print("-" * 50)
        
        success_count = 0
        total_time = 0
        
        for i, message in enumerate(test_messages, 1):
            print(f"\n{i:2d}. 消息: {message}")
            
            try:
                start_time = time.time()
                
                # 处理消息（包含意图识别和执行）
                result = self.engine.process_message(message)
                
                processing_time = time.time() - start_time
                total_time += processing_time
                
                # 显示意图识别结果
                intent_data = result.get("intent_data", {})
                intent_type = intent_data.get("intent_type", "unknown")
                confidence = intent_data.get("confidence", 0)
                
                print(f"   意图类型: {intent_type}")
                print(f"   置信度: {confidence:.2f}")
                print(f"   处理时间: {processing_time:.3f}秒")
                
                # 显示执行结果
                if result.get("success", False):
                    print(f"   ✅ 执行成功")
                    print(f"   技能名称: {result.get('skill_name', 'unknown')}")
                    print(f"   响应类型: {result.get('response_type', 'unknown')}")
                    print(f"   响应内容: {result.get('response', '')}")
                    
                    # 显示生成的代码（如果有）
                    if 'code' in result:
                        print(f"   生成代码: {result['code']}")
                    
                    success_count += 1
                else:
                    print(f"   ❌ 执行失败")
                    print(f"   错误信息: {result.get('error', '未知错误')}")
                    
            except Exception as e:
                print(f"   ❌ 处理异常: {e}")
        
        # 4. 统计信息
        print(f"\n4️⃣ 测试统计")
        print("-" * 50)
        
        stats = self.engine.get_stats()
        print(f"   成功处理: {success_count}/{len(test_messages)}")
        print(f"   平均处理时间: {total_time/len(test_messages):.3f}秒")
        print(f"   总请求数: {stats.get('total_requests', 0)}")
        print(f"   缓存命中率: {stats.get('cache_hit_rate', 0):.2%}")
        print(f"   成功率: {stats.get('success_rate', 0):.2%}")
        print(f"   代码执行次数: {stats.get('code_executions', 0)}")
        print(f"   技能匹配次数: {stats.get('skill_matches', 0)}")
        
        print("\n✅ 完整测试完成！")
        return success_count > 0
    
    def _show_stats(self):
        """显示统计信息"""
        stats = self.engine.get_stats()
        plugin_stats = self.registry.get_plugin_stats()
        
        print("\n📊 统计信息:")
        print(f"   意图引擎:")
        print(f"     总请求数: {stats.get('total_requests', 0)}")
        print(f"     缓存命中率: {stats.get('cache_hit_rate', 0):.2%}")
        print(f"     成功率: {stats.get('success_rate', 0):.2%}")
        print(f"     平均响应时间: {stats.get('average_response_time', 0):.3f}秒")
        
        print(f"   插件系统:")
        print(f"     总插件数: {plugin_stats.get('plugin_count', 0)}")
        print(f"     执行成功率: {plugin_stats.get('success_rate', 0):.2%}")
        print(f"     平均执行时间: {plugin_stats.get('average_execution_time', 0):.3f}秒")
        
        if plugin_stats.get('most_used_plugin'):
            most_used = plugin_stats['most_used_plugin']
            print(f"     最常用插件: {most_used['name']} ({most_used['usage_count']}次)")
    
    def _show_help(self):
        """显示帮助信息"""
        print("\n📖 帮助信息:")
        print("   输入消息进行意图识别测试")
        print("   支持的命令:")
        print("     - quit/exit/q: 退出测试")
        print("     - stats: 查看统计信息")
        print("     - help: 显示此帮助")
        print("   支持的意图类型:")
        print("     - search: 搜索相关")
        print("     - chat: 聊天交流")
        print("     - config: 配置设置")
        print("     - help: 帮助请求")
        print("     - meditation: 冥想相关")
        print("     - system: 系统操作")
    
    def _load_test_vectors(self) -> List[str]:
        """从test_vectors.txt加载测试向量"""
        try:
            vector_file = "test_vectors.txt"
            if not os.path.exists(vector_file):
                print(f"❌ 测试向量文件不存在: {vector_file}")
                return []
            
            with open(vector_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 解析测试向量
            test_messages = []
            lines = content.split('\n')
            
            for line in lines:
                line = line.strip()
                # 跳过空行和注释行
                if not line or line.startswith('#'):
                    continue
                
                # 提取消息内容（去掉序号）
                if line and line[0].isdigit():
                    # 格式: "1. 今天几号"
                    parts = line.split('.', 1)
                    if len(parts) > 1:
                        message = parts[1].strip()
                        if message:
                            test_messages.append(message)
                else:
                    # 直接是消息内容
                    test_messages.append(line)
            
            print(f"✅ 成功加载 {len(test_messages)} 条测试向量")
            return test_messages
            
        except Exception as e:
            print(f"❌ 加载测试向量失败: {e}")
            return []
    
    def _display_result(self, message: str, result: Dict[str, Any], processing_time: float):
        """显示处理结果"""
        print(f"\n📝 处理结果:")
        print(f"   消息: {message}")
        print(f"   处理时间: {processing_time:.3f}秒")
        
        intent_data = result.get("intent_data", {})
        plugin_result = result.get("plugin_result", {})
        
        print(f"   意图识别:")
        print(f"     类型: {intent_data.get('intent_type', 'unknown')}")
        print(f"     置信度: {intent_data.get('confidence', 0):.2f}")
        
        if intent_data.get('search_query'):
            print(f"     搜索查询: {intent_data['search_query']}")
        
        print(f"   插件执行:")
        print(f"     成功: {result.get('success', False)}")
        print(f"     插件: {plugin_result.get('plugin_name', 'unknown')}")
        
        if plugin_result.get('message'):
            print(f"     响应: {plugin_result['message']}")
        
        if plugin_result.get('error'):
            print(f"     错误: {plugin_result['error']}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="Brain Agent 测试工具")
    parser.add_argument("--quick", action="store_true", help="快速测试")
    parser.add_argument("--interactive", action="store_true", help="交互式测试")
    parser.add_argument("--full", action="store_true", help="完整测试")
    parser.add_argument("--all", action="store_true", help="运行所有测试")
    parser.add_argument("--api-test", action="store_true", help="仅测试API连接")
    
    args = parser.parse_args()
    
    # 如果没有指定参数，默认运行快速测试
    if not any([args.quick, args.interactive, args.full, args.all, args.api_test]):
        args.quick = True
    
    tester = BrainAgentTester()
    
    if not tester.setup():
        sys.exit(1)
    
    success = True
    
    try:
        if args.api_test:
            success = tester.test_api_connection()
        
        elif args.quick:
            success = tester.quick_test()
        
        elif args.interactive:
            tester.interactive_test()
        
        elif args.full:
            success = tester.full_test()
        
        elif args.all:
            print("🚀 运行所有测试")
            success = tester.quick_test() and tester.full_test()
        
    except KeyboardInterrupt:
        print("\n👋 测试被用户中断")
        sys.exit(0)
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {e}")
        sys.exit(1)
    
    if success:
        print("\n🎉 所有测试通过！")
        sys.exit(0)
    else:
        print("\n⚠️  部分测试失败")
        sys.exit(1)


if __name__ == "__main__":
    main() 