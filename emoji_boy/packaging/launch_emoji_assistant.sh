#!/bin/bash

# Emoji Assistant 启动脚本
# 用于启动打包后的程序

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
APP_DIR="$PROJECT_DIR/dist/EmojiAssistant"

echo "🚀 启动 Emoji Assistant..."

# 检查打包后的程序是否存在
if [ ! -f "$APP_DIR/EmojiAssistant" ]; then
    echo "❌ 错误：找不到打包后的程序"
    echo "请先运行打包脚本: ./packaging/build.sh"
    exit 1
fi

# 启动程序
echo "✅ 找到程序，正在启动..."
"$APP_DIR/EmojiAssistant"

echo "👋 Emoji Assistant 已退出" 