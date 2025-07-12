"""
对话记录管理模块
负责存储和管理用户与AI的对话记录
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Optional


class ChatMemory:
    """对话记录管理类"""
    
    def __init__(self, memory_dir: str = "MemABC/memA"):
        """
        初始化对话记录管理器
        
        Args:
            memory_dir: 对话记录存储目录
        """
        self.memory_dir = memory_dir
        self.current_session_id = None
        self.current_file_path = None
        
        # 确保目录存在
        os.makedirs(memory_dir, exist_ok=True)
    
    def _get_date_filename(self, date_obj: datetime) -> str:
        """
        根据日期生成文件名
        
        Args:
            date_obj: 日期对象
            
        Returns:
            文件名，格式如: 20250712.txt
        """
        return date_obj.strftime("%Y%m%d") + ".txt"
    
    def _get_timestamp(self) -> str:
        """
        获取当前时间戳
        
        Returns:
            时间戳字符串，格式如: [2025/07/12 14:27:49]
        """
        return datetime.now().strftime("[%Y/%m/%d %H:%M:%S]")
    
    def _get_file_path(self, date_obj: datetime) -> str:
        """
        获取指定日期的文件路径
        
        Args:
            date_obj: 日期对象
            
        Returns:
            完整的文件路径
        """
        filename = self._get_date_filename(date_obj)
        return os.path.join(self.memory_dir, filename)
    
    def start_new_session(self) -> str:
        """
        开始新的对话会话
        
        Returns:
            会话ID
        """
        self.current_session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.current_file_path = self._get_file_path(datetime.now())
        
        # 立即写入新会话的时间戳
        self._write_session_start(self.current_file_path)
        
        return self.current_session_id
    
    def end_current_session(self):
        """结束当前对话会话"""
        if self.current_session_id:
            self._write_session_end()
            self.current_session_id = None
            self.current_file_path = None
    
    def _write_session_start(self, file_path: str):
        """写入会话开始标记"""
        timestamp = self._get_timestamp()
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(f"{timestamp}\n")

    def _write_session_end(self):
        """写入会话结束标记（已废弃，不再写入）"""
        pass
    
    def record_message(self, sender: str, message: str, force_new_session: bool = False):
        current_time = datetime.now()
        current_file_path = self._get_file_path(current_time)

        # 检查是否需要开始新会话
        if force_new_session or not self.current_session_id:
            self.start_new_session()

        # 如果文件路径发生变化（跨天），需要在新文件中继续记录
        if self.current_file_path != current_file_path:
            self.current_file_path = current_file_path
            self._write_session_start(current_file_path)

        # 写入消息
        with open(current_file_path, 'a', encoding='utf-8') as f:
            f.write(f"{sender}> {message}\n")
    
    def record_user_message(self, message: str):
        """记录用户消息"""
        self.record_message("M", message)
    
    def record_ai_message(self, message: str):
        """记录AI消息"""
        self.record_message("ai", message)
    
    def get_recent_conversations(self, days: int = 7) -> List[Dict]:
        """
        获取最近几天的对话记录
        
        Args:
            days: 获取最近几天的记录
            
        Returns:
            对话记录列表
        """
        conversations = []
        current_time = datetime.now()
        
        for i in range(days):
            target_date = current_time.replace(day=current_time.day - i)
            file_path = self._get_file_path(target_date)
            
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if content.strip():
                            conversations.append({
                                'date': target_date.strftime('%Y-%m-%d'),
                                'file_path': file_path,
                                'content': content
                            })
                except Exception as e:
                    print(f"读取对话记录文件失败 {file_path}: {e}")
        
        return conversations
    
    def search_conversations(self, keyword: str, days: int = 30) -> List[Dict]:
        """
        搜索对话记录
        
        Args:
            keyword: 搜索关键词
            days: 搜索最近几天的记录
            
        Returns:
            包含关键词的对话记录列表
        """
        results = []
        conversations = self.get_recent_conversations(days)
        
        for conv in conversations:
            if keyword.lower() in conv['content'].lower():
                results.append(conv)
        
        return results
    
    def get_today_conversations(self) -> str:
        """
        获取今天的对话记录
        
        Returns:
            今天的对话记录内容
        """
        today_file = self._get_file_path(datetime.now())
        if os.path.exists(today_file):
            try:
                with open(today_file, 'r', encoding='utf-8') as f:
                    return f.read()
            except Exception as e:
                print(f"读取今天对话记录失败: {e}")
                return ""
        return ""
    
    def clear_old_conversations(self, days_to_keep: int = 90):
        """
        清理旧的对话记录
        
        Args:
            days_to_keep: 保留最近几天的记录
        """
        current_time = datetime.now()
        
        for filename in os.listdir(self.memory_dir):
            if filename.endswith('.txt'):
                try:
                    file_date = datetime.strptime(filename[:-4], '%Y%m%d')
                    days_old = (current_time - file_date).days
                    
                    if days_old > days_to_keep:
                        file_path = os.path.join(self.memory_dir, filename)
                        os.remove(file_path)
                        print(f"已删除旧对话记录: {filename}")
                except ValueError:
                    # 文件名格式不正确，跳过
                    continue


# 全局对话记录管理器实例
chat_memory = ChatMemory() 