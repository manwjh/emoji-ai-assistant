"""
Plugin Registry - 技能网络系统

负责管理所有技能模块的注册、查找、启用/禁用和执行。
模仿人脑的技能网络，提供技能生命周期管理和执行统计功能。
"""

import time
import logging
from typing import Dict, Any, List, Optional, Type
try:
    from .plugins.base_plugin import BasePlugin, PluginPriority
except (ImportError, SystemError):
    from brain_agent.plugins.base_plugin import BasePlugin, PluginPriority

# 配置日志
logger = logging.getLogger(__name__)


class PluginRegistry:
    """技能网络系统 - 模仿人脑的技能网络"""
    
    def __init__(self):
        """初始化技能网络系统"""
        self._plugins: Dict[str, BasePlugin] = {}
        self._plugin_classes: Dict[str, Type[BasePlugin]] = {}
        self._execution_stats = {
            "total_executions": 0,
            "successful_executions": 0,
            "failed_executions": 0,
            "execution_times": [],
            "plugin_usage": {}  # 记录每个技能的使用次数
        }
        
        logger.info("技能网络系统初始化完成")
    
    def register_plugin(self, plugin: BasePlugin) -> bool:
        """
        注册技能模块
        
        Args:
            plugin: 技能模块实例
            
        Returns:
            bool: 注册是否成功
        """
        if not isinstance(plugin, BasePlugin):
            raise ValueError("技能模块必须继承BasePlugin")
        
        if not plugin.name:
            raise ValueError("技能模块名称不能为空")
        
        if plugin.name in self._plugins:
            logger.warning(f"技能模块 {plugin.name} 已存在，将被覆盖")
        
        self._plugins[plugin.name] = plugin
        self._execution_stats["plugin_usage"][plugin.name] = 0
        
        logger.info(f"技能模块 {plugin.name} 注册成功 (优先级: {plugin.priority.name})")
        return True
    
    def register_plugin_class(self, plugin_class: Type[BasePlugin], **kwargs) -> bool:
        """
        注册技能模块类
        
        Args:
            plugin_class: 技能模块类
            **kwargs: 技能模块初始化参数
            
        Returns:
            bool: 注册是否成功
        """
        try:
            plugin_instance = plugin_class(**kwargs)
            return self.register_plugin(plugin_instance)
        except Exception as e:
            logger.error(f"技能模块类注册失败: {e}")
            return False
    
    def unregister_plugin(self, plugin_name: str) -> bool:
        """
        注销技能模块
        
        Args:
            plugin_name: 技能模块名称
            
        Returns:
            bool: 注销是否成功
        """
        if plugin_name in self._plugins:
            del self._plugins[plugin_name]
            if plugin_name in self._execution_stats["plugin_usage"]:
                del self._execution_stats["plugin_usage"][plugin_name]
            
            logger.info(f"技能模块 {plugin_name} 注销成功")
            return True
        
        logger.warning(f"技能模块 {plugin_name} 不存在，无法注销")
        return False
    
    def get_plugin(self, plugin_name: str) -> Optional[BasePlugin]:
        """
        获取技能模块
        
        Args:
            plugin_name: 技能模块名称
            
        Returns:
            BasePlugin: 技能模块实例，如果不存在返回None
        """
        return self._plugins.get(plugin_name)
    
    def get_all_plugins(self) -> List[BasePlugin]:
        """
        获取所有技能模块
        
        Returns:
            List[BasePlugin]: 技能模块列表
        """
        return list(self._plugins.values())
    
    def get_enabled_plugins(self) -> List[BasePlugin]:
        """
        获取所有启用的技能模块
        
        Returns:
            List[BasePlugin]: 启用的技能模块列表
        """
        return [plugin for plugin in self._plugins.values() if plugin.is_enabled()]
    
    def find_plugins_for_intent(self, intent_data: Dict[str, Any]) -> List[BasePlugin]:
        """
        查找能处理指定意图的技能模块
        
        Args:
            intent_data: 意图数据
            
        Returns:
            List[BasePlugin]: 能处理的技能模块列表，按优先级排序
        """
        suitable_plugins = []
        
        for plugin in self.get_enabled_plugins():
            try:
                if plugin.can_handle(intent_data):
                    suitable_plugins.append(plugin)
                    logger.debug(f"技能模块 {plugin.name} 可以处理意图: {intent_data.get('intent_type')}")
            except Exception as e:
                logger.warning(f"技能模块 {plugin.name} 检查意图时出错: {e}")
                continue
        
        # 按优先级排序（高优先级在前）
        suitable_plugins.sort(key=lambda p: p.priority.value, reverse=True)
        
        if suitable_plugins:
            logger.info(f"找到 {len(suitable_plugins)} 个技能模块处理意图: {intent_data.get('intent_type')}")
        else:
            logger.warning(f"没有找到技能模块处理意图: {intent_data.get('intent_type')}")
        
        return suitable_plugins
    
    def execute_plugin(self, plugin: BasePlugin, intent_data: Dict[str, Any], 
                      context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        执行技能模块
        
        Args:
            plugin: 技能模块实例
            intent_data: 意图数据
            context: 上下文信息
            
        Returns:
            Dict: 执行结果
        """
        start_time = time.time()
        self._execution_stats["total_executions"] += 1
        
        # 更新技能使用统计
        if plugin.name in self._execution_stats["plugin_usage"]:
            self._execution_stats["plugin_usage"][plugin.name] += 1
        
        try:
            logger.debug(f"执行技能模块: {plugin.name}")
            result = plugin.handle(intent_data, context)
            execution_time = time.time() - start_time
            
            self._execution_stats["successful_executions"] += 1
            self._execution_stats["execution_times"].append(execution_time)
            
            # 限制执行时间记录数量
            if len(self._execution_stats["execution_times"]) > 1000:
                self._execution_stats["execution_times"] = self._execution_stats["execution_times"][-500:]
            
            result["execution_time"] = execution_time
            result["plugin_name"] = plugin.name
            
            logger.info(f"技能模块 {plugin.name} 执行成功 (耗时: {execution_time:.3f}s)")
            return result
            
        except Exception as e:
            self._execution_stats["failed_executions"] += 1
            execution_time = time.time() - start_time
            
            logger.error(f"技能模块 {plugin.name} 执行失败: {e}")
            return {
                "success": False,
                "error": str(e),
                "plugin_name": plugin.name,
                "execution_time": execution_time
            }
    
    def execute_intent(self, intent_data: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        执行意图（自动选择合适的技能模块）
        
        Args:
            intent_data: 意图数据
            context: 上下文信息
            
        Returns:
            Dict: 执行结果
        """
        suitable_plugins = self.find_plugins_for_intent(intent_data)
        
        if not suitable_plugins:
            logger.warning(f"没有找到合适的技能模块处理意图: {intent_data.get('intent_type')}")
            return {
                "success": False,
                "error": "没有找到合适的技能模块处理该意图",
                "intent_type": intent_data.get("intent_type", "unknown")
            }
        
        # 执行最高优先级的技能模块
        primary_plugin = suitable_plugins[0]
        result = self.execute_plugin(primary_plugin, intent_data, context)
        
        # 如果有多个技能模块，记录备选技能
        if len(suitable_plugins) > 1:
            result["alternative_plugins"] = [p.name for p in suitable_plugins[1:]]
            logger.debug(f"备选技能模块: {result['alternative_plugins']}")
        
        return result
    
    def enable_plugin(self, plugin_name: str) -> bool:
        """
        启用技能模块
        
        Args:
            plugin_name: 技能模块名称
            
        Returns:
            bool: 启用是否成功
        """
        plugin = self.get_plugin(plugin_name)
        if plugin:
            plugin.enable()
            logger.info(f"技能模块 {plugin_name} 已启用")
            return True
        else:
            logger.warning(f"技能模块 {plugin_name} 不存在，无法启用")
            return False
    
    def disable_plugin(self, plugin_name: str) -> bool:
        """
        禁用技能模块
        
        Args:
            plugin_name: 技能模块名称
            
        Returns:
            bool: 禁用是否成功
        """
        plugin = self.get_plugin(plugin_name)
        if plugin:
            plugin.disable()
            logger.info(f"技能模块 {plugin_name} 已禁用")
            return True
        else:
            logger.warning(f"技能模块 {plugin_name} 不存在，无法禁用")
            return False
    
    def get_plugin_stats(self) -> Dict[str, Any]:
        """
        获取技能网络统计信息
        
        Returns:
            Dict: 统计信息
        """
        stats = self._execution_stats.copy()
        
        # 计算成功率
        if stats["total_executions"] > 0:
            stats["success_rate"] = stats["successful_executions"] / stats["total_executions"]
        else:
            stats["success_rate"] = 0.0
        
        # 计算平均执行时间
        if stats["execution_times"]:
            stats["average_execution_time"] = sum(stats["execution_times"]) / len(stats["execution_times"])
        else:
            stats["average_execution_time"] = 0.0
        
        # 技能模块统计
        stats["plugin_count"] = len(self._plugins)
        stats["enabled_plugin_count"] = len(self.get_enabled_plugins())
        
        # 最常用的技能模块
        if stats["plugin_usage"]:
            most_used = max(stats["plugin_usage"].items(), key=lambda x: x[1])
            stats["most_used_plugin"] = {
                "name": most_used[0],
                "usage_count": most_used[1]
            }
        
        return stats
    
    def list_plugins(self) -> List[Dict[str, Any]]:
        """
        列出所有技能模块信息
        
        Returns:
            List[Dict]: 技能模块信息列表
        """
        plugins_info = []
        
        for plugin in self._plugins.values():
            usage_count = self._execution_stats["plugin_usage"].get(plugin.name, 0)
            
            plugins_info.append({
                "name": plugin.name,
                "description": plugin.description,
                "priority": plugin.priority.name,
                "enabled": plugin.is_enabled(),
                "usage_count": usage_count
            })
        
        # 按优先级排序
        plugins_info.sort(key=lambda x: PluginPriority[x["priority"]].value, reverse=True)
        
        return plugins_info
    
    def clear_plugins(self):
        """清空所有技能模块"""
        self._plugins.clear()
        self._execution_stats["plugin_usage"].clear()
        logger.info("所有技能模块已清空")
    
    def reload_plugin(self, plugin_name: str) -> bool:
        """
        重新加载技能模块
        
        Args:
            plugin_name: 技能模块名称
            
        Returns:
            bool: 重载是否成功
        """
        plugin = self.get_plugin(plugin_name)
        if plugin:
            try:
                # 这里可以实现技能模块热重载逻辑
                logger.info(f"技能模块 {plugin_name} 重载成功")
                return True
            except Exception as e:
                logger.error(f"技能模块 {plugin_name} 重载失败: {e}")
                return False
        else:
            logger.warning(f"技能模块 {plugin_name} 不存在，无法重载")
            return False
    
    def get_plugin_by_intent_type(self, intent_type: str) -> Optional[BasePlugin]:
        """
        根据意图类型获取技能模块
        
        Args:
            intent_type: 意图类型
            
        Returns:
            BasePlugin: 技能模块实例，如果不存在返回None
        """
        for plugin in self.get_enabled_plugins():
            try:
                # 创建测试意图数据
                test_intent = {"intent_type": intent_type}
                if plugin.can_handle(test_intent):
                    return plugin
            except Exception:
                continue
        
        return None
    
    def validate_plugins(self) -> Dict[str, Any]:
        """
        验证所有技能模块的完整性
        
        Returns:
            Dict: 验证结果
        """
        validation_result = {
            "total_plugins": len(self._plugins),
            "valid_plugins": 0,
            "invalid_plugins": 0,
            "errors": []
        }
        
        for plugin_name, plugin in self._plugins.items():
            try:
                # 检查技能模块基本属性
                if not hasattr(plugin, 'name') or not plugin.name:
                    raise ValueError("技能模块名称缺失")
                
                if not hasattr(plugin, 'can_handle') or not callable(plugin.can_handle):
                    raise ValueError("can_handle方法缺失或不可调用")
                
                if not hasattr(plugin, 'handle') or not callable(plugin.handle):
                    raise ValueError("handle方法缺失或不可调用")
                
                validation_result["valid_plugins"] += 1
                
            except Exception as e:
                validation_result["invalid_plugins"] += 1
                validation_result["errors"].append({
                    "plugin": plugin_name,
                    "error": str(e)
                })
        
        logger.info(f"技能模块验证完成: {validation_result['valid_plugins']}/{validation_result['total_plugins']} 有效")
        return validation_result


# 全局技能网络系统实例
plugin_registry = PluginRegistry() 