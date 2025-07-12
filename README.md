# Emoji AI Assistant v0.1.0

一个极简但功能完整的桌面Emoji虚拟人助手，具备桌面浮动、智能对话、情绪检测和类脑记忆系统等功能。

## 🎯 功能特性

- 🎭 **桌面浮动Emoji虚拟人** - 可爱的😺表情，可拖拽移动，总在最前显示
- 💬 **智能对话系统** - 集成OpenAI/HuggingFace API，支持上下文记忆
- 🧠 **MemABC记忆系统** - 实验性类脑记忆架构，支持记忆编码和检索
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
- **键盘输入** - 程序自动检测情绪关键词并给出安慰
- **Ctrl+C** - 优雅退出程序

### 对话功能
- 支持多轮对话，保持上下文记忆
- 集成多种AI模型（OpenAI GPT、HuggingFace、Mock模式）
- 智能回复，带有emoji表情
- 对话历史自动保存和管理

### 情绪检测
程序会实时检测以下情绪关键词：
- **负面情绪**: 烦、累、唉、难过、😢、😭
- **愤怒情绪**: 操、妈的、气死、😠、😡
- **疲惫情绪**: 累、疲惫、困、😴、😪
- **正面情绪**: 开心、高兴、棒、😊、😄

### MemABC记忆系统
- **MemA**: 原始记忆存储（每日文件）
- **MemB**: 处理后的分类记忆
- **MemC**: 长期记忆存储和AI潜意识
- 支持A2B和A2C编码转换
- 自动备份和记忆管理

## 🏗️ 项目结构

```
emoji-ai-assistant/
├── emoji_boy/                    # 主程序目录
│   ├── main.py                   # 主程序入口
│   ├── run.py                    # 启动脚本
│   ├── config.py                 # 配置文件
│   ├── requirements.txt          # Python依赖
│   ├── env_example.txt           # 环境变量模板
│   ├── start.sh                  # 完整启动脚本
│   ├── quick_start.sh            # 快速启动脚本
│   ├── test_venv.sh              # 环境测试脚本
│   ├── emoji_boy.png             # Emoji图标
│   ├── ui/                       # 用户界面模块
│   │   ├── __init__.py
│   │   └── floating_head.py      # 悬浮Emoji窗口
│   ├── interaction/              # 交互模块
│   │   ├── __init__.py
│   │   ├── chat_input.py         # 聊天输入对话框
│   │   ├── chat_state_machine.py # 聊天状态机
│   │   └── emotion_detector.py   # 情绪检测器
│   ├── core/                     # 核心模块
│   │   ├── __init__.py
│   │   ├── llm_client.py         # AI模型客户端
│   │   ├── chat_memory.py        # 聊天记忆管理
│   │   └── config_manager.py     # 配置管理器
│   ├── MemABC/                   # 记忆系统
│   │   ├── README.md             # 记忆系统文档
│   │   ├── a2b.sh                # A到B编码脚本
│   │   ├── a2c.sh                # A到C编码脚本
│   │   ├── encoding_a2b.py       # A到B编码实现
│   │   ├── encoding_a2c.py       # A到C编码实现
│   │   ├── memA/                 # 原始记忆存储
│   │   ├── memB/                 # 处理记忆存储
│   │   └── memC/                 # 长期记忆存储
│   └── venv/                     # Python虚拟环境
├── MemABC/                       # 根目录记忆系统
├── Design Goals.md               # 设计目标文档
├── README.md                     # 项目说明
└── LICENSE                       # 许可证
```

## 🛠️ 技术栈

- **Python 3.7+** - 主要编程语言
- **PyQt5** - 现代化GUI框架
- **OpenAI API** - GPT模型支持
- **HuggingFace API** - 开源模型支持
- **pynput** - 键盘监听库
- **requests** - HTTP请求库
- **threading** - 多线程处理

## 📋 开发计划

### v0.1.0 ✅ (当前版本)
- [x] 桌面浮动Emoji虚拟人
- [x] 智能对话系统（多API支持）
- [x] MemABC记忆系统基础架构
- [x] 聊天状态机和记忆管理
- [x] 配置管理系统
- [x] 完整的启动脚本系统

### 未来计划
- [ ] 语音识别和语音合成
- [ ] 更多表情动画效果
- [ ] 自定义主题和样式
- [ ] 插件系统支持
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
- **隐私保护**: 键盘监听仅检测情绪关键词，不会记录完整文本
- **数据存储**: 对话历史和记忆数据存储在本地，注意备份

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