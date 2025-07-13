#!/bin/bash

# memC_to_system_prompt.sh - 从memC生成系统提示词
# 使用与b2c相同的API配置和模型

echo "🚀 启动 memC_to_system_prompt - 从memC生成系统提示词"
echo "=================================================="

# 切换到父目录并激活虚拟环境（与b2c.sh相同）
cd "$(dirname "$0")"/..
echo "📁 切换到项目根目录: $(pwd)"
echo "🔧 激活虚拟环境..."
source venv/bin/activate

# 检查是否为初始化模式
if [ "$1" = "--init" ]; then
    echo "🔧 初始化模式：生成默认系统提示词"
    echo "📄 输出文件: MemABC/systemprompt.txt"
    echo ""
    
    PYTHONPATH=. python3 MemABC/memC_to_system_prompt.py --init
else
    # 检查memC文件是否存在
    if [ ! -f "MemABC/memC/memC.txt" ]; then
        echo "❌ memC文件不存在: MemABC/memC/memC.txt"
        echo "请先运行 a2c.sh 或 b2c.sh 生成memC内容"
        exit 1
    fi

    # 执行mem2prompt（与b2c.sh相同的执行方式）
    echo "📄 memC文件: MemABC/memC/memC.txt"
    echo "📄 输出文件: MemABC/systemprompt.txt"
    echo ""

    PYTHONPATH=. python3 MemABC/memC_to_system_prompt.py
fi

# 检查执行结果
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ memC_to_system_prompt 执行完成！"
    echo "📄 系统提示词已保存到: MemABC/systemprompt.txt"
    
    # 显示文件大小
    if [ -f "MemABC/systemprompt.txt" ]; then
        file_size=$(wc -c < "MemABC/systemprompt.txt")
        echo "📊 文件大小: ${file_size} 字节"
    fi
else
    echo ""
    echo "❌ memC_to_system_prompt 执行失败！"
    exit 1
fi 