# Emoji AI Assistant v0.2.3

一个具有情感记忆和人格演化的AI助手系统。

**最新更新**: MemABC初始化系统 - 确保纯净人格，简化维护流程

## 快速开始

### 安装依赖
```bash
pip install -r emoji_boy/requirements.txt
```

### 启动AI助手
```bash
cd emoji_boy
python main.py
```

## MemABC记忆管理

### 自动化管理（推荐）
- **Git自动清理**: 每次`git commit`时自动清理MemABC人格和记忆
- **无需手动操作**: 开发过程中正常使用，提交时自动处理

### 手动管理
```bash
# 清理MemABC（上传前准备）
./clean.sh

# 查看备份列表
./clean.sh --list

# 删除所有备份（谨慎使用）
./clean.sh --purge
```

### 备份策略
- 自动保留最近5个备份
- 超过5个时自动删除最旧的
- 备份包含完整的memA、memB、memC和systemprompt.txt

## 项目结构

```
emoji-ai-assistant/
├── emoji_boy/                 # 主程序目录
│   ├── MemABC/               # 记忆管理系统
│   ├── core/                 # 核心功能模块
│   ├── brain_agent/          # 智能代理模块
│   └── main.py               # 主程序入口
├── clean.sh                  # MemABC清理工具
└── README.md                 # 项目说明
```

## 开发说明

- 开发时正常使用，无需担心MemABC状态
- Git hook会自动处理人格和记忆的清理
- 如需手动清理，使用`./clean.sh`即可
- 备份数据存储在`emoji_boy/MemABC/backup_*`目录

## 许可证

MIT License 
