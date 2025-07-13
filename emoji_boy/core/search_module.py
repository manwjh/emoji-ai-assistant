"""
搜索模块 - 增强emoji_boy对数字世界的感知能力
"""

import webbrowser
import requests
import json
import urllib.parse
from typing import Optional, Dict, Any, List
import time
import re
from bs4 import BeautifulSoup
import config


class SearchModule:
    """搜索模块 - 提供多种搜索功能"""
    
    def __init__(self):
        """初始化搜索模块"""
        self.search_engines = {
            'google': 'https://www.google.com/search?q={}',
            'bing': 'https://www.bing.com/search?q={}',
            'baidu': 'https://www.baidu.com/s?wd={}',
            'duckduckgo': 'https://duckduckgo.com/?q={}'
        }
        
        # 默认搜索引擎
        self.default_engine = 'google'
        
        # 搜索历史
        self.search_history = []
        self.max_history = 20
        
        # 请求配置
        self.timeout = 10
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def web_search(self, query: str, engine: str = None, crawl_results: bool = True) -> Dict[str, Any]:
        """
        执行网页搜索
        
        Args:
            query: 搜索查询
            engine: 搜索引擎 ('google', 'bing', 'baidu', 'duckduckgo')
            crawl_results: 是否爬取搜索结果内容
            
        Returns:
            搜索结果字典
        """
        try:
            engine = engine or self.default_engine
            if engine not in self.search_engines:
                engine = self.default_engine
            
            # 构建搜索URL
            search_url = self.search_engines[engine].format(urllib.parse.quote(query))
            
            # 记录搜索历史
            self._add_to_history(query, engine, search_url)
            
            # 在默认浏览器中打开
            webbrowser.open(search_url)
            
            # 爬取搜索结果内容
            crawled_content = None
            if crawl_results:
                crawled_content = self._crawl_search_results(query, engine)
            
            return {
                'success': True,
                'query': query,
                'engine': engine,
                'url': search_url,
                'crawled_content': crawled_content,
                'message': f'🔍 已在{engine}中搜索: {query}' + (f'\n📄 已获取{len(crawled_content) if crawled_content else 0}条搜索结果' if crawled_content else '')
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': f'❌ 搜索失败: {str(e)}'
            }
    
    def smart_search(self, query: str, crawl_results: bool = True) -> Dict[str, Any]:
        """
        智能搜索 - 根据查询内容选择合适的搜索方式
        
        Args:
            query: 搜索查询
            crawl_results: 是否爬取搜索结果内容
            
        Returns:
            搜索结果
        """
        try:
            # 分析查询类型
            query_type = self._analyze_query_type(query)
            
            if query_type == 'knowledge':
                return self._knowledge_search(query, crawl_results)
            elif query_type == 'news':
                return self._news_search(query, crawl_results)
            elif query_type == 'image':
                return self._image_search(query, crawl_results)
            else:
                return self.web_search(query, crawl_results=crawl_results)
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': f'❌ 智能搜索失败: {str(e)}'
            }
    
    def _analyze_query_type(self, query: str) -> str:
        """分析查询类型"""
        query_lower = query.lower()
        
        # 知识类查询关键词
        knowledge_keywords = ['是什么', '如何', '怎么', '为什么', '定义', '概念', '原理', '方法']
        if any(keyword in query_lower for keyword in knowledge_keywords):
            return 'knowledge'
        
        # 新闻类查询关键词
        news_keywords = ['新闻', '最新', '今天', '昨天', '发生', '事件', '报道']
        if any(keyword in query_lower for keyword in news_keywords):
            return 'news'
        
        # 图片类查询关键词
        image_keywords = ['图片', '照片', '图像', '图标', 'logo', '壁纸']
        if any(keyword in query_lower for keyword in image_keywords):
            return 'image'
        
        return 'general'
    
    def _knowledge_search(self, query: str, crawl_results: bool = True) -> Dict[str, Any]:
        """知识搜索"""
        # 使用百度百科或维基百科搜索
        search_url = f"https://www.baidu.com/s?wd={urllib.parse.quote(query + ' 百科')}"
        webbrowser.open(search_url)
        
        # 爬取搜索结果
        crawled_content = None
        if crawl_results:
            crawled_content = self._crawl_search_results(query + ' 百科', 'baidu')
        
        return {
            'success': True,
            'query': query,
            'type': 'knowledge',
            'url': search_url,
            'crawled_content': crawled_content,
            'message': f'📚 知识搜索: {query}' + (f'\n📄 已获取{len(crawled_content) if crawled_content else 0}条百科结果' if crawled_content else '')
        }
    
    def _news_search(self, query: str, crawl_results: bool = True) -> Dict[str, Any]:
        """新闻搜索"""
        search_url = f"https://www.google.com/search?q={urllib.parse.quote(query + ' 新闻')}&tbm=nws"
        webbrowser.open(search_url)
        
        # 爬取搜索结果
        crawled_content = None
        if crawl_results:
            crawled_content = self._crawl_search_results(query + ' 新闻', 'google')
        
        return {
            'success': True,
            'query': query,
            'type': 'news',
            'url': search_url,
            'crawled_content': crawled_content,
            'message': f'📰 新闻搜索: {query}' + (f'\n📄 已获取{len(crawled_content) if crawled_content else 0}条新闻结果' if crawled_content else '')
        }
    
    def _image_search(self, query: str, crawl_results: bool = True) -> Dict[str, Any]:
        """图片搜索"""
        search_url = f"https://www.google.com/search?q={urllib.parse.quote(query)}&tbm=isch"
        webbrowser.open(search_url)
        
        # 图片搜索通常不需要爬取内容，但可以获取图片链接
        crawled_content = None
        if crawl_results:
            # 对于图片搜索，我们可以获取图片的链接信息
            try:
                response = requests.get(search_url, headers=self.headers, timeout=self.timeout)
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # 查找图片链接
                img_links = soup.find_all('img')
                crawled_content = []
                
                for img in img_links[:5]:  # 限制前5张图片
                    src = img.get('src', '')
                    alt = img.get('alt', '')
                    if src and not src.startswith('data:'):
                        crawled_content.append({
                            'title': alt or f'图片 {len(crawled_content) + 1}',
                            'link': src,
                            'snippet': f'图片链接: {src}'
                        })
                        
            except Exception as e:
                print(f"⚠️ 获取图片信息失败: {e}")
        
        return {
            'success': True,
            'query': query,
            'type': 'image',
            'url': search_url,
            'crawled_content': crawled_content,
            'message': f'🖼️ 图片搜索: {query}' + (f'\n📄 已获取{len(crawled_content) if crawled_content else 0}张图片' if crawled_content else '')
        }
    
    def search_with_context(self, query: str, context: str = "") -> Dict[str, Any]:
        """
        带上下文的搜索
        
        Args:
            query: 搜索查询
            context: 上下文信息
            
        Returns:
            搜索结果
        """
        try:
            # 如果有上下文，将其添加到查询中
            if context:
                enhanced_query = f"{context} {query}"
            else:
                enhanced_query = query
            
            return self.smart_search(enhanced_query)
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': f'❌ 上下文搜索失败: {str(e)}'
            }
    
    def get_search_suggestions(self, query: str) -> List[str]:
        """
        获取搜索建议
        
        Args:
            query: 查询词
            
        Returns:
            建议列表
        """
        try:
            # 这里可以集成搜索建议API
            # 目前返回基于历史的基本建议
            suggestions = []
            
            # 从历史记录中查找相关建议
            for hist in self.search_history:
                if query.lower() in hist['query'].lower():
                    suggestions.append(hist['query'])
            
            # 添加一些通用建议
            if '如何' in query:
                suggestions.extend([f"{query} 步骤", f"{query} 方法", f"{query} 教程"])
            elif '是什么' in query:
                suggestions.extend([f"{query} 定义", f"{query} 概念", f"{query} 解释"])
            
            return list(set(suggestions))[:5]  # 去重并限制数量
            
        except Exception as e:
            print(f"⚠️ 获取搜索建议失败: {e}")
            return []
    
    def _add_to_history(self, query: str, engine: str, url: str):
        """添加到搜索历史"""
        history_item = {
            'query': query,
            'engine': engine,
            'url': url,
            'timestamp': time.time()
        }
        
        self.search_history.append(history_item)
        
        # 限制历史记录数量
        if len(self.search_history) > self.max_history:
            self.search_history = self.search_history[-self.max_history:]
    
    def get_search_history(self) -> List[Dict[str, Any]]:
        """获取搜索历史"""
        return self.search_history.copy()
    
    def clear_search_history(self):
        """清空搜索历史"""
        self.search_history.clear()
    
    def get_status(self) -> Dict[str, Any]:
        """获取搜索模块状态"""
        return {
            'available_engines': list(self.search_engines.keys()),
            'default_engine': self.default_engine,
            'history_count': len(self.search_history),
            'max_history': self.max_history
        }
    
    def set_default_engine(self, engine: str):
        """设置默认搜索引擎"""
        if engine in self.search_engines:
            self.default_engine = engine
            return True
        return False
    
    def _crawl_search_results(self, query: str, engine: str) -> List[Dict[str, str]]:
        """
        爬取搜索结果内容
        
        Args:
            query: 搜索查询
            engine: 搜索引擎
            
        Returns:
            搜索结果列表
        """
        try:
            # 构建搜索URL
            search_url = self.search_engines[engine].format(urllib.parse.quote(query))
            
            # 发送HTTP请求
            response = requests.get(search_url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            
            # 解析HTML内容
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 根据搜索引擎提取搜索结果
            if engine == 'google':
                return self._extract_google_results(soup)
            elif engine == 'bing':
                return self._extract_bing_results(soup)
            elif engine == 'baidu':
                return self._extract_baidu_results(soup)
            else:
                return self._extract_generic_results(soup)
                
        except Exception as e:
            print(f"⚠️ 爬取搜索结果失败: {e}")
            return []
    
    def _extract_google_results(self, soup) -> List[Dict[str, str]]:
        """提取Google搜索结果"""
        results = []
        
        try:
            # 查找搜索结果容器
            search_results = soup.find_all('div', class_='g')
            
            for result in search_results[:5]:  # 限制前5个结果
                try:
                    # 提取标题
                    title_elem = result.find('h3')
                    title = title_elem.get_text().strip() if title_elem else ""
                    
                    # 提取链接
                    link_elem = result.find('a')
                    link = link_elem.get('href') if link_elem else ""
                    
                    # 提取摘要
                    snippet_elem = result.find('div', class_='VwiC3b')
                    snippet = snippet_elem.get_text().strip() if snippet_elem else ""
                    
                    if title and link:
                        results.append({
                            'title': title,
                            'link': link,
                            'snippet': snippet
                        })
                        
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"⚠️ 提取Google结果失败: {e}")
        
        return results
    
    def _extract_bing_results(self, soup) -> List[Dict[str, str]]:
        """提取Bing搜索结果"""
        results = []
        
        try:
            # 查找搜索结果容器
            search_results = soup.find_all('li', class_='b_algo')
            
            for result in search_results[:5]:  # 限制前5个结果
                try:
                    # 提取标题
                    title_elem = result.find('h2')
                    title = title_elem.get_text().strip() if title_elem else ""
                    
                    # 提取链接
                    link_elem = result.find('a')
                    link = link_elem.get('href') if link_elem else ""
                    
                    # 提取摘要
                    snippet_elem = result.find('p')
                    snippet = snippet_elem.get_text().strip() if snippet_elem else ""
                    
                    if title and link:
                        results.append({
                            'title': title,
                            'link': link,
                            'snippet': snippet
                        })
                        
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"⚠️ 提取Bing结果失败: {e}")
        
        return results
    
    def _extract_baidu_results(self, soup) -> List[Dict[str, str]]:
        """提取百度搜索结果"""
        results = []
        
        try:
            # 查找搜索结果容器
            search_results = soup.find_all('div', class_='result')
            
            for result in search_results[:5]:  # 限制前5个结果
                try:
                    # 提取标题
                    title_elem = result.find('h3')
                    title = title_elem.get_text().strip() if title_elem else ""
                    
                    # 提取链接
                    link_elem = result.find('a')
                    link = link_elem.get('href') if link_elem else ""
                    
                    # 提取摘要
                    snippet_elem = result.find('div', class_='c-abstract')
                    snippet = snippet_elem.get_text().strip() if snippet_elem else ""
                    
                    if title and link:
                        results.append({
                            'title': title,
                            'link': link,
                            'snippet': snippet
                        })
                        
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"⚠️ 提取百度结果失败: {e}")
        
        return results
    
    def _extract_generic_results(self, soup) -> List[Dict[str, str]]:
        """提取通用搜索结果"""
        results = []
        
        try:
            # 尝试查找常见的搜索结果元素
            title_selectors = ['h1', 'h2', 'h3', '.title', '.result-title']
            link_selectors = ['a[href]']
            snippet_selectors = ['p', '.snippet', '.description', '.summary']
            
            # 查找所有链接
            links = soup.find_all('a', href=True)
            
            for link in links[:10]:  # 限制前10个链接
                try:
                    title = link.get_text().strip()
                    href = link.get('href')
                    
                    # 过滤掉无效链接
                    if not title or not href or href.startswith('#') or 'javascript:' in href:
                        continue
                    
                    # 查找相关的摘要
                    snippet = ""
                    parent = link.parent
                    if parent:
                        snippet_elem = parent.find(['p', 'div', 'span'])
                        if snippet_elem:
                            snippet = snippet_elem.get_text().strip()[:200]  # 限制长度
                    
                    results.append({
                        'title': title,
                        'link': href,
                        'snippet': snippet
                    })
                    
                    if len(results) >= 5:  # 限制结果数量
                        break
                        
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"⚠️ 提取通用结果失败: {e}")
        
        return results
    
    def get_search_summary(self, crawled_content: List[Dict[str, str]]) -> str:
        """
        生成搜索结果摘要
        
        Args:
            crawled_content: 爬取的搜索结果
            
        Returns:
            搜索结果摘要
        """
        if not crawled_content:
            return "未找到相关搜索结果"
        
        summary_parts = []
        summary_parts.append(f"找到 {len(crawled_content)} 条相关结果：")
        
        for i, result in enumerate(crawled_content[:3], 1):  # 只显示前3个结果
            title = result.get('title', '')
            snippet = result.get('snippet', '')
            
            summary_parts.append(f"\n{i}. {title}")
            if snippet:
                # 限制摘要长度
                snippet_short = snippet[:100] + "..." if len(snippet) > 100 else snippet
                summary_parts.append(f"   {snippet_short}")
        
        return "\n".join(summary_parts)


# 全局搜索模块实例
search_module = SearchModule() 