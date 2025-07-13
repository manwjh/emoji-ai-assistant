# Brain Agent - 类脑意图识别与执行系统 (v0.2.2)

**去他大爷的MCP，做个类脑Agent试试！** 🚀

Brain Agent 是一个模仿人脑对外界输入反应模式的智能系统，采用类脑架构设计。它能够像人脑一样识别用户意图，并通过相应的技能模块进行执行。支持动态代码生成与安全执行，实现真正的类脑感知-认知-执行循环。

## 🧠 核心理念

### 类脑架构设计
- **感知-认知-执行循环**: 模仿人脑的信息处理流程
- **技能网络系统**: 类似人脑的技能网络，支持多种能力
- **记忆机制**: 模拟人脑的记忆和回忆过程
- **行为模式学习**: 基于交互历史优化反应策略
- **自适应执行**: 根据上下文调整执行策略

### 人脑反应模式
- **信息获取需求**: 类似人脑的求知欲（搜索意图）
- **社交交流需求**: 类似人脑的社交本能（聊天意图）
- **系统调整需求**: 类似人脑的适应能力（配置意图）
- **学习指导需求**: 类似人脑的学习能力（帮助意图）
- **专注训练需求**: 类似人脑的专注力（冥想意图）
- **系统操作需求**: 类似人脑的自主控制（系统意图）
- **未知需求**: 类似人脑的困惑状态（未知意图）

## 🚀 快速开始

### 测试 Brain Agent

#### 使用Shell脚本（推荐）

```bash
# 快速测试（推荐）- 自动设置虚拟环境
./test.sh quick

# 交互式测试 - 实时输入消息测试
./test.sh interactive

# 完整测试 - 包含API连接和准确性测试
./test.sh full

# 所有测试 - 运行快速测试和完整测试
./test.sh all

# API连接测试 - 仅测试API连接
./test.sh api

# 查看帮助
./test.sh help
```

#### 直接使用Python

```bash
# 快速测试（推荐）- 测试10条预定义消息
python test.py --quick

# 交互式测试 - 实时输入消息测试
python test.py --interactive

# 完整测试 - 包含API连接和准确性测试
python test.py --full

# 所有测试 - 运行快速测试和完整测试
python test.py --all

# API连接测试 - 仅测试API连接
python test.py --api-test
```

### Shell脚本功能

`test.sh` 脚本提供以下自动化功能：

- ✅ **自动检查Python环境** - 检测Python3或Python
- ✅ **自动管理虚拟环境** - 检查、创建、激活虚拟环境
- ✅ **自动安装依赖** - 安装requirements.txt和必要包
- ✅ **自动检查API密钥** - 检查环境变量和.env文件
- ✅ **彩色输出** - 友好的彩色提示信息
- ✅ **错误处理** - 完善的错误处理和用户提示

### API密钥配置

Brain Agent 需要豆包API密钥进行类脑意图识别：

```bash
# 方法1: 环境变量
export DOUBAO_API_KEY="your_doubao_api_key_here"

# 方法2: .env文件
echo "DOUBAO_API_KEY=your_doubao_api_key_here" > ../.env

# 方法3: 配置脚本
cd .. && python setup_api.py
```

### 测试示例

```bash
# 1. 设置API密钥
export DOUBAO_API_KEY="your_api_key"

# 2. 运行快速测试
./test.sh quick

# 输出示例:
# ⚡ 快速测试
# ==============================
# 🔍 测试 10 条消息的意图识别:
# --------------------------------------------------
#  1. 消息: 搜索Python教程
#     意图类型: search
#     置信度: 0.95
#     搜索查询: Python教程
#     响应时间: 0.234秒
```

## 🧪 测试功能

### 类脑意图识别测试
- **信息获取需求**: 包含"搜索"、"查找"、"如何"等关键词
- **社交交流需求**: 问候、感谢、情感表达
- **系统调整需求**: 设置、配置、API相关
- **学习指导需求**: 帮助、说明、指南
- **专注训练需求**: 冥想、编码、A2B/B2C
- **系统操作需求**: 时间查询、系统信息、数学计算等
- **未知需求**: 无法识别的意图类型

### 性能指标
- **响应时间**: 类脑感知-认知-执行循环耗时
- **准确率**: 意图识别正确率
- **记忆效果**: 重复请求的记忆命中率
- **API连接**: 认知API连接状态

## 🏗️ 类脑架构设计

```
brain_agent/
├── __init__.py              # 模块初始化
├── intent_engine.py         # 类脑意图识别引擎
├── plugin_registry.py       # 技能网络系统
├── plugins/                 # 技能模块目录
│   ├── __init__.py         # 技能模块初始化
│   ├── base_plugin.py      # 技能模块基类
│   ├── search_plugin.py    # 信息获取技能
│   ├── chat_plugin.py      # 社交交流技能
│   ├── config_plugin.py    # 系统调整技能
│   ├── help_plugin.py      # 学习指导技能
│   ├── meditation_plugin.py # 专注训练技能
│   └── system_plugin.py    # 系统操作技能
├── test.py                 # 测试脚本
├── test.sh                 # 测试Shell脚本
└── README.md               # 本文档
```

## 🚀 核心特性

### 1. 类脑意图识别
- 模仿人脑的感知和认知过程
- 支持7种意图类型：信息获取、社交交流、系统调整、学习指导、专注训练、系统操作、未知意图
- 高精度识别和置信度计算
- 类脑记忆机制（LRU记忆）
- 平均响应时间监控
- 动态代码生成与安全执行
- AI初始对话由大模型根据人格和记忆自动生成，不再使用固定开场白。

### 2. 技能网络系统
- 模块化设计，每个功能都是独立技能模块
- 可扩展性，轻松添加新技能
- 优先级管理，技能按优先级执行
- 热插拔，支持动态启用/禁用技能
- 技能使用统计和性能监控

### 3. 类脑优化机制
- LRU记忆机制减少重复请求
- 行为模式统计提供详细执行信息
- 错误处理和重试机制
- 自适应执行支持
- 技能验证和完整性检查

### 4. 完善的日志系统
- 分级日志记录（INFO、DEBUG、WARNING、ERROR）
- 详细的执行追踪
- 性能指标记录
- 错误诊断信息

## 📦 技能网络系统

### 技能模块基类 (BasePlugin)
所有技能模块都继承自 `BasePlugin`，提供统一的接口：

```python
from brain_agent.plugins.base_plugin import BasePlugin, PluginPriority

class MySkill(BasePlugin):
    def __init__(self):
        super().__init__(
            name="my_skill",
            description="我的自定义技能",
            priority=PluginPriority.NORMAL
        )
    
    def can_handle(self, intent_data):
        # 判断是否能处理该意图
        return intent_data.get("intent_type") == "my_intent"
    
    def handle(self, intent_data, context=None):
        # 处理意图
        return {
            "success": True,
            "message": "处理完成"
        }
```

### 内置技能模块

#### 1. 信息获取技能 (SearchPlugin)
- **功能**: 处理信息获取相关的用户意图
- **支持**: 关键词搜索、问题搜索、信息查找
- **优先级**: HIGH
- **意图类型**: search

#### 2. 社交交流技能 (ChatPlugin)
- **功能**: 处理社交交流、问候、情感交流
- **支持**: 问候语、告别语、感谢语、情感回应
- **优先级**: NORMAL
- **意图类型**: chat

#### 3. 系统调整技能 (ConfigPlugin)
- **功能**: 处理系统调整、设置API、修改参数
- **支持**: API密钥设置、基础URL设置、配置管理
- **优先级**: HIGH
- **意图类型**: config

#### 4. 学习指导技能 (HelpPlugin)
- **功能**: 处理学习指导、查看说明、了解功能
- **支持**: 分类帮助、完整帮助、使用指南
- **优先级**: NORMAL
- **意图类型**: help

#### 5. 专注训练技能 (MeditationPlugin)
- **功能**: 处理专注训练、记忆编码、A2B/B2C
- **支持**: A2B编码、B2C编码、自动编码、专注会话
- **优先级**: HIGH
- **意图类型**: meditation

## 🔧 使用方法

### 1. 基本使用

```python
from brain_agent import create_brain

# 快速创建类脑意图识别系统（自动注册所有技能）
brain = create_brain(api_key="your_doubao_api_key")

# 处理消息
result = brain.process_message("搜索Python教程")
print(result)
```

### 2. 高级使用

```python
from brain_agent import IntentEngine, PluginRegistry
from brain_agent.plugins import SearchPlugin, ChatPlugin

# 创建类脑意图识别引擎
brain = IntentEngine(api_key="your_doubao_api_key")

# 创建技能网络系统
skill_network = PluginRegistry()

# 注册技能模块
skill_network.register_plugin(SearchPlugin())
skill_network.register_plugin(ChatPlugin())

# 处理消息
result = brain.process_message("搜索Python教程")
print(result)
```

### 3. 自定义技能模块

```python
from brain_agent.plugins.base_plugin import BasePlugin, PluginPriority

class CustomSkill(BasePlugin):
    def __init__(self):
        super().__init__(
            name="custom_skill",
            description="自定义技能模块",
            priority=PluginPriority.NORMAL
        )
    
    def can_handle(self, intent_data):
        return intent_data.get("intent_type") == "custom"
    
    def handle(self, intent_data, context=None):
        return {
            "success": True,
            "message": "自定义处理完成"
        }
```

### 4. 技能网络管理

```python
# 获取所有技能模块
skills = skill_network.get_all_plugins()

# 启用/禁用技能模块
skill_network.enable_plugin("search_plugin")
skill_network.disable_plugin("chat_plugin")

# 获取技能网络统计
stats = skill_network.get_plugin_stats()

# 验证技能模块完整性
validation = skill_network.validate_plugins()
```

## 🔑 API配置

Brain Agent 使用豆包API进行类脑意图识别。需要配置 `DOUBAO_API_KEY` 环境变量：

### 方法1: 环境变量
```bash
export DOUBAO_API_KEY="your_doubao_api_key_here"
```

### 方法2: 配置文件
创建 `.env` 文件：
```
DOUBAO_API_KEY=your_doubao_api_key_here
```

### 方法3: 使用配置脚本
```bash
python setup_api.py
```

### 方法4: 代码中设置
```python
import os
os.environ["DOUBAO_API_KEY"] = "your_doubao_api_key_here"
```

## 🧪 测试

### 运行基本测试
```bash
# 使用Shell脚本（推荐）
./test.sh quick

# 或直接使用Python
python test.py --quick
```

### 运行完整测试
```bash
# 使用Shell脚本
./test.sh full

# 或直接使用Python
python test.py --full
```

### 交互式测试
```bash
# 使用Shell脚本
./test.sh interactive

# 或直接使用Python
python test.py --interactive
```

## 📊 统计信息

Brain Agent 提供详细的行为模式统计信息：

```python
# 获取类脑意图识别统计
stats = brain.get_stats()
print(f"总请求数: {stats['total_requests']}")
print(f"记忆命中率: {stats['cache_hit_rate']:.2%}")
print(f"成功率: {stats['success_rate']:.2%}")
print(f"平均响应时间: {stats['average_response_time']:.3f}秒")

# 获取技能网络统计
skill_stats = skill_network.get_plugin_stats()
print(f"总技能模块数: {skill_stats['plugin_count']}")
print(f"执行成功率: {skill_stats['success_rate']:.2%}")
print(f"平均执行时间: {skill_stats['average_execution_time']:.3f}秒")
```

## 🔄 集成到主项目

将 Brain Agent 集成到主项目中：

```python
# 在 main.py 中
from brain_agent import create_brain

# 初始化类脑意图识别系统
brain = create_brain()

# 处理用户输入
def handle_user_input(message):
    result = brain.process_message(message)
    return result
```

## 🛠️ 开发指南

### 添加新技能模块

1. 创建技能模块文件 `plugins/my_skill.py`
2. 继承 `BasePlugin` 类
3. 实现 `can_handle` 和 `handle` 方法
4. 在 `plugins/__init__.py` 中导入技能模块
5. 注册技能模块到系统中

### 扩展意图类型

1. 在 `intent_engine.py` 中添加新的意图类型
2. 更新类脑意图识别提示词
3. 创建对应的技能模块
4. 更新测试用例

### 性能优化

1. 调整记忆容量和TTL
2. 优化技能模块优先级
3. 实现异步处理
4. 添加监控和日志

### 调试技巧

1. 启用DEBUG日志级别
2. 使用交互式测试模式
3. 查看详细的行为模式统计信息
4. 验证技能模块完整性

## 📝 更新日志

### v2.0.0 (最新) - 类脑架构版本
- 🧠 **类脑架构设计**: 模仿人脑的感知-认知-执行循环
- 🎯 **技能网络系统**: 类似人脑的技能网络，支持多种能力
- 💾 **类脑记忆机制**: 模拟人脑的记忆和回忆过程
- 📈 **行为模式学习**: 基于交互历史优化反应策略
- 🔄 **自适应执行**: 根据上下文调整执行策略
- 📊 **完善统计系统**: 详细的行为模式统计和性能监控
- 🧪 **增强测试功能**: 支持多种测试模式和交互式测试
- 📚 **完善文档**: 详细的类脑架构说明和使用指南

### v1.0.0 - 基础版本
- 🎉 初始版本发布
- 🧠 实现核心意图识别引擎
- 🔌 提供5个基础技能模块
- 🏗️ 支持技能网络架构
- 📊 添加统计和监控功能
- 🚀 优化记忆机制（LRU记忆）
- 📝 完善日志系统
- 🧪 增强测试功能
- 🔧 改进错误处理
- 📚 完善文档

## 🤝 贡献

欢迎贡献代码！请遵循以下步骤：

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

### 开发环境设置

```bash
# 克隆项目
git clone <repository_url>
cd emoji-ai-assistant

# 设置虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 运行测试
cd emoji_boy/brain_agent
./test.sh quick
```

## 📄 许可证

本项目采用 MIT 许可证。详见 [LICENSE](../LICENSE) 文件。

## 🆘 支持

如果遇到问题，请：

1. 查看本文档
2. 运行测试脚本
3. 检查API配置
4. 提交 Issue

### 常见问题

**Q: API密钥未设置怎么办？**
A: 请参考"API配置"部分，使用环境变量、.env文件或配置脚本设置API密钥。

**Q: 测试失败怎么办？**
A: 请检查Python环境、依赖包、API密钥配置，或使用 `./test.sh help` 查看帮助。

**Q: 如何添加自定义技能模块？**
A: 请参考"开发指南"部分的"添加新技能模块"说明。

**Q: 什么是类脑架构？**
A: 类脑架构是模仿人脑信息处理方式的系统设计，包括感知、认知、执行等环节。

---

**Brain Agent v2.0.0** - 让AI更智能，让交互更自然！🧠✨ 