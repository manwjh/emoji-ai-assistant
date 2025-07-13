#!/usr/bin/env python3
"""
自动编码调度器
- 每天凌晨3点自动启动 encoding_a2b 和 encoding_a2c
- 程序关闭时静默执行（如果当天未执行过）
"""

import os
import sys
import time
import datetime
import subprocess
import threading
import json
from pathlib import Path
from PyQt5.QtCore import QTimer, QThread, pyqtSignal


class AutoEncoder(QThread):
    """自动编码线程"""
    
    # 信号定义
    encoding_started = pyqtSignal(str)  # 编码开始信号
    encoding_completed = pyqtSignal(str, bool)  # 编码完成信号 (脚本名, 是否成功)
    encoding_failed = pyqtSignal(str, str)  # 编码失败信号 (脚本名, 错误信息)
    
    def __init__(self, script_name):
        super().__init__()
        self.script_name = script_name
        self.running = False
        
    def run(self):
        """执行编码脚本"""
        self.running = True
        self.encoding_started.emit(self.script_name)
        
        try:
            # 获取脚本路径
            script_path = Path(__file__).parent.parent / "MemABC" / f"{self.script_name}.py"
            
            if not script_path.exists():
                raise FileNotFoundError(f"脚本文件不存在: {script_path}")
            
            # 执行脚本
            result = subprocess.run(
                [sys.executable, str(script_path)],
                capture_output=True,
                text=True,
                cwd=str(script_path.parent),
                timeout=300  # 5分钟超时
            )
            
            if result.returncode == 0:
                self.encoding_completed.emit(self.script_name, True)
            else:
                error_msg = result.stderr.strip() or result.stdout.strip()
                self.encoding_failed.emit(self.script_name, error_msg)
                
        except subprocess.TimeoutExpired:
            self.encoding_failed.emit(self.script_name, "执行超时（5分钟）")
        except Exception as e:
            self.encoding_failed.emit(self.script_name, str(e))
        finally:
            self.running = False
    
    def stop(self):
        """停止编码"""
        self.running = False


class AutoEncoderScheduler:
    """自动编码调度器"""
    
    def __init__(self):
        self.encoding_threads = {}  # 存储编码线程
        self.daily_timer = None  # 每日定时器
        self.last_run_date = None  # 上次运行日期
        self.state_file = Path(__file__).parent.parent / "MemABC" / ".auto_encoder_state.json"
        self._load_state()
        
    def _load_state(self):
        """加载状态文件"""
        try:
            if self.state_file.exists():
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    state = json.load(f)
                    self.last_run_date = state.get('last_run_date')
        except Exception as e:
            print(f"⚠️ 加载自动编码状态失败: {e}")
            self.last_run_date = None
    
    def _save_state(self):
        """保存状态文件"""
        try:
            state = {
                'last_run_date': datetime.date.today().isoformat(),
                'last_update': datetime.datetime.now().isoformat()
            }
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(state, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️ 保存自动编码状态失败: {e}")
    
    def _should_run_today(self):
        """检查今天是否应该运行"""
        today = datetime.date.today()
        return self.last_run_date != today.isoformat()
    
    def _setup_daily_timer(self):
        """设置每日定时器（凌晨3点）"""
        try:
            now = datetime.datetime.now()
            target_time = now.replace(hour=3, minute=0, second=0, microsecond=0)
            
            # 如果今天3点已过，设置为明天3点
            if now >= target_time:
                target_time += datetime.timedelta(days=1)
            
            # 计算到目标时间的秒数
            seconds_until_target = (target_time - now).total_seconds()
            
            # 设置定时器
            self.daily_timer = QTimer()
            self.daily_timer.timeout.connect(self._run_daily_encoding)
            self.daily_timer.start(int(seconds_until_target * 1000))  # 转换为毫秒
            
            print(f"⏰ 自动编码定时器已设置，下次执行时间: {target_time.strftime('%Y-%m-%d %H:%M:%S')}")
            
        except Exception as e:
            print(f"⚠️ 设置每日定时器失败: {e}")
    
    def _run_daily_encoding(self):
        """执行每日编码"""
        if not self._should_run_today():
            return
        
        print("🔄 开始每日自动编码...")
        self._run_encoding_scripts()
        
        # 重新设置明天的定时器
        self._setup_daily_timer()
    
    def _run_encoding_scripts(self):
        """运行编码脚本"""
        scripts = ['encoding_a2b', 'encoding_a2c']
        
        for script in scripts:
            if script in self.encoding_threads and self.encoding_threads[script].running:
                print(f"⚠️ {script} 正在运行中，跳过")
                continue
            
            # 创建并启动编码线程
            thread = AutoEncoder(script)
            thread.encoding_started.connect(self._on_encoding_started)
            thread.encoding_completed.connect(self._on_encoding_completed)
            thread.encoding_failed.connect(self._on_encoding_failed)
            
            self.encoding_threads[script] = thread
            thread.start()
    
    def _on_encoding_started(self, script_name):
        """编码开始回调"""
        print(f"🔄 开始执行 {script_name}...")
    
    def _on_encoding_completed(self, script_name, success):
        """编码完成回调"""
        if success:
            print(f"✅ {script_name} 执行成功")
        else:
            print(f"❌ {script_name} 执行失败")
        
        # 更新状态
        self._save_state()
    
    def _on_encoding_failed(self, script_name, error_msg):
        """编码失败回调"""
        print(f"❌ {script_name} 执行失败: {error_msg}")
        
        # 更新状态
        self._save_state()
    
    def start(self):
        """启动调度器"""
        print("🚀 启动自动编码调度器...")
        
        # 设置每日定时器
        self._setup_daily_timer()
        
        # 如果今天还没运行过，立即运行一次
        if self._should_run_today():
            print("🔄 今天还未执行编码，立即执行...")
            self._run_encoding_scripts()
    
    def stop(self):
        """停止调度器"""
        print("🛑 停止自动编码调度器...")
        
        # 停止定时器
        if self.daily_timer:
            self.daily_timer.stop()
            self.daily_timer = None
        
        # 停止所有编码线程
        for script, thread in self.encoding_threads.items():
            if thread.running:
                thread.stop()
                thread.wait(5000)  # 等待5秒
        
        self.encoding_threads.clear()
    
    def run_on_exit(self):
        """程序退出时运行（如果今天还没运行过）"""
        if self._should_run_today():
            print("🔄 程序退出前执行编码（今天还未执行）...")
            self._run_encoding_scripts()
            
            # 等待所有线程完成
            for script, thread in self.encoding_threads.items():
                if thread.running:
                    thread.wait(10000)  # 等待10秒 