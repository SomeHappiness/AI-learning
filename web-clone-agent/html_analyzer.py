#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
HTML分析器模块 (html_analyzer.py)
-----------------------------
本模块负责分析网页的HTML结构，识别组件和布局。

主要功能:
1. 解析HTML文档结构
2. 识别页面主要组件（导航栏、页眉、页脚等）
3. 分析页面布局结构
4. 提取元数据（标题、描述等）
5. 为Vue组件生成准备元素分类

工作原理:
该模块使用BeautifulSoup4解析HTML，然后通过分析标签结构、类名和ID等来
识别页面的逻辑部分和组件，为后续生成Vue组件提供基础。
"""

import re
import logging
from bs4 import BeautifulSoup
from collections import Counter

# 配置日志
logger = logging.getLogger(__name__)

class HtmlAnalyzer:
    """
    HTML分析器类
    
    负责解析和分析HTML内容，提取组件和布局结构。
    这是Vue组件生成的关键前置步骤。
    """
    
    def __init__(self):
        """
        初始化HTML分析器
        
        设置组件识别的基本规则和阈值。
        """
        # 常见组件标识符（用于识别页面组件）
        self.component_identifiers = {
            'navigation': ['nav', 'navbar', 'menu', 'header', 'navigation'],
            'header': ['header', 'banner', 'hero', 'jumbotron', 'masthead'],
            'footer': ['footer', 'bottom', 'foot'],
            'sidebar': ['sidebar', 'side', 'sidenav', 'aside'],
            'content': ['content', 'main', 'article', 'post'],
            'card': ['card', 'box', 'panel', 'tile'],
            'form': ['form', 'contact-form', 'login', 'signup', 'register'],
            'button': ['btn', 'button', 'cta'],
            'carousel': ['carousel', 'slider', 'slideshow'],
            'modal': ['modal', 'dialog', 'popup'],
            'tab': ['tab', 'tabs'],
            'accordion': ['accordion', 'collapse', 'dropdown']
        }
        
        # 页面划分时的最小文本长度要求
        self.min_text_length = 10
        
        # 组件最小内容要求
        self.min_component_size = 50
    
    def analyze(self, html_content):
        """
        分析HTML内容
        
        这是主要的公共方法，完成整个HTML分析流程。
        
        参数:
            html_content (str): 页面HTML内容
        
        返回:
            dict: 包含页面结构、组件和元数据的分析结果
        """
        try:
            logger.info("开始分析HTML内容")
        
        # 使用BeautifulSoup解析HTML
            soup = BeautifulSoup(html_content, 'html.parser')
        
            # 初始化结果字典
            result = {
                'title': self._extract_title(soup),
                'meta': self._extract_meta(soup),
                'structure': self._analyze_structure(soup),
                'components': self._identify_components(soup),
                'layout': self._analyze_layout(soup)
            }
            
            logger.info("HTML分析完成")
            return result
            
        except Exception as e:
            logger.error(f"分析HTML内容时出错: {str(e)}")
            raise
    
    def _extract_title(self, soup):
        """
        提取页面标题
        
        参数:
            soup (BeautifulSoup): 已解析的HTML
            
        返回:
            str: 页面标题
        """
        # 尝试从<title>标签获取标题
        title_tag = soup.find('title')
        if title_tag and title_tag.string:
            return title_tag.string.strip()
        
        # 如果没有<title>标签，尝试从h1标签获取
        h1_tag = soup.find('h1')
        if h1_tag and h1_tag.string:
            return h1_tag.string.strip()
        
        # 最后返回默认标题
        return "未命名页面"
    
    def _extract_meta(self, soup):
        """
        提取页面元数据（如描述、关键词等）
        
        参数:
            soup (BeautifulSoup): 已解析的HTML
            
        返回:
            dict: 包含元数据的字典
        """
        meta_data = {
            'description': '',
            'keywords': '',
            'author': '',
            'viewport': '',
            'charset': '',
            'language': 'zh-CN',  # 默认语言
            'og_tags': {},        # Open Graph标签
            'twitter_tags': {}    # Twitter卡片标签
        }
        
        # 提取基本元数据
        for meta in soup.find_all('meta'):
            # 获取描述
            if meta.get('name') == 'description' and meta.get('content'):
                meta_data['description'] = meta.get('content')
            
            # 获取关键词
            elif meta.get('name') == 'keywords' and meta.get('content'):
                meta_data['keywords'] = meta.get('content')
            
            # 获取作者
            elif meta.get('name') == 'author' and meta.get('content'):
                meta_data['author'] = meta.get('content')
            
            # 获取视口设置
            elif meta.get('name') == 'viewport' and meta.get('content'):
                meta_data['viewport'] = meta.get('content')
            
            # 获取字符集
            elif meta.get('charset'):
                meta_data['charset'] = meta.get('charset')
                
            # 提取Open Graph标签
            elif meta.get('property') and meta.get('property').startswith('og:'):
                property_name = meta.get('property')[3:]  # 去掉'og:'前缀
                meta_data['og_tags'][property_name] = meta.get('content', '')
                
            # 提取Twitter卡片标签
            elif meta.get('name') and meta.get('name').startswith('twitter:'):
                property_name = meta.get('name')[8:]  # 去掉'twitter:'前缀
                meta_data['twitter_tags'][property_name] = meta.get('content', '')
        
        # 提取语言
        html_tag = soup.find('html')
        if html_tag and html_tag.get('lang'):
            meta_data['language'] = html_tag.get('lang')
        
        return meta_data
    
    def _analyze_structure(self, soup):
        """
        分析HTML文档结构
        
        检查文档的结构是否符合现代Web标准，如是否有语义化标签。
        
        参数:
            soup (BeautifulSoup): 已解析的HTML
            
        返回:
            dict: 文档结构分析结果
        """
        # 初始化结构信息字典
        structure = {
            'has_header': bool(soup.find('header')),
            'has_footer': bool(soup.find('footer')),
            'has_nav': bool(soup.find('nav')),
            'has_main': bool(soup.find('main')),
            'has_aside': bool(soup.find('aside')),
            'has_semantic_tags': False,
            'has_schema_markup': bool(soup.find(attrs={"itemtype": True})),
            'nesting_level': self._get_max_nesting_level(soup.body) if soup.body else 0,
            'tag_counts': self._count_tags(soup)
            }
        
        # 检查是否使用了语义化标签
        semantic_tags = ['header', 'footer', 'nav', 'main', 'article', 'section', 'aside']
        for tag in semantic_tags:
            if soup.find(tag):
                structure['has_semantic_tags'] = True
                break
        
        return structure
    
    def _get_max_nesting_level(self, element, current_level=0):
        """
        获取HTML最大嵌套深度
        
        参数:
            element (Tag): 当前HTML元素
            current_level (int): 当前嵌套级别
            
        返回:
            int: 最大嵌套深度
        """
        # 如果没有子元素，返回当前级别
        if not element or not hasattr(element, 'children'):
            return current_level
        
        # 找到子元素中最大嵌套深度
        max_level = current_level
        for child in element.children:
            if child.name:  # 只处理标签元素，忽略文本
                child_level = self._get_max_nesting_level(child, current_level + 1)
                max_level = max(max_level, child_level)
        
        return max_level
    
    def _count_tags(self, soup):
        """
        统计页面中各种标签的数量
        
        参数:
            soup (BeautifulSoup): 已解析的HTML
            
        返回:
            dict: 标签计数结果
        """
        # 初始化空字典
        tag_counts = {}
        
        # 统计所有标签
        all_tags = [tag.name for tag in soup.find_all()]
        tag_counter = Counter(all_tags)
        
        # 只保留数量大于1的标签，减少输出
        tag_counts = {tag: count for tag, count in tag_counter.items() if count > 1}
        
        return tag_counts
    
    def _identify_components(self, soup):
        """
        识别页面组件
        
        根据标签、类名和ID等信息来识别页面中的组件。
        
        参数:
            soup (BeautifulSoup): 已解析的HTML
            
        返回:
            list: 识别出的组件列表
        """
        logger.info("开始识别页面组件")
        components = []
        
        # 1. 先识别明确的组件（有明确标识的组件）
        for component_type, identifiers in self.component_identifiers.items():
            # 在标签名、ID和类名中查找组件标识符
            for identifier in identifiers:
                # 检查标签名
                for tag in soup.find_all(identifier):
                    components.append({
                        'type': component_type,
                        'html': str(tag),
                        'element': tag.name,
                        'id': tag.get('id', ''),
                        'classes': tag.get('class', []),
                        'text_length': len(tag.get_text()),
                        'identification_method': 'tag_name'
                    })
                
                # 检查ID
                for tag in soup.find_all(id=re.compile(identifier, re.I)):
                    components.append({
                        'type': component_type,
                        'html': str(tag),
                        'element': tag.name,
                        'id': tag.get('id', ''),
                        'classes': tag.get('class', []),
                        'text_length': len(tag.get_text()),
                        'identification_method': 'id'
                    })
                
                # 检查类名
                for tag in soup.find_all(class_=re.compile(identifier, re.I)):
                    components.append({
                        'type': component_type,
                        'html': str(tag),
                        'element': tag.name,
                        'id': tag.get('id', ''),
                        'classes': tag.get('class', []),
                        'text_length': len(tag.get_text()),
                        'identification_method': 'class'
                    })
        
        # 2. 根据页面结构识别可能的组件
        # 页眉识别（位于文档顶部）
        if not any(comp['type'] == 'header' for comp in components):
            potential_headers = []
            body = soup.body
            if body and body.contents:
                # 获取文档顶部的元素
                for i, element in enumerate(body.contents[:5]):
                    if hasattr(element, 'name') and element.name and i < 3:
                        text = element.get_text().strip()
                        if text and len(text) > self.min_text_length:
                            potential_headers.append(element)
            
            # 将可能的页眉添加到组件列表中
            for element in potential_headers:
                components.append({
                    'type': 'header',
                    'html': str(element),
                    'element': element.name,
                    'id': element.get('id', ''),
                    'classes': element.get('class', []),
                    'text_length': len(element.get_text()),
                    'identification_method': 'structure_position'
                })
        
        # 页脚识别（位于文档底部）
        if not any(comp['type'] == 'footer' for comp in components):
            potential_footers = []
            body = soup.body
            if body and body.contents:
                # 获取文档底部的元素
                for i, element in enumerate(reversed(body.contents[-5:])):
                    if hasattr(element, 'name') and element.name and i < 3:
                        text = element.get_text().strip()
                        if text and len(text) > self.min_text_length:
                            potential_footers.append(element)
            
            # 将可能的页脚添加到组件列表中
            for element in potential_footers:
                components.append({
                    'type': 'footer',
                    'html': str(element),
                    'element': element.name,
                    'id': element.get('id', ''),
                    'classes': element.get('class', []),
                    'text_length': len(element.get_text()),
                    'identification_method': 'structure_position'
                })
        
        # 移除重复的组件
        # 通过组件的HTML内容进行去重
        unique_components = []
        seen_html = set()
        
        for component in components:
            # 获取一个缩短版本的HTML进行比较
            short_html = component['html'][:100]
            if short_html not in seen_html:
                seen_html.add(short_html)
                unique_components.append(component)
        
        logger.info(f"识别出 {len(unique_components)} 个组件")
        return unique_components
    
    def _analyze_layout(self, soup):
        """
        分析页面整体布局
        
        检测页面的布局类型（单栏、双栏、网格等）
        并识别主要的布局容器。
        
        参数:
            soup (BeautifulSoup): 已解析的HTML
            
        返回:
            dict: 布局分析结果
        """
        layout = {
            'type': 'unknown',
            'containers': [],
            'grid_system': False,
            'flex_layout': False,
            'responsive': False,
            'column_count': 1  # 默认为单栏
        }
        
        # 检查是否使用网格系统
        grid_classes = ['row', 'grid', 'container', 'col', 'column']
        for grid_class in grid_classes:
            if soup.find(class_=re.compile(f'{grid_class}', re.I)):
                layout['grid_system'] = True
                break
        
        # 检查是否使用弹性布局
        if soup.find(style=re.compile('display\s*:\s*flex', re.I)) or soup.find(class_=re.compile('flex|d-flex', re.I)):
            layout['flex_layout'] = True
        
        # 检查是否响应式
        meta_viewport = soup.find('meta', attrs={'name': 'viewport'})
        media_queries = soup.find_all(style=re.compile('@media', re.I))
        if meta_viewport or media_queries:
            layout['responsive'] = True
        
        # 尝试确定列数
        containers = soup.find_all(['div', 'section'], class_=re.compile('container|wrapper|row', re.I))
        if containers:
            # 分析第一个容器下的直接子元素数量来估计列数
            first_container = containers[0]
            children = [child for child in first_container.children if hasattr(child, 'name') and child.name]
            if len(children) > 1:
                # 简单计算列数：如果子元素都有类似col的类名，按子元素数计算
                col_children = [child for child in children if hasattr(child, 'get') and child.get('class') and any('col' in cls.lower() for cls in child.get('class'))]
                if col_children:
                    layout['column_count'] = len(col_children)
                else:
                    layout['column_count'] = min(len(children), 4)  # 限制最大列数为4
        
        # 确定布局类型
        if layout['column_count'] == 1:
            layout['type'] = 'single_column'
        elif layout['column_count'] == 2:
            layout['type'] = 'two_column'
        elif layout['column_count'] == 3:
            layout['type'] = 'three_column'
        elif layout['column_count'] >= 4:
            layout['type'] = 'grid'
        
        # 如果检测到弹性盒子或网格系统，优先考虑这些
        if layout['flex_layout']:
            layout['type'] += '_flex'
        elif layout['grid_system']:
            layout['type'] += '_grid'
        
        # 记录主要容器
        layout['containers'] = [
            {
                'element': container.name,
                'id': container.get('id', ''),
                'classes': container.get('class', []),
                'children_count': len([child for child in container.children if hasattr(child, 'name') and child.name])
            }
            for container in containers[:5]  # 只保留前5个容器
        ]
        
        return layout 