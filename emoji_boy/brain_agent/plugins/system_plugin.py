"""
系统命令执行插件 - 处理系统相关查询和命令执行

支持的功能：
- 时间查询（今天几号、现在时间等）
- 系统信息查询
- 基本系统命令执行
"""

import os
import subprocess
import platform
import datetime
import re
from typing import Dict, Any, Optional
try:
    from .base_plugin import BasePlugin, PluginPriority
except (ImportError, SystemError):
    from brain_agent.plugins.base_plugin import BasePlugin, PluginPriority


class SystemPlugin(BasePlugin):
    """系统命令执行插件"""
    
    def __init__(self):
        super().__init__(
            name="system_plugin",
            description="系统命令执行和系统信息查询",
            priority=PluginPriority.HIGH
        )
        
        # 时间相关关键词
        self.time_keywords = [
            "今天几号", "现在几号", "今天日期", "现在日期",
            "今天时间", "现在时间", "几点", "几点了",
            "日期", "时间", "星期", "周几"
        ]
        
        # 系统信息关键词
        self.system_keywords = [
            "系统信息", "系统版本", "操作系统", "平台信息",
            "CPU信息", "内存信息", "磁盘信息", "网络信息"
        ]
        
        # 安全命令白名单
        self.safe_commands = {
            "date": "获取系统时间",
            "whoami": "获取当前用户",
            "pwd": "获取当前目录",
            "ls": "列出目录内容",
            "ps": "查看进程信息",
            "df": "查看磁盘使用情况",
            "free": "查看内存使用情况",
            "uname": "查看系统信息"
        }
    
    def can_handle(self, intent_data: Dict[str, Any]) -> bool:
        """判断是否能处理该意图"""
        intent_type = intent_data.get("intent_type", "")
        user_message = intent_data.get("user_message", "").lower()
        
        # 检查是否是系统相关意图
        if intent_type == "system":
            return True
        
        # 检查是否包含时间相关关键词
        if any(keyword in user_message for keyword in self.time_keywords):
            return True
        
        # 检查是否包含系统信息关键词
        if any(keyword in user_message for keyword in self.system_keywords):
            return True
        
        return False
    
    def handle(self, intent_data: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """处理系统相关请求"""
        user_message = intent_data.get("user_message", "")
        
        try:
            # 处理时间查询
            if self._is_time_query(user_message):
                return self._handle_time_query()
            
            # 处理系统信息查询
            elif self._is_system_info_query(user_message):
                return self._handle_system_info_query()
            
            # 处理系统命令执行
            elif self._is_command_execution(user_message):
                return self._handle_command_execution(user_message)
            
            # 默认返回系统状态
            else:
                return self._handle_system_status()
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"❌ 系统操作失败: {str(e)}"
            }
    
    def _is_time_query(self, message: str) -> bool:
        """判断是否是时间查询"""
        return any(keyword in message for keyword in self.time_keywords)
    
    def _is_system_info_query(self, message: str) -> bool:
        """判断是否是系统信息查询"""
        return any(keyword in message for keyword in self.system_keywords)
    
    def _is_command_execution(self, message: str) -> bool:
        """判断是否是命令执行请求"""
        # 检查是否包含命令执行关键词
        command_keywords = ["执行", "运行", "命令", "cmd", "shell"]
        return any(keyword in message for keyword in command_keywords)
    
    def _handle_time_query(self) -> Dict[str, Any]:
        """处理时间查询"""
        now = datetime.datetime.now()
        
        # 格式化时间信息
        date_str = now.strftime("%Y年%m月%d日")
        time_str = now.strftime("%H:%M:%S")
        weekday_str = now.strftime("%A")  # 英文星期
        
        # 中文星期映射
        weekday_cn = {
            "Monday": "星期一",
            "Tuesday": "星期二", 
            "Wednesday": "星期三",
            "Thursday": "星期四",
            "Friday": "星期五",
            "Saturday": "星期六",
            "Sunday": "星期日"
        }
        
        weekday_cn_str = weekday_cn.get(weekday_str, weekday_str)
        
        # 尝试获取系统时间命令结果
        system_time = self._get_system_time()
        
        return {
            "success": True,
            "message": f"📅 今天是 {date_str} {weekday_cn_str}\n🕐 现在时间是 {time_str}",
            "data": {
                "date": date_str,
                "time": time_str,
                "weekday": weekday_cn_str,
                "system_time": system_time,
                "timestamp": now.timestamp()
            }
        }
    
    def _handle_system_info_query(self) -> Dict[str, Any]:
        """处理系统信息查询"""
        try:
            system_info = {
                "platform": platform.system(),
                "platform_version": platform.version(),
                "architecture": platform.architecture()[0],
                "processor": platform.processor(),
                "python_version": platform.python_version(),
                "hostname": platform.node()
            }
            
            # 获取更详细的系统信息
            if platform.system() == "Darwin":  # macOS
                system_info.update(self._get_macos_info())
            elif platform.system() == "Windows":
                system_info.update(self._get_windows_info())
            elif platform.system() == "Linux":
                system_info.update(self._get_linux_info())
            
            info_text = f"💻 系统信息:\n"
            info_text += f"• 操作系统: {system_info['platform']} {system_info['platform_version']}\n"
            info_text += f"• 架构: {system_info['architecture']}\n"
            info_text += f"• 处理器: {system_info['processor']}\n"
            info_text += f"• Python版本: {system_info['python_version']}\n"
            info_text += f"• 主机名: {system_info['hostname']}"
            
            return {
                "success": True,
                "message": info_text,
                "data": system_info
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"❌ 获取系统信息失败: {str(e)}"
            }
    
    def _handle_command_execution(self, message: str) -> Dict[str, Any]:
        """处理命令执行请求"""
        # 提取命令（这里简化处理，实际应用中需要更复杂的解析）
        command_match = re.search(r'执行\s*([^\s]+)', message)
        if not command_match:
            return {
                "success": False,
                "message": "❌ 未找到要执行的命令，请明确指定要执行的命令"
            }
        
        command = command_match.group(1)
        
        # 检查命令安全性
        if not self._is_safe_command(command):
            return {
                "success": False,
                "message": f"❌ 出于安全考虑，不允许执行命令: {command}"
            }
        
        try:
            # 执行命令
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            
            if result.returncode == 0:
                return {
                    "success": True,
                    "message": f"✅ 命令执行成功:\n{result.stdout}",
                    "data": {
                        "command": command,
                        "stdout": result.stdout,
                        "stderr": result.stderr,
                        "returncode": result.returncode
                    }
                }
            else:
                return {
                    "success": False,
                    "message": f"❌ 命令执行失败:\n{result.stderr}",
                    "data": {
                        "command": command,
                        "stdout": result.stdout,
                        "stderr": result.stderr,
                        "returncode": result.returncode
                    }
                }
                
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "message": "❌ 命令执行超时"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"❌ 命令执行异常: {str(e)}"
            }
    
    def _handle_system_status(self) -> Dict[str, Any]:
        """处理系统状态查询"""
        return {
            "success": True,
            "message": "🖥️ 系统运行正常\n💡 你可以询问:\n• 时间日期信息\n• 系统信息\n• 执行安全命令",
            "data": {
                "status": "running",
                "available_features": ["time_query", "system_info", "safe_commands"]
            }
        }
    
    def _get_system_time(self) -> str:
        """获取系统时间命令结果"""
        try:
            result = subprocess.run(
                "date", 
                shell=True, 
                capture_output=True, 
                text=True, 
                timeout=5
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass
        return ""
    
    def _is_safe_command(self, command: str) -> bool:
        """检查命令是否安全"""
        # 检查是否在白名单中
        base_command = command.split()[0] if command else ""
        return base_command in self.safe_commands
    
    def _get_macos_info(self) -> Dict[str, str]:
        """获取macOS系统信息"""
        info = {}
        try:
            # 获取macOS版本
            result = subprocess.run(
                "sw_vers -productVersion", 
                shell=True, 
                capture_output=True, 
                text=True
            )
            if result.returncode == 0:
                info["macos_version"] = result.stdout.strip()
        except:
            pass
        return info
    
    def _get_windows_info(self) -> Dict[str, str]:
        """获取Windows系统信息"""
        info = {}
        try:
            # 获取Windows版本
            result = subprocess.run(
                "ver", 
                shell=True, 
                capture_output=True, 
                text=True
            )
            if result.returncode == 0:
                info["windows_version"] = result.stdout.strip()
        except:
            pass
        return info
    
    def _get_linux_info(self) -> Dict[str, str]:
        """获取Linux系统信息"""
        info = {}
        try:
            # 获取Linux发行版信息
            result = subprocess.run(
                "cat /etc/os-release", 
                shell=True, 
                capture_output=True, 
                text=True
            )
            if result.returncode == 0:
                info["linux_distro"] = result.stdout.strip()
        except:
            pass
        return info 