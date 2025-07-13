# Emoji AI Assistant v0.2.2

**去他大爷的RAG、MCP、Manus，做个类脑Agent试试！** 🚀

本版本为类脑Agent系统 + 闭环人格演化重大升级版，详见[CHANGELOG.md](CHANGELOG.md)

一个极简但功能完整的桌面Emoji虚拟人助手，具备桌面浮动、智能对话、类脑记忆系统和类脑意图识别系统等功能。
<img width="503" height="597" alt="image" src="https://github.com/user-attachments/assets/7d951f2e-04a6-424c-ad22-faa7d8773ba5" />

## 🎯 功能特性

- 🎭 **桌面浮动Emoji虚拟人** - 可爱的😺表情，可拖拽移动，总在最前显示
- 💬 **智能对话系统** - 集成OpenAI/HuggingFace API，支持上下文记忆，AI初始对话由大模型根据人格和记忆自动生成，不再使用固定开场白
- 🧠 **MemABC记忆系统** - 实验性类脑记忆架构，支持记忆编码和检索
- 🧠 **类脑Agent系统** - 实验性类脑意图架构，支持意图识别+能力执行+动态代码生成
- 🧠 **闭环人格演化** - 深层记忆影响AI人格，形成经历→记忆→人格→经历的闭环
- 🎨 **现代化UI** - 基于PyQt5的优雅界面，支持动画效果
- 🔧 **配置管理** - 灵活的配置系统，支持多种API和自定义设置
- 🚀 **一键启动** - 完整的启动脚本，自动环境配置

## 🚀 快速开始

### 1. 克隆项目
```bash
git clone <repository-url>
cd emoji-ai-assistant
```

### 2. 安装依赖
```bash
cd emoji_boy
pip install -r requirements.txt
```

### 3. 配置API密钥（可选）
```bash
cp env_example.txt .env
```

编辑 `.env` 文件：
```
OPENAI_API_KEY=your_openai_api_key_here
HUGGINGFACE_API_KEY=your_huggingface_api_key_here
```

**注意**：如果不配置API密钥，程序会使用内置的Mock模式。

### 4. 启动程序

**方法一：使用启动脚本（推荐）**
```bash
./start.sh
```

**方法二：直接运行**
```bash
python run.py
```

## 📖 使用说明

### 基本操作
- **点击Emoji** - 打开聊天对话框，开始对话
- **拖拽Emoji** - 移动助手位置到屏幕任意位置
- **Ctrl+C** - 优雅退出程序

### 对话功能
- 支持多轮对话，保持上下文记忆
- 集成多种AI模型（OpenAI GPT、HuggingFace、Mock模式）
- 智能回复，带有emoji表情
- 对话历史自动保存和管理
- **类脑意图识别**: 自动识别用户意图并执行相应功能
- **动态代码生成**: 根据意图自动生成并安全执行Python代码
- **功能自动执行**: 时间查询、系统信息、数学计算、搜索等
- **AI初始对话由大模型根据人格和记忆自动生成，不再使用固定开场白**

### MemABC记忆系统
- **MemA**: 原始记忆存储（每日文件）
- **MemB**: 处理后的分类记忆
- **MemC**: 长期记忆存储和AI潜意识
- 支持A2B、A2C、B2C编码转换
- **memC_to_system_prompt**: 深层记忆转换为AI人格特征
- 自动备份和记忆管理
- **自动编码调度**: 每天凌晨3点自动执行编码，程序关闭时静默执行（如果当天未执行）
- **闭环人格演化**: 经历→深层记忆→重塑人格→影响后续经历

### 🧠 类脑Agent系统
- **意图识别**: 支持7种意图类型（search、chat、config、help、meditation、system、unknown）
- **技能网络**: 6个核心插件（system、chat、search、config、help、meditation）
- **动态执行**: 根据意图自动生成并安全执行Python代码
- **感知-认知-执行循环**: 模仿人脑的信息处理流程
- **记忆机制**: 模拟人脑的记忆和回忆过程
- **行为模式学习**: 基于交互历史优化反应策略

## 🏗️ 项目结构

```
emoji-ai-assistant/
├── emoji_boy/                    # 主程序目录
│   ├── ui/                       # 用户界面模块
│   ├── interaction/              # 交互模块
│   ├── core/                     # 核心模块
│   ├── brain_agent/              # 🧠 类脑Agent系统
│   │   ├── intent_engine.py      # 意图识别引擎
│   │   ├── plugin_registry.py    # 技能网络注册表
│   │   ├── plugins/              # 技能插件目录
│   │   │   ├── system_plugin.py  # 系统操作插件
│   │   │   ├── chat_plugin.py    # 聊天交流插件
│   │   │   ├── search_plugin.py  # 搜索功能插件
│   │   │   ├── config_plugin.py  # 配置管理插件
│   │   │   ├── help_plugin.py    # 帮助指导插件
│   │   │   └── meditation_plugin.py # 冥想引导插件
│   │   ├── test.py               # 测试框架
│   │   ├── test.sh               # 自动化测试脚本
│   │   └── test_vectors.txt      # 测试向量数据集
│   ├── MemABC/                   # 记忆系统
│   │   ├── memC_to_system_prompt.py  # 深层记忆转系统提示词
│   │   ├── memC_to_system_prompt.sh  # 自动化脚本
│   │   └── systemprompt.txt          # 生成的AI人格定义
│   └── ...                       # 其他配置和脚本文件
├── scripts/                      # 工具脚本
├── MemABC/                       # 根目录记忆系统
└── ...                           # 文档和配置文件
```

## 🛠️ 技术栈

- **Python 3.7+** - 主要编程语言
- **PyQt5** - 现代化GUI框架
- **OpenAI API** - GPT模型支持
- **HuggingFace API** - 开源模型支持

- **requests** - HTTP请求库
- **threading** - 多线程处理

## 📋 开发计划

### v0.2.2 ✅（当前版本）- 初始对话由AI自动生成
- [x] 💬 AI初始对话由大模型根据人格和记忆自动生成，不再使用固定开场白
- [x] 🧠 类脑意图识别引擎
- [x] 🧠 技能网络系统（6个核心插件）
- [x] 🧠 动态代码生成与安全执行
- [x] 🧠 意图识别与执行集成
- [x] 🧠 模块独立性支持
- [x] 🧠 完整的测试框架
- [x] 🧠 自动化测试脚本
- [x] 🧠 兼容性导入系统
- [x] 🧠 API密钥统一管理
- [x] 🧠 安全沙箱执行环境
- [x] 🧠 **memC_to_system_prompt**: 深层记忆转换为AI人格特征
- [x] 🧠 **闭环人格演化**: 经历→深层记忆→重塑人格→影响后续经历
- [x] 🧠 **动态系统提示词**: 每次对话都注入最新的memC潜意识
- [x] 🧠 **人格特征提取**: 从深层记忆中提取行为模式、情感依恋、语言风格等

### v0.1.1 ✅ (历史版本) - 安全增强版
- [x] 桌面浮动Emoji虚拟人
- [x] 智能对话系统（多API支持）
- [x] MemABC记忆系统基础架构
- [x] 聊天状态机和记忆管理
- [x] 配置管理系统
- [x] 完整的启动脚本系统
- [x] 🔐 安全增强：API密钥泄露防护
- [x] 🔐 安全增强：预提交钩子检查
- [x] 🔐 安全增强：安全扫描工具
- [x] 🔐 安全增强：完整的安全文档

### v0.1.0 ✅ (历史版本)
- [x] 桌面浮动Emoji虚拟人
- [x] 智能对话系统（多API支持）
- [x] MemABC记忆系统基础架构
- [x] 聊天状态机和记忆管理
- [x] 配置管理系统
- [x] 完整的启动脚本系统

### 未来计划
- [ ] 🧠 更多意图类型和技能插件
- [ ] 🧠 意图识别准确率优化
- [ ] 🧠 代码生成能力增强
- [ ] 🧠 多模态意图识别（图像、语音）
- [ ] 🧠 分布式技能网络
- [ ] 🧠 类脑学习机制优化
- [ ] 语音识别和语音合成
- [ ] 更多表情动画效果
- [ ] 自定义主题和样式
- [ ] 多语言支持
- [ ] MemABC记忆系统优化
- [ ] 移动端支持

## ⚠️ 注意事项

### 系统要求
- **操作系统**: macOS 10.14+, Windows 10+, Ubuntu 18.04+
- **Python**: 3.7 或更高版本
- **内存**: 至少 512MB 可用内存
- **存储**: 至少 100MB 可用空间

### 安全提醒
- **API费用**: 使用OpenAI API会产生费用，请注意控制使用量

- **数据存储**: 对话历史和记忆数据存储在本地，注意备份
- **API密钥安全**: 请参考 [SECURITY.md](SECURITY.md) 了解如何安全管理API密钥

## 🐛 故障排除

### 常见问题

1. **权限问题**
   ```bash
   # macOS
   sudo chmod +x start.sh
   
   # Linux
   chmod +x start.sh
   ```

2. **依赖安装失败**
   ```bash
   # 升级pip
   python -m pip install --upgrade pip
   
   # 重新安装依赖
   pip install -r requirements.txt --force-reinstall
   ```

3. **PyQt5安装问题**
   ```bash
   # macOS
   brew install pyqt5
   
   # Ubuntu
   sudo apt-get install python3-pyqt5
   ```

4. **API连接失败**
   - 检查网络连接
   - 验证API密钥是否正确
   - 确认API配额是否充足

### 调试模式

设置环境变量启用调试：
```bash
export DEBUG_MODE=true
export LOG_LEVEL=DEBUG
```

### 日志文件

程序运行日志保存在：
- 控制台输出
- 系统日志（macOS/Linux）

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 📝 更新日志

详细的功能更新和修复记录，请查看 [CHANGELOG.md](CHANGELOG.md)

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个项目！

### 贡献指南
1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📞 联系方式

- **项目主页**: [GitHub Repository]
- **问题反馈**: [Issues]
- **功能建议**: [Discussions]

## 🙏 致谢

感谢所有为这个项目做出贡献的开发者和用户！ 
