#!/bin/bash

# Emoji Assistant 打包脚本
# 使用配置文件进行打包

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "🚀 开始打包 Emoji Assistant..."

# 切换到项目目录
cd "$PROJECT_DIR"

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "❌ 错误：找不到虚拟环境"
    echo "请先运行: python3 -m venv venv"
    exit 1
fi

# 激活虚拟环境
source venv/bin/activate

# 检查依赖
echo "📦 检查打包依赖..."
python -c "import pyinstaller" 2>/dev/null || {
    echo "安装 PyInstaller..."
    pip install pyinstaller
}

python -c "import PIL" 2>/dev/null || {
    echo "安装 Pillow..."
    pip install pillow
}

# 清理旧文件
echo "🧹 清理旧文件..."
rm -rf build dist *.spec

# 使用配置文件打包
echo "🔨 开始打包..."
pyinstaller packaging/build_config.spec

echo "✅ 打包完成！"
echo ""
echo "📁 生成的文件："
echo "  - dist/EmojiAssistant/ (可执行程序)"
echo "  - dist/EmojiAssistant.app/ (macOS 应用)"
echo ""
echo "🚀 启动方式："
echo "  - ./packaging/launch_emoji_assistant.sh"
echo "  - ./dist/EmojiAssistant/EmojiAssistant"
echo "  - 双击 dist/EmojiAssistant.app" 