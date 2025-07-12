# Emoji 虚拟人桌面助手

一个极简但可运行的桌面 Emoji 助手，具备桌面浮动 Emoji 虚拟人、基本气泡对话显示、点击互动触发对话输入、简单集成大模型生成回复、感知用户键盘输入（情绪关键词检测）等功能。

## 🚀 功能特点

- **悬浮 Emoji 虚拟人**: 可爱的 😺 表情悬浮在屏幕右下角
- **智能情绪感知**: 实时监听键盘输入，检测情绪关键词
- **智能对话**: 集成大模型API，提供智能回复
- **美观界面**: 现代化的UI设计，支持动画效果
- **可拖拽**: 支持鼠标拖拽移动位置
- **气泡对话**: 优雅的对话气泡显示

## 📦 安装依赖

```bash
pip install -r requirements.txt
```

## ⚙️ 配置

1. 复制环境变量模板：
```bash
cp env_example.txt .env
```

2. 编辑 `.env` 文件，配置API密钥：
```
OPENAI_API_KEY=your_openai_api_key_here
HUGGINGFACE_API_KEY=your_huggingface_api_key_here
```

3. 编辑 `config.py` 文件，根据需要调整配置

## 🎯 使用方法

### 启动程序
```bash
python run.py
```

### 基本操作
- **点击 Emoji**: 打开聊天对话框
- **拖拽 Emoji**: 移动位置
- **键盘输入**: 自动检测情绪关键词
- **Ctrl+C**: 优雅退出程序

### 情绪关键词示例
- 负面情绪: "烦"、"累"、"唉"、"难过"等
- 愤怒情绪: "操"、"妈的"、"气死"等
- 疲惫情绪: "累"、"疲惫"、"困"等
- 正面情绪: "开心"、"高兴"、"棒"等

## 🏗️ 项目结构

```
emoji_assistant/
├── main.py                 # 主程序入口
├── config.py              # 配置文件
├── run.py                 # 启动脚本
├── requirements.txt       # 依赖列表
├── README.md             # 项目文档
├── ui/                   # UI模块
│   ├── __init__.py
│   ├── floating_head.py  # 悬浮Emoji窗口
│   └── speech_bubble.py  # 对话气泡组件
├── interaction/          # 交互模块
│   ├── __init__.py
│   ├── emotion_detector.py    # 情绪检测器
│   ├── keyboard_listener.py   # 键盘监听器
│   └── chat_input.py          # 聊天输入对话框
├── core/                 # 核心模块
│   ├── __init__.py
│   └── llm_client.py     # 大模型客户端
└── assets/               # 资源文件
    └── emoji_icon.png    # Emoji图标（可选）
```

## 🔧 开发说明

### 模块说明

1. **FloatingEmojiWindow**: 悬浮Emoji窗口，支持拖拽和点击
2. **SpeechBubbleWidget**: 对话气泡组件，支持动画效果
3. **EmotionDetector**: 情绪检测器，基于关键词匹配
4. **KeyboardListener**: 键盘监听器，使用pynput库
5. **ChatInputDialog**: 聊天输入对话框，支持异步请求
6. **LLMClient**: 大模型客户端，支持多种API

### 扩展功能

- 支持自定义情绪关键词
- 支持自定义安慰消息
- 支持多种大模型API
- 支持主题定制
- 支持动画效果开关

## 🐛 故障排除

### 常见问题

1. **权限问题**: 键盘监听需要系统权限
   - macOS: 系统偏好设置 > 安全性与隐私 > 辅助功能
   - Windows: 以管理员身份运行
   - Linux: 确保有X11权限

2. **API连接失败**: 检查网络连接和API密钥配置

3. **界面显示异常**: 确保PyQt5正确安装

### 调试模式

设置 `config.py` 中的 `DEBUG_MODE = True` 启用调试模式。

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📞 联系方式

如有问题，请提交Issue或联系开发者。 