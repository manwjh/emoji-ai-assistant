"""
配置文件
"""

import os
from typing import Optional

# API配置
OPENAI_API_KEY: Optional[str] = None
HUGGINGFACE_API_KEY: Optional[str] = None

# 默认API类型
DEFAULT_API_TYPE = "mock"  # "openai", "huggingface", "mock"

# 模型配置
DEFAULT_MODEL = {
    "openai": "gpt-3.5-turbo",
    "huggingface": "gpt2",
    "mock": "mock-model"
}

# UI配置
WINDOW_SIZE = (80, 80)  # Emoji窗口大小
BUBBLE_DURATION = 5000  # 气泡显示时长（毫秒）
WINDOW_POSITION = "bottom_right"  # 窗口位置

# 情绪检测配置
EMOTION_WINDOW_SIZE = 50  # 情绪检测窗口大小
EMOTION_THRESHOLD = 3  # 情绪检测阈值
EMOTION_COOLDOWN = 10  # 情绪检测冷却时间（秒）

# 键盘监听配置
KEYBOARD_ENABLED = True
IGNORE_SPECIAL_KEYS = True
IGNORE_MODIFIER_KEYS = True

# 日志配置
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
LOG_FILE = "emoji_assistant.log"

# 主题配置
THEME = {
    "primary_color": "#4CAF50",
    "secondary_color": "#45a049",
    "background_color": "#f9f9f9",
    "text_color": "#333333",
    "border_color": "#e0e0e0"
}

# 动画配置
ANIMATION_ENABLED = True
ANIMATION_DURATION = 200  # 毫秒

# 开发配置
DEBUG_MODE = False
SHOW_CONSOLE = True

def load_env_vars():
    """从环境变量加载配置"""
    global OPENAI_API_KEY, HUGGINGFACE_API_KEY
    
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

def get_api_key(api_type: str) -> Optional[str]:
    """获取指定API类型的密钥"""
    if api_type == "openai":
        return OPENAI_API_KEY
    elif api_type == "huggingface":
        return HUGGINGFACE_API_KEY
    return None

def is_api_configured(api_type: str) -> bool:
    """检查指定API是否已配置"""
    return bool(get_api_key(api_type))

# 加载环境变量
load_env_vars() 