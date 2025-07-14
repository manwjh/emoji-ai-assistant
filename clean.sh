#!/bin/bash

# MemABC清理脚本 - 一键清理和备份管理
# 用法: ./clean.sh [选项]
# 选项: --list (查看备份) --purge (删除所有备份)

echo "🧹 MemABC清理工具"
echo "=================="

case "${1:-}" in
    --list)
        echo "📋 当前备份列表:"
        cd emoji_boy/MemABC
        if ls backup_* 1> /dev/null 2>&1; then
            for backup in $(ls -dt backup_*); do
                if [ -d "$backup" ]; then
                    size=$(du -sh "$backup" | cut -f1)
                    date=$(stat -f "%Sm" -t "%Y-%m-%d %H:%M" "$backup")
                    echo "   📦 $backup ($date, $size)"
                fi
            done
        else
            echo "   没有备份"
        fi
        cd ../..
        ;;
    --purge)
        echo "⚠️  删除所有备份..."
        read -p "确认删除所有备份？(输入yes): " confirm
        if [ "$confirm" = "yes" ]; then
            rm -rf emoji_boy/MemABC/backup_*
            echo "✅ 所有备份已删除"
        else
            echo "❌ 操作取消"
        fi
        ;;
    *)
        echo "📋 正在清理MemABC..."
        cd emoji_boy/MemABC && ./init_MemABC.sh --safe && cd ../..
        echo "✅ 清理完成！"
        echo ""
        echo "💡 其他选项:"
        echo "   ./clean.sh --list    # 查看备份"
        echo "   ./clean.sh --purge   # 删除所有备份"
        ;;
esac 