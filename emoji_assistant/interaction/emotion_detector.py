"""
情绪感知模块
"""

import re
from collections import deque
from PyQt5.QtCore import QObject, pyqtSignal


class EmotionDetector(QObject):
    """情绪检测器"""
    
    # 信号定义
    emotion_detected = pyqtSignal(str, str)  # emotion_type, message
    
    def __init__(self, window_size=50, threshold=3):
        super().__init__()
        
        # 配置参数
        self.window_size = window_size
        self.threshold = threshold
        
        # 字符缓冲区（滑窗）
        self.char_buffer = deque(maxlen=window_size)
        
        # 情绪关键词库
        self.emotion_keywords = {
            'sad': [
                '烦', '累', '唉', '难过', '伤心', '痛苦', '绝望', '沮丧',
                '失望', '郁闷', '悲伤', '哭泣', '哭', '泪', '心碎', '孤独',
                '寂寞', '空虚', '无助', '无力', '疲惫', '困', '想死', '死',
                '活不下去', '没意思', '无聊', '没劲', '没希望', '没未来'
            ],
            'angry': [
                '操', '妈的', '混蛋', '该死', '气死', '愤怒', '生气', '恼火',
                '烦躁', '暴躁', '暴怒', '火大', '火冒三丈', '气炸', '气疯',
                '恨', '讨厌', '厌恶', '恶心', '烦死了', '受不了', '崩溃',
                '抓狂', '发疯', '神经病', '有病', '傻逼', '白痴', '垃圾'
            ],
            'tired': [
                '累', '疲惫', '困', '想睡', '没精神', '没力气', '虚脱',
                '精疲力尽', '筋疲力尽', '累死', '累趴', '累垮', '累倒',
                '没劲', '没力气', '没精神', '没状态', '没心情', '没动力',
                '想休息', '想躺', '想睡', '困死了', '累死了', '累趴了'
            ],
            'happy': [
                '开心', '高兴', '快乐', '兴奋', '激动', '爽', '棒', '好',
                '赞', '棒棒', '棒极了', '太棒了', '太好了', '好棒', '好赞',
                '开心死了', '高兴死了', '快乐死了', '爽死了', '棒死了',
                '哈哈', '呵呵', '嘻嘻', '嘿嘿', '😊', '😄', '😃', '😁'
            ],
            'surprised': [
                '哇', '天哪', '我的天', '真的吗', '不会吧', '怎么可能',
                '太意外', '太惊讶', '太震惊', '太不可思议', '太神奇',
                '太厉害了', '太强了', '太牛了', '太棒了', '太赞了',
                '😲', '😱', '😳', '😵', '😨', '😰', '😯', '😮'
            ]
        }
        
        # 安慰消息库
        self.comfort_messages = {
            'sad': [
                "别难过，一切都会好起来的 💕",
                "我在这里陪着你，你不是一个人 🤗",
                "生活总有起起落落，明天会更好的 🌅",
                "累了就休息一下，给自己一点时间 🛌",
                "你比想象中更坚强，加油！ 💪"
            ],
            'angry': [
                "深呼吸，冷静一下 😌",
                "生气对身体不好，先消消气吧 🌸",
                "我理解你的感受，但别让愤怒控制你 🧘‍♀️",
                "换个角度想想，也许事情没那么糟 🤔",
                "来，我们一起想想解决办法 💡"
            ],
            'tired': [
                "累了就休息一下吧，身体最重要 😴",
                "工作再忙也要注意身体哦 💪",
                "休息是为了走更远的路 🌟",
                "给自己一点时间，慢慢来 🕐",
                "你辛苦了，休息一下再继续吧 🛌"
            ],
            'happy': [
                "看到你开心我也很开心 😊",
                "继续保持这份好心情吧！ ✨",
                "你的快乐感染了我 🌈",
                "今天是个好日子呢 🎉",
                "开心就好，保持这份快乐 🎊"
            ],
            'surprised': [
                "哇，看来发生了有趣的事情呢 😲",
                "生活总是充满惊喜 ✨",
                "这确实很让人意外呢 🤔",
                "看来今天有好事发生 🎉",
                "惊喜总是让人心情愉悦 🌟"
            ]
        }
        
        # 情绪检测状态
        self.last_emotion_time = 0
        self.emotion_cooldown = 10  # 10秒冷却时间
        self.current_time = 0
    
    def add_character(self, char):
        """添加字符到缓冲区"""
        self.char_buffer.append(char)
        self.current_time += 1
        
        # 检查情绪
        self.check_emotion()
    
    def check_emotion(self):
        """检查情绪状态"""
        # 检查冷却时间
        if self.current_time - self.last_emotion_time < self.emotion_cooldown:
            return
        
        # 获取当前文本
        text = ''.join(self.char_buffer)
        
        # 检测各种情绪
        for emotion_type, keywords in self.emotion_keywords.items():
            count = 0
            for keyword in keywords:
                count += len(re.findall(re.escape(keyword), text))
            
            if count >= self.threshold:
                self.trigger_emotion(emotion_type)
                break
    
    def trigger_emotion(self, emotion_type):
        """触发情绪事件"""
        import random
        
        # 更新最后触发时间
        self.last_emotion_time = self.current_time
        
        # 随机选择安慰消息
        messages = self.comfort_messages.get(emotion_type, [])
        if messages:
            message = random.choice(messages)
        else:
            message = "我感受到了你的情绪变化 🤗"
        
        # 发射信号
        self.emotion_detected.emit(emotion_type, message)
        
        print(f"🎭 检测到情绪: {emotion_type} - {message}")
    
    def add_text(self, text):
        """添加文本（用于批量处理）"""
        for char in text:
            self.add_character(char)
    
    def clear_buffer(self):
        """清空缓冲区"""
        self.char_buffer.clear()
        self.current_time = 0
        self.last_emotion_time = 0
    
    def set_threshold(self, threshold):
        """设置检测阈值"""
        self.threshold = threshold
    
    def set_window_size(self, window_size):
        """设置窗口大小"""
        self.window_size = window_size
        # 重新创建缓冲区
        old_buffer = list(self.char_buffer)
        self.char_buffer = deque(old_buffer, maxlen=window_size)
    
    def add_custom_keywords(self, emotion_type, keywords):
        """添加自定义关键词"""
        if emotion_type not in self.emotion_keywords:
            self.emotion_keywords[emotion_type] = []
        
        self.emotion_keywords[emotion_type].extend(keywords)
    
    def add_custom_messages(self, emotion_type, messages):
        """添加自定义安慰消息"""
        if emotion_type not in self.comfort_messages:
            self.comfort_messages[emotion_type] = []
        
        self.comfort_messages[emotion_type].extend(messages) 