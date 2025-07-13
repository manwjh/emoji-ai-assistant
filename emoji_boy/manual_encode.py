#!/usr/bin/env python3
"""
手动触发编码脚本
用于调试和测试 encoding_a2b 和 encoding_a2c
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from core.auto_encoder import AutoEncoderScheduler


def manual_encode():
    """手动触发编码"""
    print("🔄 手动触发编码...")
    
    # 创建调度器
    scheduler = AutoEncoderScheduler()
    
    # 直接运行编码脚本
    scheduler._run_encoding_scripts()
    
    # 等待所有线程完成
    for script, thread in scheduler.encoding_threads.items():
        if thread.running:
            print(f"⏳ 等待 {script} 完成...")
            thread.wait(30000)  # 等待30秒
    
    print("✅ 手动编码完成")
    
    return 0


if __name__ == "__main__":
    sys.exit(manual_encode()) 