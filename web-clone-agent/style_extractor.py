#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
样式提取器模块 (style_extractor.py)
-----------------------------
该模块负责提取和分析网页的CSS样式，为Vue组件生成做准备。

主要功能:
1. 提取和解析CSS样式规则
2. 分析网页使用的颜色方案
3. 识别字体和排版样式
4. 提取常用组件样式（按钮、表单等）
5. 生成Vue组件可用的样式文件

工作原理:
使用tinycss2、cssutils等工具解析CSS，分析样式规则，
提取关键的样式信息，用于后续Vue组件的样式生成。
"""

import os
import re
import logging
import colorsys
from urllib.parse import urljoin
from collections import Counter, defaultdict

# 尝试导入CSS解析库，使用能够成功导入的一个
try:
    import tinycss2
    USE_TINYCSS2 = True
except ImportError:
    USE_TINYCSS2 = False
    try:
        import cssutils
        USE_CSSUTILS = True
    except ImportError:
        USE_CSSUTILS = False

# 配置日志
logger = logging.getLogger(__name__)

class StyleExtractor:
    """
    样式提取器类
    
    负责从CSS文件和HTML内容中提取样式信息，
    分析配色方案、字体和常用组件样式。
    """
    
    def __init__(self):
        """
        初始化样式提取器
        
        设置默认值和常用样式识别规则。
        """
        # 常用组件的CSS选择器模式
        self.component_patterns = {
            'button': [r'\.btn', r'\.button', r'button', r'\.cta'],
            'form': [r'form', r'\.form', r'input', r'\.input-group'],
            'card': [r'\.card', r'\.box', r'\.panel', r'\.tile'],
            'navbar': [r'\.navbar', r'\.nav', r'nav', r'\.navigation', r'\.menu'],
            'footer': [r'footer', r'\.footer', r'\.bottom'],
            'header': [r'header', r'\.header', r'\.top', r'\.banner'],
        }
        
        # 颜色识别的正则表达式
        self.color_regex = {
            'hex': re.compile(r'#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})'),
            'rgb': re.compile(r'rgb\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)'),
            'rgba': re.compile(r'rgba\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*([0-9]*\.?[0-9]+)\s*\)'),
            'hsl': re.compile(r'hsl\(\s*(\d+)\s*,\s*(\d+%)\s*,\s*(\d+%)\s*\)'),
            'hsla': re.compile(r'hsla\(\s*(\d+)\s*,\s*(\d+%)\s*,\s*(\d+%)\s*,\s*([0-9]*\.?[0-9]+)\s*\)')
        }
        
        # 字体识别的正则表达式
        self.font_regex = re.compile(r'font-family\s*:\s*([^;}]+)')
        
        # 存储提取的样式
        self.extracted_styles = {
            'colors': {},
            'fonts': [],
            'component_styles': {},
            'global_styles': {}
        }
    
    def extract_styles(self, css_files, css_content, html_content, base_url):
        """
        提取和处理CSS样式
        
        这是主要的公共方法，协调整个样式提取和分析过程。
        
        参数:
            css_files (list): CSS文件名列表
            css_content (dict): CSS内容字典
            html_content (str): HTML内容
            base_url (str): 基础URL
            
        返回:
            dict: 包含提取样式的字典
        """
        logger.info("开始提取和分析CSS样式")
        
        # 重置提取的样式
        self.extracted_styles = {
            'colors': {},
            'fonts': [],
            'component_styles': {},
            'global_styles': {},
            'file_stats': {}
        }
        
        # 处理所有CSS文件
        total_css = ""
        for css_file in css_files:
            if css_file in css_content:
                logger.info(f"分析CSS文件: {css_file}")
                css_text = css_content[css_file]
                total_css += css_text
                
                # 处理相对URL（如背景图片）
                css_text = self._fix_relative_urls(css_text, base_url)
                
                # 提取和分析样式
                self._extract_styles_from_css(css_text, css_file)
                
                # 收集文件统计信息
                self.extracted_styles['file_stats'][css_file] = {
                    'size': len(css_text),
                    'rules': len(re.findall(r'[^}]+{[^}]+}', css_text)),
                    'selectors': len(re.findall(r'[^{]+{', css_text))
                }
        
        # 提取颜色方案
        color_scheme = self.extract_color_palette(css_content)
        self.extracted_styles['colors'] = color_scheme
        
        # 提取并合并内联样式
        inline_styles = self._extract_inline_styles(html_content)
        for selector, properties in inline_styles.items():
            if selector in self.extracted_styles['global_styles']:
                self.extracted_styles['global_styles'][selector].update(properties)
            else:
                self.extracted_styles['global_styles'][selector] = properties
        
        logger.info("CSS样式分析完成")
        return self.extracted_styles
    
    def _extract_styles_from_css(self, css_text, source_file):
        """
        从CSS文本中提取样式规则
        
        使用可用的CSS解析库分析CSS文本，提取样式规则。
        
        参数:
            css_text (str): CSS文本内容
            source_file (str): 源CSS文件名（用于日志）
        """
        try:
            if USE_TINYCSS2:
                # 使用tinycss2解析
                self._extract_with_tinycss2(css_text, source_file)
            elif USE_CSSUTILS:
                # 使用cssutils解析
                self._extract_with_cssutils(css_text, source_file)
            else:
                # 使用正则表达式进行基本解析
                self._extract_with_regex(css_text, source_file)
                
        except Exception as e:
            logger.error(f"解析CSS文件 {source_file} 时出错: {str(e)}")
    
    def _extract_with_tinycss2(self, css_text, source_file):
        """
        使用tinycss2库解析CSS
        
        参数:
            css_text (str): CSS文本内容
            source_file (str): 源文件名
        """
        # 解析CSS
        rules = tinycss2.parse_stylesheet(css_text)
        
        for rule in rules:
            # 只处理样式规则，忽略注释和@规则
            if rule.type == 'qualified-rule':
                try:
                    # 获取选择器文本
                    selector_text = ''.join(token.serialize() for token in rule.prelude).strip()
                    
                    # 获取声明块
                    declarations = {}
                    for decl in tinycss2.parse_declaration_list(rule.content):
                        if decl.type == 'declaration':
                            name = decl.name
                            value = ''.join(token.serialize() for token in decl.value).strip()
                            declarations[name] = value
                    
                    # 分类样式规则
                    self._categorize_style_rule(selector_text, declarations, source_file)
                    
                except Exception as e:
                    logger.warning(f"处理tinycss2规则时出错: {str(e)}")
    
    def _extract_with_cssutils(self, css_text, source_file):
        """
        使用cssutils库解析CSS
        
        参数:
            css_text (str): CSS文本内容
            source_file (str): 源文件名
        """
        # 解析CSS
        sheet = cssutils.parseString(css_text)
        
        for rule in sheet:
            # 只处理样式规则
            if rule.type == rule.STYLE_RULE:
                try:
                    # 获取选择器和样式
                    selector_text = rule.selectorText
                    declarations = {prop.name: prop.value for prop in rule.style}
                    
                    # 分类样式规则
                    self._categorize_style_rule(selector_text, declarations, source_file)
                    
                except Exception as e:
                    logger.warning(f"处理cssutils规则时出错: {str(e)}")
    
    def _extract_with_regex(self, css_text, source_file):
        """
        使用正则表达式解析CSS（当没有专门的CSS解析库时）
        
        参数:
            css_text (str): CSS文本内容
            source_file (str): 源文件名
        """
        # 使用正则表达式匹配CSS规则
        rule_pattern = re.compile(r'([^{]+){([^}]+)}')
        
        for match in rule_pattern.finditer(css_text):
            try:
                # 获取选择器和样式声明
                selector_text = match.group(1).strip()
                declarations_text = match.group(2).strip()
                
                # 解析样式声明
                declarations = {}
                for decl in declarations_text.split(';'):
                    if ':' in decl:
                        prop, value = decl.split(':', 1)
                        declarations[prop.strip()] = value.strip()
                
                # 分类样式规则
                self._categorize_style_rule(selector_text, declarations, source_file)
                
            except Exception as e:
                logger.warning(f"使用正则表达式解析CSS规则时出错: {str(e)}")
    
    def _categorize_style_rule(self, selector, declarations, source_file):
        """
        对样式规则进行分类
        
        根据选择器将样式规则分为组件样式和全局样式。
        
        参数:
            selector (str): CSS选择器
            declarations (dict): CSS属性和值
            source_file (str): 源CSS文件
        """
        # 为组件样式分类
        for component, patterns in self.component_patterns.items():
            for pattern in patterns:
                if re.search(pattern, selector):
                    if component not in self.extracted_styles['component_styles']:
                        self.extracted_styles['component_styles'][component] = {}
                    
                    if selector not in self.extracted_styles['component_styles'][component]:
                        self.extracted_styles['component_styles'][component][selector] = {}
                    
                    self.extracted_styles['component_styles'][component][selector].update(declarations)
                    return  # 一旦归类为组件样式就返回
        
        # 不匹配任何组件模式，视为全局样式
        if selector not in self.extracted_styles['global_styles']:
            self.extracted_styles['global_styles'][selector] = {}
        
        self.extracted_styles['global_styles'][selector].update(declarations)
    
    def _extract_inline_styles(self, html_content):
        """
        从HTML中提取内联样式
        
        参数:
            html_content (str): HTML内容
            
        返回:
            dict: 内联样式字典
        """
        inline_styles = {}
        
        # 匹配带有style属性的标签
        style_pattern = re.compile(r'<([a-z0-9]+)[^>]*?style\s*=\s*["\']([^"\']+)["\'][^>]*?>', re.I)
        
        for match in style_pattern.finditer(html_content):
            tag = match.group(1)
            style_text = match.group(2)
            
            # 使用标签作为选择器
            selector = tag
            
            # 解析样式属性
            declarations = {}
            for decl in style_text.split(';'):
                if ':' in decl:
                    prop, value = decl.split(':', 1)
                    declarations[prop.strip()] = value.strip()
            
            if selector not in inline_styles:
                inline_styles[selector] = {}
            
            inline_styles[selector].update(declarations)
        
        return inline_styles
    
    def extract_color_palette(self, css_content):
        """
        提取网页使用的颜色方案
        
        参数:
            css_content (dict): CSS内容字典
            
        返回:
            dict: 颜色方案信息，包括主要颜色、次要颜色等
        """
        logger.info("开始提取颜色方案")
        
        # 合并所有CSS内容
        all_css = " ".join(css_content.values())
        
        # 提取所有颜色值
        all_colors = []
        
        # 提取十六进制颜色
        hex_colors = self.color_regex['hex'].findall(all_css)
        all_colors.extend(['#' + color for color in hex_colors])
        
        # 提取RGB颜色
        rgb_colors = self.color_regex['rgb'].findall(all_css)
        all_colors.extend([f"rgb({r},{g},{b})" for r, g, b in rgb_colors])
        
        # 提取RGBA颜色
        rgba_colors = self.color_regex['rgba'].findall(all_css)
        all_colors.extend([f"rgba({r},{g},{b},{a})" for r, g, b, a in rgba_colors])
        
        # 统计颜色出现频率
        color_counter = Counter(all_colors)
        
        # 如果颜色太少，尝试将类似颜色归类
        if len(color_counter) < 5:
            color_counter = self._group_similar_colors(all_colors)
        
        # 提取字体
        fonts = self.font_regex.findall(all_css)
        font_counter = Counter([font.strip().split(',')[0].strip('"\'') for font in fonts])
        
        # 构建颜色方案
        color_scheme = {
            'primary_colors': [],
            'secondary_colors': [],
            'neutral_colors': [],
            'accent_colors': [],
            'all_colors': dict(color_counter),
            'primary_font': font_counter.most_common(1)[0][0] if font_counter else 'sans-serif',
            'secondary_fonts': [font for font, _ in font_counter.most_common()[1:3]] if len(font_counter) > 1 else []
        }
        
        # 提取最常用的颜色作为主要颜色
        most_common = color_counter.most_common(10)
        
        # 分类颜色
        for color, count in most_common:
            color_info = {
                'value': color,
                'count': count,
                'brightness': self._get_color_brightness(color)
            }
            
            # 根据出现频率和亮度分类颜色
            if len(color_scheme['primary_colors']) < 2:
                color_scheme['primary_colors'].append(color_info)
            elif len(color_scheme['secondary_colors']) < 3:
                color_scheme['secondary_colors'].append(color_info)
            elif self._is_neutral_color(color):
                color_scheme['neutral_colors'].append(color_info)
            else:
                color_scheme['accent_colors'].append(color_info)
        
        logger.info(f"提取到 {len(color_counter)} 种颜色，{len(font_counter)} 种字体")
        return color_scheme
    
    def _fix_relative_urls(self, css_text, base_url):
        """
        修复CSS中的相对URL
        
        将CSS中的相对URL转换为绝对URL。
        
        参数:
            css_text (str): CSS文本内容
            base_url (str): 基础URL
            
        返回:
            str: 修复后的CSS文本
        """
        # 匹配url()函数
        url_pattern = re.compile(r'url\(["\']?([^)]+?)["\']?\)')
        
        # 查找并替换所有相对URL
        def replace_url(match):
            url = match.group(1)
            
            # 跳过数据URI和绝对URL
            if url.startswith('data:') or url.startswith('http://') or url.startswith('https://'):
                return f'url({url})'
            
            # 转换相对URL为绝对URL
            absolute_url = urljoin(base_url, url)
            return f'url({absolute_url})'
        
        # 替换CSS中的所有URL
        fixed_css = url_pattern.sub(replace_url, css_text)
        return fixed_css
    
    def _group_similar_colors(self, colors):
        """
        将相似的颜色归为一组
        
        参数:
            colors (list): 颜色列表
            
        返回:
            Counter: 颜色计数器
        """
        # 颜色分组
        color_groups = defaultdict(list)
        
        for color in colors:
            # 尝试将颜色转换为RGB
            rgb = self._parse_color_to_rgb(color)
            
            if rgb:
                # 简化RGB值，归类相似颜色
                simplified = (rgb[0] // 20, rgb[1] // 20, rgb[2] // 20)
                color_groups[simplified].append(color)
        
        # 为每个组选择代表颜色
        grouped_colors = []
        for group in color_groups.values():
            group_counter = Counter(group)
            grouped_colors.extend(group_counter.most_common())
        
        return Counter(dict(grouped_colors))
    
    def _parse_color_to_rgb(self, color):
        """
        将颜色值解析为RGB格式
        
        参数:
            color (str): 颜色值
            
        返回:
            tuple: RGB值(r,g,b)或None
        """
        # 解析十六进制颜色
        hex_match = re.match(r'^#?([0-9a-f]{3}|[0-9a-f]{6})$', color, re.I)
        if hex_match:
            hex_color = hex_match.group(1)
            if len(hex_color) == 3:
                r = int(hex_color[0] + hex_color[0], 16)
                g = int(hex_color[1] + hex_color[1], 16)
                b = int(hex_color[2] + hex_color[2], 16)
            else:
                r = int(hex_color[0:2], 16)
                g = int(hex_color[2:4], 16)
                b = int(hex_color[4:6], 16)
            return (r, g, b)
        
        # 解析RGB颜色
        rgb_match = re.match(r'rgb\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)', color)
        if rgb_match:
            r = int(rgb_match.group(1))
            g = int(rgb_match.group(2))
            b = int(rgb_match.group(3))
            return (r, g, b)
        
        # 解析RGBA颜色
        rgba_match = re.match(r'rgba\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*[0-9.]+\s*\)', color)
        if rgba_match:
            r = int(rgba_match.group(1))
            g = int(rgba_match.group(2))
            b = int(rgba_match.group(3))
            return (r, g, b)
        
        return None
    
    def _get_color_brightness(self, color):
        """
        计算颜色的亮度
        
        参数:
            color (str): 颜色值
            
        返回:
            float: 亮度值(0-1)
        """
        rgb = self._parse_color_to_rgb(color)
        
        if not rgb:
            return 0.5  # 默认中等亮度
        
        # 计算亮度 (0-1)
        r, g, b = rgb
        return (0.299 * r + 0.587 * g + 0.114 * b) / 255
    
    def _is_neutral_color(self, color):
        """
        判断是否为中性颜色（黑、白、灰）
        
        参数:
            color (str): 颜色值
            
        返回:
            bool: 是否为中性颜色
        """
        rgb = self._parse_color_to_rgb(color)
        
        if not rgb:
            return False
            
        r, g, b = rgb
        
        # 判断是否接近黑白灰
        max_diff = max(abs(r - g), abs(r - b), abs(g - b))
        
        # 如果RGB各分量相差不大，认为是中性颜色
        return max_diff < 30 