# Emoji AI Assistant v0.2.0

**Screw MCP, let's build a Brain Agent!** 🚀

This is a major upgrade with Brain Agent system, see [CHANGELOG.md](CHANGELOG.md) for details.

A minimalist yet feature-complete desktop Emoji virtual assistant with floating desktop interface, intelligent conversation, brain-like memory system, and brain-like intent recognition system.

## 🎯 Features

- 🎭 **Floating Desktop Emoji** - Cute 😺 emoji that can be dragged and stays on top
- 💬 **Intelligent Conversation System** - Integrated OpenAI/HuggingFace API with context memory
- 🧠 **MemABC Memory System** - Experimental brain-like memory architecture with encoding and retrieval
- 🧠 **Brain Agent System** - Experimental brain-like intent architecture with intent recognition + capability execution + dynamic code generation
- 🎨 **Modern UI** - Elegant PyQt5-based interface with animation effects
- 🔧 **Configuration Management** - Flexible configuration system supporting multiple APIs
- 🚀 **One-Click Launch** - Complete startup scripts with automatic environment setup

## 🚀 Quick Start

### 1. Clone the Project
```bash
git clone <repository-url>
cd emoji-ai-assistant
```

### 2. Install Dependencies
```bash
cd emoji_boy
pip install -r requirements.txt
```

### 3. Configure API Keys (Optional)
```bash
cp env_example.txt .env
```

Edit the `.env` file:
```
OPENAI_API_KEY=your_openai_api_key_here
HUGGINGFACE_API_KEY=your_huggingface_api_key_here
```

**Note**: If no API keys are configured, the program will use built-in Mock mode.

### 4. Launch the Application

**Method 1: Using Startup Script (Recommended)**
```bash
./start.sh
```

**Method 2: Direct Run**
```bash
python run.py
```

## 📖 Usage Guide

### Basic Operations
- **Click Emoji** - Open chat dialog to start conversation
- **Drag Emoji** - Move assistant to any position on screen
- **Ctrl+C** - Graceful exit

### Conversation Features
- Supports multi-turn conversations with context memory
- Integrates multiple AI models (OpenAI GPT, HuggingFace, Mock mode)
- Intelligent responses with emoji expressions
- Automatic conversation history saving and management
- **Brain-like Intent Recognition**: Automatically recognizes user intent and executes corresponding functions
- **Dynamic Code Generation**: Automatically generates and safely executes Python code based on intent
- **Automatic Function Execution**: Time queries, system information, mathematical calculations, search, etc.



### MemABC Memory System
- **MemA**: Raw memory storage (daily files)
- **MemB**: Processed and categorized memory
- **MemC**: Long-term memory storage and AI subconscious
- Supports A2B and A2C encoding conversion
- Automatic backup and memory management

### 🧠 Brain Agent System
- **Intent Recognition**: Supports 7 intent types (search, chat, config, help, meditation, system, unknown)
- **Skill Network**: 6 core plugins (system, chat, search, config, help, meditation)
- **Dynamic Execution**: Automatically generates and safely executes Python code based on intent
- **Perception-Cognition-Execution Loop**: Mimics human brain's information processing flow
- **Memory Mechanism**: Simulates human brain's memory and recall processes
- **Behavioral Pattern Learning**: Optimizes response strategies based on interaction history

## 🏗️ Project Structure

```
emoji-ai-assistant/
├── emoji_boy/                    # Main program directory
│   ├── ui/                       # User interface module
│   ├── interaction/              # Interaction module
│   ├── core/                     # Core module
│   ├── brain_agent/              # 🧠 Brain Agent System
│   │   ├── intent_engine.py      # Intent recognition engine
│   │   ├── plugin_registry.py    # Skill network registry
│   │   ├── plugins/              # Skill plugins directory
│   │   │   ├── system_plugin.py  # System operation plugin
│   │   │   ├── chat_plugin.py    # Chat communication plugin
│   │   │   ├── search_plugin.py  # Search functionality plugin
│   │   │   ├── config_plugin.py  # Configuration management plugin
│   │   │   ├── help_plugin.py    # Help guidance plugin
│   │   │   └── meditation_plugin.py # Meditation guidance plugin
│   │   ├── test.py               # Test framework
│   │   ├── test.sh               # Automated test script
│   │   └── test_vectors.txt      # Test vector dataset
│   ├── MemABC/                   # Memory system
│   └── ...                       # Other config and script files
├── scripts/                      # Utility scripts
├── MemABC/                       # Root directory memory system
└── ...                           # Documentation and config files
```

## 🛠️ Technology Stack

- **Python 3.7+** - Primary programming language
- **PyQt5** - Modern GUI framework
- **OpenAI API** - GPT model support
- **HuggingFace API** - Open-source model support

- **requests** - HTTP request library
- **threading** - Multi-threading support

## 📋 Development Roadmap

### v0.2.0 ✅ (Current Version) - Brain Agent System
- [x] 🧠 Brain-like intent recognition engine
- [x] 🧠 Skill network system (6 core plugins)
- [x] 🧠 Dynamic code generation and safe execution
- [x] 🧠 Intent recognition and execution integration
- [x] 🧠 Module independence support
- [x] 🧠 Complete test framework
- [x] 🧠 Automated test scripts
- [x] 🧠 Compatibility import system
- [x] 🧠 Unified API key management
- [x] 🧠 Secure sandbox execution environment

### v0.1.1 ✅ (Previous Version) - Security Enhanced
- [x] Floating desktop emoji virtual assistant
- [x] Intelligent conversation system (multi-API support)
- [x] MemABC memory system foundation
- [x] Chat state machine and memory management
- [x] Configuration management system
- [x] Complete startup script system
- [x] 🔐 Security Enhancement: API key leak prevention
- [x] 🔐 Security Enhancement: Pre-commit hook checks
- [x] 🔐 Security Enhancement: Security scanning tools
- [x] 🔐 Security Enhancement: Comprehensive security documentation

### v0.1.0 ✅ (Previous Version)
- [x] Floating desktop emoji virtual assistant
- [x] Intelligent conversation system (multi-API support)
- [x] MemABC memory system foundation
- [x] Chat state machine and memory management
- [x] Configuration management system
- [x] Complete startup script system

### Future Plans
- [ ] 🧠 More intent types and skill plugins
- [ ] 🧠 Intent recognition accuracy optimization
- [ ] 🧠 Code generation capability enhancement
- [ ] 🧠 Multi-modal intent recognition (image, speech)
- [ ] 🧠 Distributed skill network
- [ ] 🧠 Brain-like learning mechanism optimization
- [ ] Speech recognition and synthesis
- [ ] More emoji animation effects
- [ ] Custom themes and styling
- [ ] Multi-language support
- [ ] MemABC memory system optimization
- [ ] Mobile platform support

## ⚠️ Important Notes

### System Requirements
- **Operating System**: macOS 10.14+, Windows 10+, Ubuntu 18.04+
- **Python**: 3.7 or higher
- **Memory**: At least 512MB available RAM
- **Storage**: At least 100MB available space



### Security Reminders
- **API Costs**: Using OpenAI API incurs costs, please monitor usage

- **Data Storage**: Conversation history and memory data stored locally, remember to backup

## 🐛 Troubleshooting

### Common Issues

1. **Permission Problems**
   ```bash
   # macOS
   sudo chmod +x start.sh
   
   # Linux
   chmod +x start.sh
   ```

2. **Dependency Installation Failures**
   ```bash
   # Upgrade pip
   python -m pip install --upgrade pip
   
   # Reinstall dependencies
   pip install -r requirements.txt --force-reinstall
   ```

3. **PyQt5 Installation Issues**
   ```bash
   # macOS
   brew install pyqt5
   
   # Ubuntu
   sudo apt-get install python3-pyqt5
   ```

4. **API Connection Failures**
   - Check network connection
   - Verify API keys are correct
   - Confirm API quota is sufficient

### Debug Mode

Set environment variables to enable debugging:
```bash
export DEBUG_MODE=true
export LOG_LEVEL=DEBUG
```

### Log Files

Program logs are saved in:
- Console output
- System logs (macOS/Linux)

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details

## 📝 Changelog

For detailed feature updates and bug fixes, please see [CHANGELOG.md](CHANGELOG.md)

## 🤝 Contributing

We welcome Issue submissions and Pull Requests to improve this project!

### Contribution Guidelines
1. Fork the project
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 Contact

- **Project Homepage**: [GitHub Repository]
- **Issue Reports**: [Issues]
- **Feature Suggestions**: [Discussions]

## 🙏 Acknowledgments

Thanks to all developers and users who have contributed to this project!

## 🔗 Related Links

- [Design Goals](Design Goals.md) - Project design philosophy and goals
- [MemABC System](emoji_boy/MemABC/README.md) - Memory system documentation
- [Chinese README](README.md) - Chinese version of this documentation 