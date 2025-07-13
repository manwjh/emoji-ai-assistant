"""
Search Plugin - 搜索插件

处理用户搜索相关的意图，包括信息搜索、资料查找等。
"""

from typing import Dict, Any, Optional
try:
    from .base_plugin import BasePlugin, PluginPriority
except (ImportError, SystemError):
    from brain_agent.plugins.base_plugin import BasePlugin, PluginPriority


class SearchPlugin(BasePlugin):
    """搜索插件"""
    
    def __init__(self):
        super().__init__(
            name="search_plugin",
            description="处理搜索相关的用户意图，提供信息搜索和资料查找功能",
            priority=PluginPriority.HIGH
        )
        
        # 插件元数据
        self.metadata.update({
            "tags": ["search", "information", "find"],
            "dependencies": [],
            "config_schema": {
                "max_results": {"type": int, "default": 5},
                "search_timeout": {"type": int, "default": 10}
            }
        })
        
        # 搜索关键词
        self.search_keywords = [
            '搜索', '查找', '找', '帮我找', '帮我搜索', '帮我查找',
            '如何', '怎么', '什么是', '最新', '新闻', '信息',
            'search', 'find', 'look for', 'help me find'
        ]
    
    def can_handle(self, intent_data: Dict[str, Any]) -> bool:
        """判断是否能处理该意图"""
        intent_type = intent_data.get("intent_type", "")
        return intent_type == "search"
    
    def handle(self, intent_data: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """处理搜索意图"""
        try:
            # 获取搜索查询
            search_query = intent_data.get("search_query", "")
            if not search_query:
                search_query = intent_data.get("message", "")
            
            # 清理搜索查询
            search_query = self._clean_search_query(search_query)
            
            if not search_query:
                return {
                    "success": False,
                    "error": "搜索查询为空",
                    "suggestion": "请提供具体的搜索内容"
                }
            
            # 执行搜索
            search_results = self._perform_search(search_query, context)
            
            return {
                "success": True,
                "search_query": search_query,
                "results": search_results,
                "result_count": len(search_results),
                "message": f"为您搜索到 {len(search_results)} 条相关结果"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"搜索执行失败: {str(e)}"
            }
    
    def _clean_search_query(self, query: str) -> str:
        """清理搜索查询"""
        if not query:
            return ""
        
        # 移除搜索关键词
        cleaned_query = query
        for keyword in self.search_keywords:
            if keyword in cleaned_query.lower():
                cleaned_query = cleaned_query.replace(keyword, '').replace('帮我', '').strip()
                break
        
        # 移除多余空格
        cleaned_query = ' '.join(cleaned_query.split())
        
        return cleaned_query
    
    def _perform_search(self, query: str, context: Dict[str, Any] = None) -> list:
        """
        执行搜索
        
        Args:
            query: 搜索查询
            context: 上下文信息
            
        Returns:
            list: 搜索结果列表
        """
        # 这里可以集成各种搜索服务
        # 目前返回模拟结果
        
        max_results = self.metadata["config_schema"]["max_results"]["default"]
        
        # 模拟搜索结果
        mock_results = [
            {
                "title": f"关于 '{query}' 的搜索结果 1",
                "content": f"这是关于 {query} 的相关信息...",
                "url": f"https://example.com/search?q={query}",
                "source": "模拟搜索",
                "relevance": 0.95
            },
            {
                "title": f"'{query}' 相关信息 2",
                "content": f"更多关于 {query} 的详细内容...",
                "url": f"https://example.com/info/{query}",
                "source": "模拟搜索",
                "relevance": 0.87
            }
        ]
        
        # 限制结果数量
        return mock_results[:max_results]
    
    def get_help(self) -> str:
        """获取插件帮助信息"""
        return """
搜索插件帮助：
- 支持关键词搜索：搜索 [关键词]
- 支持问题搜索：如何 [问题]
- 支持信息查找：查找 [信息]
- 支持最新信息：最新 [主题]

示例：
- "搜索Python教程"
- "如何学习机器学习"
- "查找最新科技新闻"
        """
    
    def get_stats(self) -> Dict[str, Any]:
        """获取插件统计信息"""
        base_stats = super().get_stats()
        base_stats.update({
            "search_keywords_count": len(self.search_keywords),
            "plugin_type": "search"
        })
        return base_stats 