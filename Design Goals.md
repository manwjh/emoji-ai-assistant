项目研发需求文档

#（第一阶段）

🏷 项目名称

Emoji 虚拟人桌面助手（Minimal Floating Emoji Assistant）

🎯 产品目标（阶段一）

打造一个极简但可运行的桌面 Emoji 助手，具备：
	•	桌面浮动 Emoji 虚拟人
	•	基本气泡对话显示
	•	点击互动触发对话输入
	•	简单集成大模型生成回复
	•	感知用户键盘输入（情绪关键词检测）

模块划分与功能定义

1. FloatingEmojiWindow 虚拟人界面
	•	悬浮在屏幕右下角（支持拖动）
	•	Emoji 图案（默认：😺）
	•	无边框、透明背景、总在最前
	•	点击 Emoji 弹出输入对话框

2. SpeechBubbleWidget 对话气泡
	•	相对虚拟人位置浮动显示
	•	支持淡入淡出动画
	•	可以程序调用显示文本内容
	•	显示 LLM 返回的回答或预设语句

3. EmotionDetector 情绪感知模块
	•	基于用户输入字符流构建上下文（滑窗）
	•	预置情绪关键词库（如：烦、累、操、唉等）
	•	检测阈值后发送“情绪触发事件”到主 UI
	•	后续可扩展为接入情感分析模型

4. KeyboardListener 键盘监听模块
	•	使用 pynput.keyboard.Listener 实现
	•	在后台线程中运行，不阻塞主 UI
	•	每次键入字符送入 EmotionDetector

5. ChatInputDialog 用户交互窗口
	•	点击 Emoji 时弹出
	•	简单输入框 + 发送按钮
	•	提交后调用 LLMClient 请求回复

6. LLMClient 大模型接口模块
	•	使用 OpenAI 或 HuggingFace 的 API（可配置）
	•	输入用户消息，输出 assistant 回复
	•	支持异步调用或后台线程方式避免阻塞 UI


🔄 交互流程（主线）
	1.	启动程序，显示悬浮 Emoji。
	2.	后台监听用户键盘，检测输入字符。
	3.	若识别到情绪异常，弹出气泡安慰句子。
	4.	用户点击 Emoji，弹出对话输入窗口。
	5.	用户发送问题，请求大模型回复。
	6.	回复以气泡方式显示在虚拟人旁边。

📁 目录结构
emoji_assistant/
├── main.py
├── ui/
│   ├── floating_head.py
│   └── speech_bubble.py
├── interaction/
│   ├── emotion_detector.py
│   ├── keyboard_listener.py
│   └── chat_input.py
├── core/
│   └── llm_client.py
├── config.py
├── requirements.txt
└── assets/
    └── emoji_icon.png (可选，后续扩展图标)

✅ 界面设计目标
	1.	美观但不打扰视线
	2.	浮动感明显，不嵌入具体窗口
	3.	信息层级清晰，对话内容可读
	4.	易于关闭/拖动/互动

⸻

🎨 设计风格建议（Glassmorphism）
	•	背景：半透明 + 毛玻璃模糊效果（blur）
	•	边框：淡淡的白色描边或发光边
	•	圆角：中度圆角（如 12~20px）
	•	阴影：柔和投影增强悬浮感（如 box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1)）

使用这套框架，以支持更炫酷的前端：Electron + Python

#（第二阶段）
代确定