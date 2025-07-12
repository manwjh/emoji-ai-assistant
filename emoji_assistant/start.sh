#!/bin/bash

# Emoji 虚拟人桌面助手启动脚本

set -e  # 遇到错误立即退出

echo "🚀 启动 Emoji 虚拟人桌面助手..."

# 检查虚拟环境是否存在
if [ ! -d "venv" ]; then
    echo "❌ 虚拟环境不存在，请先创建虚拟环境"
    echo "运行: python3 -m venv venv"
    exit 1
fi

# 激活虚拟环境
echo "📦 激活虚拟环境..."
source venv/bin/activate

# 检查Python版本
python_version=$(python --version 2>&1)
echo "🐍 Python版本: $python_version"

# 检查依赖是否安装
echo "🔍 检查依赖..."
if ! python -c "import PyQt5" 2>/dev/null; then
    echo "❌ PyQt5 未安装，正在安装依赖..."
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
    echo "✅ 依赖安装完成"
else
    echo "✅ 依赖检查通过"
fi

# 检查系统权限
echo "🔐 检查系统权限..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "⚠️  在 macOS 上，键盘监听需要辅助功能权限"
    echo "📋 请按以下步骤授权："
    echo "   1. 打开 系统偏好设置 > 安全性与隐私 > 辅助功能"
    echo "   2. 点击左下角的锁图标解锁"
    echo "   3. 找到 'Python' 或 'Terminal' 并勾选"
    echo "   4. 重启程序"
    echo ""
    echo "💡 如果不想授权键盘监听，程序仍可正常运行，但无法检测情绪关键词"
fi

# 检查配置文件
echo "📝 检查配置文件..."
if [ -f "~/.emoji_assistant/api_config.json" ]; then
    echo "✅ 发现已保存的API配置"
else
    echo "📋 未发现API配置，程序将使用默认配置或引导配置"
fi

# 运行程序
echo "🎯 启动主程序..."
echo "=================================="

# 使用trap捕获信号
trap 'echo -e "\n🛑 收到中断信号，正在退出..."; exit 1' INT TERM

# 运行程序并捕获错误
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