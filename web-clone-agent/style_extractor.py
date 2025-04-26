#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
样式提取器模块
负责提取CSS样式并转换为Vue组件样式
"""

import os
import re
import logging
import cssutils
import json
from collections import defaultdict
from urllib.parse import urljoin
from bs4 import BeautifulSoup

# 抑制cssutils的解析错误日志
cssutils.log.setLevel(logging.CRITICAL)
logger = logging.getLogger(__name__)

class StyleExtractor:
    """CSS样式提取器，用于分析和转换CSS"""
    
    def __init__(self, output_dir="output"):
        """
        初始化样式提取器
        
        Args:
            output_dir (str): 输出目录
        """
        self.output_dir = output_dir
        
        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(os.path.join(output_dir, 'styles'), exist_ok=True)
    
    def extract_styles(self, css_files, css_content, html_content, base_url=''):
        """
        提取和处理CSS样式
        
        Args:
            css_files (list): CSS文件列表
            css_content (dict): CSS文件内容字典
            html_content (str): HTML内容，用于分析使用的选择器
            base_url (str): 基础URL，用于解析相对路径
        
        Returns:
            dict: 处理后的样式信息
        """
        logger.info(f"开始提取样式，共有 {len(css_files)} 个CSS文件")
        
        # 解析HTML以便分析使用的类和ID
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 收集页面上使用的类和ID
        used_classes = set()
        used_ids = set()
        
        for tag in soup.find_all(True):
            if tag.has_attr('class'):
                used_classes.update(tag.get('class'))
            if tag.has_attr('id'):
                used_ids.add(tag.get('id'))
        
        logger.info(f"页面使用了 {len(used_classes)} 个类和 {len(used_ids)} 个ID")
        
        # 处理所有CSS文件
        all_rules = []
        component_styles = defaultdict(list)
        layout_styles = []
        common_styles = []
        
        for css_file in css_files:
            if css_file in css_content:
                css_text = css_content[css_file]
                
                try:
                    # 解析CSS
                    sheet = cssutils.parseString(css_text)
                    
                    # 遍历规则
                    for rule in sheet:
                        if rule.type == rule.STYLE_RULE:
                            # 检查选择器是否为组件
                            is_component = False
                            rule_str = rule.cssText.decode('utf-8') if hasattr(rule.cssText, 'decode') else rule.cssText
                            
                            # 处理布局相关样式
                            if re.search(r'(layout|container|grid|row|col|flex|section|header|footer|sidebar)', 
                                         rule.selectorText, re.I):
                                layout_styles.append(rule_str)
                            
                            # 处理组件样式
                            elif re.search(r'(card|button|form|nav|menu|table|item|panel|box|modal)', 
                                         rule.selectorText, re.I):
                                component_name = re.search(r'(card|button|form|nav|menu|table|item|panel|box|modal)', 
                                                         rule.selectorText, re.I).group(1).lower()
                                component_styles[component_name].append(rule_str)
                                is_component = True
                            
                            # 处理一般样式
                            if not is_component:
                                # 检查此选择器是否在页面中使用
                                selector_used = False
                                for selector in rule.selectorText.split(','):
                                    selector = selector.strip()
                                    # 检查类选择器
                                    class_match = re.search(r'\.([a-zA-Z0-9_-]+)', selector)
                                    if class_match and class_match.group(1) in used_classes:
                                        selector_used = True
                                        break
                                    
                                    # 检查ID选择器
                                    id_match = re.search(r'#([a-zA-Z0-9_-]+)', selector)
                                    if id_match and id_match.group(1) in used_ids:
                                        selector_used = True
                                        break
                                
                                if selector_used:
                                    common_styles.append(rule_str)
                            
                            all_rules.append(rule_str)
                        
                        elif rule.type == rule.IMPORT_RULE:
                            # 处理@import规则
                            import_url = rule.href
                            if import_url:
                                full_url = urljoin(base_url, import_url)
                                logger.info(f"检测到@import: {full_url}")
                                # 这里可以添加代码来下载和处理导入的CSS
                
                except Exception as e:
                    logger.error(f"解析CSS文件 {css_file} 时出错: {str(e)}")
        
        # 生成组件样式文件
        for component_name, styles in component_styles.items():
            output_file = os.path.join(self.output_dir, 'styles', f'{component_name}.scss')
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"// {component_name} 组件样式\n")
                f.write(".v-" + component_name + " {\n")
                for style in styles:
                    # 简化选择器，只保留组件的样式属性
                    style = re.sub(r'.*{', '', style)
                    style = re.sub(r'}', '', style)
                    f.write(f"  {style.strip()}\n")
                f.write("}\n")
        
        # 生成布局样式文件
        layout_file = os.path.join(self.output_dir, 'styles', 'layout.scss')
        with open(layout_file, 'w', encoding='utf-8') as f:
            f.write("// 布局样式\n")
            for style in layout_styles:
                f.write(f"{style}\n")
        
        # 生成通用样式文件
        common_file = os.path.join(self.output_dir, 'styles', 'common.scss')
        with open(common_file, 'w', encoding='utf-8') as f:
            f.write("// 通用样式\n")
            for style in common_styles:
                f.write(f"{style}\n")
        
        # 生成主样式文件
        main_file = os.path.join(self.output_dir, 'styles', 'main.scss')
        with open(main_file, 'w', encoding='utf-8') as f:
            f.write("// 主样式文件\n")
            f.write("@import './layout.scss';\n")
            f.write("@import './common.scss';\n")
            for component_name in component_styles.keys():
                f.write(f"@import './{component_name}.scss';\n")
        
        return {
            'component_styles': dict(component_styles),
            'layout_styles': layout_styles,
            'common_styles': common_styles,
            'total_rules': len(all_rules)
        }
    
    def extract_color_palette(self, css_content):
        """
        从CSS中提取颜色调色板
        
        Args:
            css_content (dict): CSS文件内容字典
        
        Returns:
            dict: 颜色信息
        """
        colors = set()
        font_families = set()
        
        # 颜色正则表达式模式
        color_patterns = [
            r'#[0-9a-fA-F]{3,8}',  # HEX颜色
            r'rgba?\([^)]+\)',     # RGB/RGBA颜色
            r'hsla?\([^)]+\)'      # HSL/HSLA颜色
        ]
        
        # 遍历所有CSS内容
        for css_file, content in css_content.items():
            # 提取颜色
            for pattern in color_patterns:
                matches = re.findall(pattern, content)
                colors.update(matches)
            
            # 提取字体
            font_matches = re.findall(r'font-family\s*:\s*([^;]+)', content)
            for font in font_matches:
                font_families.update([f.strip().strip('"\'') for f in font.split(',')])
        
        # 生成颜色变量
        color_vars = {}
        for i, color in enumerate(colors):
            if re.match(r'^#[0-9a-fA-F]{3,8}$', color):
                var_name = f"$color-{i+1}"
                color_vars[var_name] = color
        
        # 生成字体变量
        font_vars = {}
        for i, font in enumerate(font_families):
            if font.lower() not in ['inherit', 'initial', 'sans-serif', 'serif', 'monospace']:
                var_name = f"$font-{font.lower().replace(' ', '-')}"
                font_vars[var_name] = font
        
        # 生成变量文件
        variables_file = os.path.join(self.output_dir, 'styles', 'variables.scss')
        with open(variables_file, 'w', encoding='utf-8') as f:
            f.write("// 颜色变量\n")
            for var_name, color in color_vars.items():
                f.write(f"{var_name}: {color};\n")
            
            f.write("\n// 字体变量\n")
            for var_name, font in font_vars.items():
                f.write(f"{var_name}: '{font}';\n")
        
        return {
            'colors': list(colors),
            'color_vars': color_vars,
            'font_families': list(font_families),
            'font_vars': font_vars
        }
    
    def convert_to_vue_style(self, html_analysis, style_analysis):
        """
        将分析结果转换为Vue组件样式
        
        Args:
            html_analysis (dict): HTML分析结果
            style_analysis (dict): 样式分析结果
        
        Returns:
            dict: Vue样式信息
        """
        result = {
            'component_styles': {},
            'scoped_styles': {},
            'global_styles': {}
        }
        
        # 处理组件样式
        for component in html_analysis.get('components', []):
            component_type = component.get('type', '')
            
            if component_type in style_analysis.get('component_styles', {}):
                component_selector = f".v-{component_type}"
                result['component_styles'][component_type] = {
                    'selector': component_selector,
                    'styles': style_analysis['component_styles'][component_type]
                }
        
        # 处理全局样式
        result['global_styles'] = {
            'layout': style_analysis.get('layout_styles', []),
            'common': style_analysis.get('common_styles', [])
        }
        
        return result 