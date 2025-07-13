#!/usr/bin/env python3
"""
测试自动编码调度器
"""

import sys
import time
from PyQt5.QtWidgets import QApplication
from core.auto_encoder import AutoEncoderScheduler


def test_auto_encoder():
    """测试自动编码调度器"""
    app = QApplication(sys.argv)
    
    print("🧪 开始测试自动编码调度器...")
    
    # 创建调度器
    scheduler = AutoEncoderScheduler()
    
    # 启动调度器
    scheduler.start()
    
    print("⏳ 等待10秒观察调度器运行...")
    time.sleep(10)
    
    # 停止调度器
    scheduler.stop()
    
    print("✅ 测试完成")
    
    return 0


if __name__ == "__main__":
    sys.exit(test_auto_encoder()) 