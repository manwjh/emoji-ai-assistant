#!/bin/bash

# Emoji 虚拟人桌面助手启动脚本

set -e

PROJECT_DIR=$(cd "$(dirname "$0")" && pwd)
VENV_DIR="$PROJECT_DIR/venv"
REQUIREMENTS_FILE="$PROJECT_DIR/requirements.txt"

# 1. 检查虚拟环境
if [ ! -d "$VENV_DIR" ]; then
    echo "📦 虚拟环境不存在，正在自动创建..."
    python3 -m venv "$VENV_DIR"
    echo "✅ 虚拟环境创建完成"
fi

# 2. 激活虚拟环境
source "$VENV_DIR/bin/activate"
if [[ "$VIRTUAL_ENV" != "$VENV_DIR"* ]]; then
    echo "❌ 虚拟环境激活失败，当前 VIRTUAL_ENV: $VIRTUAL_ENV"
    exit 1
fi

PYTHON_PATH=$(which python)
PIP_PATH=$(which pip)
echo "🐍 Python路径: $PYTHON_PATH"
echo "📦 Pip路径: $PIP_PATH"
echo "✅ 虚拟环境已激活: $VIRTUAL_ENV"

# 3. 检查依赖是否已全部安装
NEED_INSTALL=0
python -c "import PyQt5" 2>/dev/null || NEED_INSTALL=1
python -c "import pynput" 2>/dev/null || NEED_INSTALL=1
python -c "import requests" 2>/dev/null || NEED_INSTALL=1
python -c "import typing_extensions" 2>/dev/null || NEED_INSTALL=1

if [ $NEED_INSTALL -eq 1 ]; then
    echo "🔍 检测到依赖未安装，正在安装 requirements.txt ..."
    if python -m pip install -r "$REQUIREMENTS_FILE"; then
        echo "✅ 依赖安装完成"
    else
        echo "❌ 依赖安装失败，请手动运行: source venv/bin/activate && python -m pip install -r requirements.txt"
        exit 1
    fi
else
    echo "✅ 所有依赖已安装"
fi

# 4. 启动主程序
trap 'echo -e "\n🛑 收到中断信号，正在退出..."; exit 1' INT TERM

echo "🎯 启动主程序..."
echo "=================================="
if python run.py; then
    echo "=================================="
    echo "✅ 程序正常退出"
else
    echo "=================================="
    echo "❌ 程序异常退出，退出码: $?"
    echo "💡 如果遇到问题，请检查："
    echo "   1. 网络连接是否正常"
    echo "   2. API密钥是否正确配置"
    echo "   3. 系统权限是否已授权"
    echo "   4. 查看上方错误信息"
    exit 1
fi 