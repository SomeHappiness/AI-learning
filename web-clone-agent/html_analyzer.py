#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
HTML分析器模块
负责分析HTML结构并将其转换为Vue组件结构
"""

import os
import re
import logging
from bs4 import BeautifulSoup
import html5lib
from collections import defaultdict

logger = logging.getLogger(__name__)

class HtmlAnalyzer:
    """HTML分析器，用于分析HTML结构并生成Vue组件"""
    
    def __init__(self, component_threshold=3):
        """
        初始化HTML分析器
        
        Args:
            component_threshold (int): 相似元素识别为组件的阈值
        """
        self.component_threshold = component_threshold
    
    def analyze(self, html_content):
        """
        分析HTML内容并生成组件结构
        
        Args:
            html_content (str): HTML内容
        
        Returns:
            dict: 页面结构和组件信息
        """
        logger.info("开始分析HTML结构...")
        
        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(html_content, 'html5lib')
        
        # 识别页面主要布局
        layout = self._identify_layout(soup)
        
        # 识别潜在组件
        components = self._identify_components(soup)
        
        # 识别交互元素
        interactive_elements = self._identify_interactive_elements(soup)
        
        result = {
            'layout': layout,
            'components': components,
            'interactive_elements': interactive_elements,
            'meta': self._extract_meta_information(soup)
        }
        
        logger.info(f"HTML分析完成，识别到 {len(components)} 个潜在组件")
        return result
    
    def _identify_layout(self, soup):
        """识别页面的主要布局结构"""
        layout = {
            'type': 'unknown',
            'header': None,
            'footer': None,
            'sidebar': None,
            'main_content': None,
            'sections': []
        }
        
        # 尝试识别头部
        header_candidates = soup.find_all(['header', 'div', 'nav'], 
                                         class_=re.compile(r'header|navbar|nav-bar|top-bar', re.I))
        if header_candidates:
            layout['header'] = {
                'element': str(header_candidates[0]),
                'classes': header_candidates[0].get('class', []),
                'id': header_candidates[0].get('id', '')
            }
        
        # 尝试识别底部
        footer_candidates = soup.find_all(['footer', 'div'], 
                                         class_=re.compile(r'footer|bottom', re.I))
        if footer_candidates:
            layout['footer'] = {
                'element': str(footer_candidates[0]),
                'classes': footer_candidates[0].get('class', []),
                'id': footer_candidates[0].get('id', '')
            }
        
        # 尝试识别侧边栏
        sidebar_candidates = soup.find_all(['aside', 'div', 'nav'], 
                                          class_=re.compile(r'sidebar|side-bar|left-menu|right-menu', re.I))
        if sidebar_candidates:
            layout['sidebar'] = {
                'element': str(sidebar_candidates[0]),
                'classes': sidebar_candidates[0].get('class', []),
                'id': sidebar_candidates[0].get('id', ''),
                'position': 'left' if 'left' in str(sidebar_candidates[0]).lower() else 'right'
            }
        
        # 尝试识别主内容区域
        main_content_candidates = soup.find_all(['main', 'div', 'article'], 
                                               class_=re.compile(r'main|content|article|container', re.I))
        if main_content_candidates:
            layout['main_content'] = {
                'element': str(main_content_candidates[0]),
                'classes': main_content_candidates[0].get('class', []),
                'id': main_content_candidates[0].get('id', '')
            }
        
        # 识别页面的主要部分
        sections = soup.find_all(['section', 'div', 'article'], 
                                class_=re.compile(r'section|container|row|block', re.I))
        for section in sections[:10]:  # 限制最多10个section以防止过多
            layout['sections'].append({
                'element': str(section)[:200] + ('...' if len(str(section)) > 200 else ''),
                'classes': section.get('class', []),
                'id': section.get('id', '')
            })
        
        # 确定布局类型
        if layout['sidebar']:
            layout['type'] = 'sidebar-layout'
        elif len(layout['sections']) > 3:
            layout['type'] = 'multi-section-layout'
        elif layout['header'] and layout['main_content'] and layout['footer']:
            layout['type'] = 'standard-layout'
        else:
            layout['type'] = 'custom-layout'
        
        return layout
    
    def _identify_components(self, soup):
        """识别潜在的可复用组件"""
        components = []
        
        # 识别可能的卡片组件
        card_candidates = soup.find_all(['div', 'article', 'section'], 
                                       class_=re.compile(r'card|box|item|product|post', re.I))
        
        # 按结构对卡片分组
        card_groups = defaultdict(list)
        
        for card in card_candidates:
            # 简化的结构特征
            structure = self._get_structure_signature(card)
            card_groups[structure].append(card)
        
        # 提取组件
        for structure, cards in card_groups.items():
            if len(cards) >= self.component_threshold:
                components.append({
                    'type': 'card',
                    'count': len(cards),
                    'sample': str(cards[0])[:300] + ('...' if len(str(cards[0])) > 300 else ''),
                    'classes': cards[0].get('class', []),
                    'structure': structure
                })
        
        # 识别导航组件
        nav_candidates = soup.find_all(['nav', 'ul'], 
                                      class_=re.compile(r'nav|menu|navigation', re.I))
        
        for nav in nav_candidates:
            components.append({
                'type': 'navigation',
                'sample': str(nav)[:300] + ('...' if len(str(nav)) > 300 else ''),
                'items': len(nav.find_all('li')),
                'classes': nav.get('class', [])
            })
        
        # 识别表单组件
        forms = soup.find_all('form')
        for form in forms:
            components.append({
                'type': 'form',
                'sample': str(form)[:300] + ('...' if len(str(form)) > 300 else ''),
                'fields': len(form.find_all(['input', 'select', 'textarea'])),
                'classes': form.get('class', []),
                'id': form.get('id', '')
            })
        
        # 识别表格组件
        tables = soup.find_all('table')
        for table in tables:
            components.append({
                'type': 'table',
                'sample': str(table)[:300] + ('...' if len(str(table)) > 300 else ''),
                'rows': len(table.find_all('tr')),
                'columns': len(table.find_all('th')) or len(table.find_all('tr')[0].find_all('td')) if table.find_all('tr') else 0,
                'classes': table.get('class', [])
            })
        
        return components
    
    def _identify_interactive_elements(self, soup):
        """识别交互元素，如按钮、表单、链接等"""
        interactive = {
            'buttons': [],
            'forms': [],
            'inputs': [],
            'links': [],
            'dropdowns': []
        }
        
        # 按钮
        buttons = soup.find_all(['button', 'a', 'input'], 
                               class_=re.compile(r'btn|button', re.I))
        for button in buttons[:20]:  # 限制数量
            interactive['buttons'].append({
                'text': button.get_text(strip=True),
                'classes': button.get('class', []),
                'id': button.get('id', ''),
                'type': button.name,
                'events': self._extract_event_handlers(button)
            })
        
        # 表单输入
        inputs = soup.find_all(['input', 'select', 'textarea'])
        for input_el in inputs[:20]:
            interactive['inputs'].append({
                'type': input_el.name,
                'input_type': input_el.get('type', ''),
                'name': input_el.get('name', ''),
                'id': input_el.get('id', ''),
                'placeholder': input_el.get('placeholder', ''),
                'classes': input_el.get('class', [])
            })
        
        # 下拉菜单
        dropdowns = soup.find_all(['select', 'div'], 
                                 class_=re.compile(r'dropdown|select|menu', re.I))
        for dropdown in dropdowns[:10]:
            interactive['dropdowns'].append({
                'type': dropdown.name,
                'id': dropdown.get('id', ''),
                'classes': dropdown.get('class', []),
                'options': len(dropdown.find_all('option')) if dropdown.name == 'select' else 0
            })
        
        return interactive
    
    def _extract_meta_information(self, soup):
        """提取页面的元信息"""
        meta = {
            'title': soup.title.string if soup.title else '',
            'meta_tags': {},
            'favicon': '',
            'scripts': [],
            'styles': []
        }
        
        # 提取meta标签
        for tag in soup.find_all('meta'):
            name = tag.get('name', tag.get('property', ''))
            if name:
                meta['meta_tags'][name] = tag.get('content', '')
        
        # 提取favicon
        favicon = soup.find('link', rel=re.compile(r'icon', re.I))
        if favicon:
            meta['favicon'] = favicon.get('href', '')
        
        # 提取外部脚本和样式
        for script in soup.find_all('script', src=True):
            meta['scripts'].append(script.get('src', ''))
        
        for style in soup.find_all('link', rel='stylesheet'):
            meta['styles'].append(style.get('href', ''))
        
        return meta
    
    def _get_structure_signature(self, element):
        """
        获取元素的结构特征签名
        用于识别相似结构
        """
        # 简化的结构签名方法，仅标记子元素的类型和数量
        children = element.find_all(True, recursive=False)
        signature = []
        
        for child in children:
            child_info = f"{child.name}:{len(child.find_all(True))}"
            signature.append(child_info)
        
        return ">".join(signature)
    
    def _extract_event_handlers(self, element):
        """提取元素上的事件处理程序"""
        events = []
        
        # 常见的JavaScript事件属性
        event_attrs = ['onclick', 'onchange', 'onsubmit', 'onmouseover', 
                      'onmouseout', 'onkeydown', 'onkeyup', 'onload']
        
        for attr in event_attrs:
            if element.has_attr(attr):
                events.append({
                    'type': attr[2:],  # 去掉"on"前缀
                    'handler': element[attr]
                })
        
        return events 