#!/usr/bin/env python3
"""
Emoji 虚拟人桌面助手 - 启动脚本
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import main

if __name__ == "__main__":
    main() 