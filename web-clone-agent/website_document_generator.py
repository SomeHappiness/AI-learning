#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
网页文档生成器模块 (website_document_generator.py)
-----------------------------------------
本模块负责根据HTML和CSS分析结果生成详细的网页设计文档，替代直接生成Vue代码。

主要功能:
1. 生成网页的整体结构文档
2. 描述页面组件和布局
3. 记录样式信息与配色方案
4. 创建网页元数据说明
5. 输出完整的网页设计说明文档

工作原理:
该模块将HTML分析器提取的信息以及样式提取器的数据，转换为结构化的设计文档，
可以作为网页重建或进一步开发的参考资料。
"""

import os
import json
import logging
from datetime import datetime
import markdown
import yaml

# 配置日志
logger = logging.getLogger(__name__)

class WebsiteDocumentGenerator:
    """
    网页文档生成器类
    
    负责生成网页的设计文档，详细记录网页的结构、组件、样式等信息。
    """
    
    def __init__(self, output_dir="website-document"):
        """
        初始化网页文档生成器
        
        参数:
            output_dir (str): 输出文档的目录
        """
        self.output_dir = output_dir
        
        # 创建文档输出目录
        os.makedirs(output_dir, exist_ok=True)
        
    def _generate_metadata_document(self, html_analysis):
        """
        生成元数据文档
        
        参数:
            html_analysis (dict): HTML分析结果
        """
        logger.info("生成元数据文档...")
        
        file_path = os.path.join(self.output_dir, "1_metadata.md")
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("# 网页元数据文档\n\n")
            
            # 页面标题
            f.write("## 页面标题\n\n")
            f.write(f"- **标题**: {html_analysis.get('title', '未命名网页')}\n\n")
            
            # 页面描述
            f.write("## 页面描述\n\n")
            f.write(f"- **描述**: {html_analysis.get('description', '无描述')}\n\n")
            
            # 关键词
            f.write("## 关键词\n\n")
            if 'keywords' in html_analysis:
                f.write("| 关键词 |\n")
                f.write("|-------|\n")
                
                for keyword in html_analysis['keywords']:
                    f.write(f"| `{keyword}` |\n")
            else:
                f.write("未能提取关键词\n\n")
            
            # 页面元数据
            f.write("\n## 页面元数据\n\n")
            if 'meta' in html_analysis:
                f.write("| 元数据键 | 值 |\n")
                f.write("|----------|--|\n")
                
                for key, value in html_analysis['meta'].items():
                    f.write(f"| `{key}` | `{value}` |\n")
            else:
                f.write("未能提取页面元数据\n\n")
    
    def _generate_structure_document(self, html_analysis):
        """
        生成结构文档
        
        参数:
            html_analysis (dict): HTML分析结果
        """
        logger.info("生成结构文档...")
        
        file_path = os.path.join(self.output_dir, "2_structure.md")
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("# 网页结构文档\n\n")
            
            # 页面语义化标签分析
            f.write("## 页面语义化标签分析\n\n")
            if 'semantic_tags' in html_analysis:
                semantic_tags = html_analysis['semantic_tags']
                
                if semantic_tags:
                    f.write("页面中使用的语义化HTML标签:\n\n")
                    f.write("| 标签 | 可能用途 |\n")
                    f.write("|------|--------|\n")
                    
                    for tag in semantic_tags:
                        f.write(f"| `{tag}` | 未知 |\n")
                else:
                    f.write("- 未检测到语义化HTML标签使用\n\n")
                
                # 标签嵌套分析
                f.write("### 标签嵌套深度\n\n")
                nesting_level = html_analysis.get('nesting_level', 0)
                f.write(f"最大嵌套深度为 **{nesting_level}** 级。\n\n")
                
                if nesting_level > 15:
                    f.write("⚠️ **警告**: 嵌套层级过深，可能导致性能问题和可维护性降低。\n\n")
                
                # 标签统计
                f.write("### 标签使用统计\n\n")
                if 'tag_counts' in html_analysis:
                    f.write("页面中使用的主要HTML标签:\n\n")
                    f.write("| 标签 | 数量 |\n")
                    f.write("|------|------|\n")
                    
                    for tag, count in html_analysis['tag_counts'].items():
                        f.write(f"| `<{tag}>` | {count} |\n")
                else:
                    f.write("未能获取标签使用统计\n\n")
            else:
                f.write("未能分析页面结构\n\n")
            
            # 布局分析
            f.write("## 页面布局分析\n\n")
            if 'layout' in html_analysis:
                layout = html_analysis['layout']
                
                f.write(f"### 布局类型: {layout.get('type', '未知')}\n\n")
                
                # 布局容器分析
                if 'containers' in layout and layout['containers']:
                    f.write("### 主要布局容器\n\n")
                    f.write("| 元素 | ID | 类名 | 子元素数量 |\n")
                    f.write("|------|------|------|------|\n")
                    
                    for container in layout['containers']:
                        element = container.get('element', '-')
                        container_id = container.get('id', '-')
                        classes = ', '.join(container.get('classes', [])) or '-'
                        children_count = container.get('children_count', 0)
                        
                        f.write(f"| `<{element}>` | {container_id} | {classes} | {children_count} |\n")
                
                # 布局特性
                f.write("\n### 布局特性\n\n")
                features = []
                
                if layout.get('responsive', False):
                    features.append("- ✅ **响应式设计**: 页面会根据视口大小调整布局")
                else:
                    features.append("- ❌ **非响应式设计**: 页面布局固定")
                
                if layout.get('grid_system', False):
                    features.append("- ✅ **网格系统**: 使用网格布局系统（如Bootstrap网格）")
                
                if layout.get('flex_layout', False):
                    features.append("- ✅ **弹性布局**: 使用CSS Flexbox")
                
                f.write('\n'.join(features))
    
    def _generate_components_document(self, html_analysis):
        """
        生成组件文档
        
        参数:
            html_analysis (dict): HTML分析结果
        """
        logger.info("生成组件文档...")
        
        file_path = os.path.join(self.output_dir, "3_components.md")
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("# 网页组件文档\n\n")
            
            if 'components' in html_analysis and html_analysis['components']:
                f.write(f"共检测到 **{len(html_analysis['components'])}** 个组件。\n\n")
                
                # 按组件类型分组
                component_types = {}
                for component in html_analysis['components']:
                    comp_type = component.get('type', '未知')
                    if comp_type not in component_types:
                        component_types[comp_type] = []
                    component_types[comp_type].append(component)
                
                # 遍历每种组件类型
                for comp_type, components in component_types.items():
                    f.write(f"## {comp_type.title()} 组件\n\n")
                    
                    for i, component in enumerate(components, 1):
                        # 组件基本信息
                        element = component.get('element', '')
                        component_id = component.get('id', '')
                        classes = component.get('classes', [])
                        text_length = component.get('text_length', 0)
                        method = component.get('identification_method', '')
                        
                        f.write(f"### {comp_type.title()} {i}\n\n")
                        f.write(f"- **元素类型**: `<{element}>`\n")
                        if component_id:
                            f.write(f"- **ID**: `{component_id}`\n")
                        if classes:
                            f.write(f"- **类名**: `{', '.join(classes)}`\n")
                        f.write(f"- **文本长度**: {text_length} 字符\n")
                        f.write(f"- **识别方法**: {method}\n\n")
                        
                        # 组件HTML片段(如果太长则截断)
                        html = component.get('html', '')
                        if html:
                            max_length = 500  # 最大显示长度
                            if len(html) > max_length:
                                html = html[:max_length] + "... (已截断)"
                            
                            f.write("#### 组件HTML片段\n\n")
                            f.write("```html\n")
                            f.write(html)
                            f.write("\n```\n\n")
                        
                        # 组件功能建议
                        f.write("#### 功能建议\n\n")
                        if comp_type == 'navigation':
                            f.write("- 实现为响应式导航栏组件\n")
                            f.write("- 考虑在小屏幕上折叠为汉堡菜单\n")
                        elif comp_type == 'header':
                            f.write("- 可包含公司标志、导航和搜索功能\n")
                            f.write("- 考虑添加固定顶部功能(sticky header)\n")
                        elif comp_type == 'footer':
                            f.write("- 包含版权信息、联系方式和链接\n")
                            f.write("- 使用flex布局使内容均匀分布\n")
                        elif comp_type == 'form':
                            f.write("- 实现表单验证\n")
                            f.write("- 添加提交反馈机制\n")
                        elif comp_type == 'card':
                            f.write("- 使用阴影和悬停效果增强用户体验\n")
                            f.write("- 保持卡片尺寸一致性\n")
                        else:
                            f.write("- 推荐使用独立组件实现\n")
            else:
                f.write("未检测到组件\n")
    
    def _generate_styles_document(self, style_analysis):
        """
        生成样式文档
        
        参数:
            style_analysis (dict): 样式分析结果
        """
        logger.info("生成样式文档...")
        
        file_path = os.path.join(self.output_dir, "4_styles.md")
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("# 网页样式文档\n\n")
            
            # 颜色方案
            f.write("## 颜色方案\n\n")
            colors = style_analysis.get('colors', [])
            if isinstance(colors, list) and colors:
                f.write("### 主要颜色\n\n")
                f.write("| 颜色代码 | 使用次数 | 可能用途 |\n")
                f.write("|---------|----------|--------|\n")
                
                color_count = 0
                for color_item in colors:
                    if color_count >= 10:  # 只显示前10种主要颜色
                        break
                    
                    color = color_item.get('color', '#000000')
                    count = color_item.get('count', 0)
                    
                    # 猜测颜色用途
                    usage = "未知"
                    if count > 20:
                        usage = "主题色"
                    elif 'background' in color_item.get('properties', []):
                        usage = "背景色"
                    elif 'color' in color_item.get('properties', []):
                        usage = "文本色"
                    elif 'border' in color_item.get('properties', []):
                        usage = "边框色"
                    
                    f.write(f"| `{color}` | {count} | {usage} |\n")
                    color_count += 1
            else:
                f.write("未能提取颜色数据\n\n")
            
            # 字体信息
            f.write("\n## 字体信息\n\n")
            fonts = style_analysis.get('fonts', [])
            if isinstance(fonts, list) and fonts:
                f.write("### 字体家族\n\n")
                f.write("| 字体名称 | 使用次数 | 可能用途 |\n")
                f.write("|---------|----------|--------|\n")
                
                font_count = 0
                for font_item in fonts:
                    if font_count >= 10:  # 只显示前10种字体
                        break
                    
                    font_family = font_item.get('font_family', 'Unknown')
                    count = font_item.get('count', 0)
                    
                    # 猜测字体用途
                    usage = "未知"
                    if count > 20:
                        usage = "主要字体"
                    elif 'h1' in font_item.get('selectors', ''):
                        usage = "标题字体"
                    elif 'p' in font_item.get('selectors', ''):
                        usage = "正文字体"
                    
                    f.write(f"| {font_family} | {count} | {usage} |\n")
                    font_count += 1
            else:
                f.write("未能提取字体信息\n\n")
            
            # 尺寸与间距
            f.write("\n## 尺寸与间距\n\n")
            spacing = style_analysis.get('spacing', {})
            if isinstance(spacing, dict):
                # 提取margin和padding值
                margin_values = spacing.get('margin', [])
                padding_values = spacing.get('padding', [])
                
                if isinstance(margin_values, list) and margin_values:
                    f.write("### 外边距(Margin)值\n\n")
                    f.write("| 值 | 使用次数 |\n")
                    f.write("|-----|-------|\n")
                    
                    margin_count = 0
                    for margin in margin_values:
                        if margin_count >= 10:  # 只显示前10个常用值
                            break
                            
                        if isinstance(margin, dict):
                            f.write(f"| {margin.get('value', '-')} | {margin.get('count', 0)} |\n")
                            margin_count += 1
                
                if isinstance(padding_values, list) and padding_values:
                    f.write("\n### 内边距(Padding)值\n\n")
                    f.write("| 值 | 使用次数 |\n")
                    f.write("|-----|-------|\n")
                    
                    padding_count = 0
                    for padding in padding_values:
                        if padding_count >= 10:  # 只显示前10个常用值
                            break
                            
                        if isinstance(padding, dict):
                            f.write(f"| {padding.get('value', '-')} | {padding.get('count', 0)} |\n")
                            padding_count += 1
            else:
                f.write("未能提取尺寸与间距信息\n\n")
                
            # 媒体查询和响应式设计
            f.write("\n## 响应式设计\n\n")
            media_queries = style_analysis.get('media_queries', [])
            if isinstance(media_queries, list) and media_queries:
                f.write("### 媒体查询断点\n\n")
                f.write("| 查询条件 | 可能用途 |\n")
                f.write("|----------|--------|\n")
                
                for query in media_queries:
                    condition = query.get('condition', '')
                    
                    # 猜测媒体查询用途
                    usage = "未知"
                    if 'max-width: 768px' in condition:
                        usage = "平板设备"
                    elif 'max-width: 576px' in condition:
                        usage = "手机设备"
                    elif 'min-width: 992px' in condition:
                        usage = "桌面设备"
                    
                    f.write(f"| `{condition}` | {usage} |\n")
            else:
                f.write("未检测到媒体查询，网页可能不是响应式设计\n\n")
    
    def _generate_index_document(self, html_analysis, style_analysis, url):
        """
        生成索引文档
        
        参数:
            html_analysis (dict): HTML分析结果
            style_analysis (dict): 样式分析结果
            url (str): 分析的网页URL
        """
        logger.info("生成索引文档...")
        
        file_path = os.path.join(self.output_dir, "index.md")
        
        with open(file_path, "w", encoding="utf-8") as f:
            title = html_analysis.get('title', '未命名网页')
            f.write(f"# {title} - 网页分析文档\n\n")
            
            # 生成时间
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"**生成时间**: {now}\n\n")
            
            # 分析的URL
            f.write(f"**分析URL**: [{url}]({url})\n\n")
            
            # 内容概览
            f.write("## 文档内容\n\n")
            f.write("本文档通过Web Clone Agent工具自动生成，包含以下几个部分：\n\n")
            f.write("1. [网页元数据](1_metadata.md) - 包含页面标题、描述、关键词等信息\n")
            f.write("2. [网页结构](2_structure.md) - 详细分析页面结构与布局\n")
            f.write("3. [网页组件](3_components.md) - 识别的主要页面组件及详情\n")
            f.write("4. [网页样式](4_styles.md) - 颜色方案、字体、尺寸等样式信息\n")
            f.write("5. [实现建议](5_implementation.md) - 网页重建的技术建议\n\n")
            
            # 简要统计
            f.write("## 简要统计\n\n")
            
            # 组件统计
            components = html_analysis.get('components', [])
            component_count = len(components) if isinstance(components, list) else 0
            f.write(f"- **组件总数**: {component_count} 个\n")
            
            # 颜色统计
            colors = style_analysis.get('colors', [])
            color_count = len(colors) if isinstance(colors, list) else 0
            f.write(f"- **使用颜色**: {color_count} 种\n")
            
            # 字体统计
            fonts = style_analysis.get('fonts', [])
            font_count = len(fonts) if isinstance(fonts, list) else 0
            f.write(f"- **字体家族**: {font_count} 种\n")
            
            # 页面类型猜测
            layout = html_analysis.get('layout', {})
            layout_type = layout.get('type', '未知') if isinstance(layout, dict) else '未知'
            f.write(f"- **布局类型**: {layout_type}\n")
            
            # 是否响应式
            is_responsive = '是' if (isinstance(layout, dict) and layout.get('responsive', False)) else '否'
            f.write(f"- **响应式设计**: {is_responsive}\n\n")
            
            # 文档用途说明
            f.write("## 文档用途\n\n")
            f.write("本文档可作为网页重建、设计参考或前端开发的基础。它提供了对原始网页结构、组件和样式的详细分析，")
            f.write("可以帮助开发者理解页面的组织方式，而无需直接复制原始代码。\n\n")
            
            f.write("建议使用本文档作为实现指南，结合现代前端框架（如Vue、React或Angular）重新构建页面，")
            f.write("同时遵循文档中提取的设计规范和组织结构。\n")
    
    def _generate_implementation_document(self, html_analysis, style_analysis):
        """
        生成实现建议文档
        
        参数:
            html_analysis (dict): HTML分析结果
            style_analysis (dict): 样式分析结果
        """
        logger.info("生成实现建议文档...")
        
        file_path = os.path.join(self.output_dir, "5_implementation.md")
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("# 网页实现建议\n\n")
            
            # 技术栈建议
            f.write("## 推荐技术栈\n\n")
            
            # 根据页面结构和布局推荐技术栈
            layout = html_analysis.get('layout', {})
            component_count = len(html_analysis.get('components', []))
            
            f.write("### 前端框架\n\n")
            
            # 根据复杂度推荐不同框架
            if component_count > 15 or layout.get('type') == 'grid':
                f.write("推荐使用 **Vue.js** 或 **React** 等现代组件化框架，原因：\n\n")
                f.write("- 页面组件较多，适合组件化开发\n")
                f.write("- 可能需要状态管理和路由功能\n")
                f.write("- 便于实现响应式布局和交互功能\n")
            else:
                f.write("可以考虑使用简单的框架如 **Alpine.js** 或原生JavaScript，原因：\n\n")
                f.write("- 页面结构相对简单，不需要复杂框架\n")
                f.write("- 减少不必要的依赖，提升加载性能\n")
            
            f.write("\n### CSS方案\n\n")
            
            # 根据样式分析推荐CSS方案
            if 'spacing' in style_analysis and 'media_queries' in style_analysis:
                f.write("推荐使用 **Tailwind CSS** 或 **Bootstrap 5**，原因：\n\n")
                f.write("- 页面使用了规范化的间距和尺寸\n")
                f.write("- 需要响应式布局支持\n")
                f.write("- 可快速实现分析文档中的设计风格\n")
            else:
                f.write("可以使用 **SCSS/SASS** 自定义样式，原因：\n\n")
                f.write("- 页面样式可能有定制化需求\n")
                f.write("- 需要更精细的样式控制\n")
            
            # 组件结构建议
            f.write("\n## 组件结构建议\n\n")
            f.write("根据分析结果，推荐将页面拆分为以下组件结构：\n\n")
            
            # 构建组件树
            components = html_analysis.get('components', [])
            component_types = set()
            for component in components:
                component_types.add(component.get('type'))
            
            f.write("```\nApp/\n")
            f.write("├── Layout/\n")
            
            # 添加布局组件
            if 'header' in component_types:
                f.write("│   ├── Header\n")
            if 'navigation' in component_types:
                f.write("│   ├── Navigation\n")
            if 'sidebar' in component_types:
                f.write("│   ├── Sidebar\n")
            if 'footer' in component_types:
                f.write("│   └── Footer\n")
            
            f.write("│\n├── Components/\n")
            
            # 添加内容组件
            for component_type in component_types:
                if component_type not in ['header', 'navigation', 'sidebar', 'footer']:
                    f.write(f"│   ├── {component_type.title()}\n")
            
            f.write("│\n└── Pages/\n")
            f.write("    └── Home\n")
            f.write("```\n\n")
            
            # 响应式设计建议
            f.write("## 响应式设计建议\n\n")
            
            if layout.get('responsive', False):
                f.write("分析显示页面具有响应式设计，推荐以下断点：\n\n")
                f.write("- **移动设备**: < 576px\n")
                f.write("- **平板设备**: 576px - 992px\n")
                f.write("- **桌面设备**: > 992px\n\n")
                
                f.write("实现方式：\n\n")
                f.write("1. 使用媒体查询适配不同屏幕尺寸\n")
                f.write("2. 采用弹性布局或网格布局\n")
                f.write("3. 对大型元素使用相对尺寸（百分比或视口单位）\n")
            else:
                f.write("分析显示页面可能不是响应式设计。建议添加以下响应式功能：\n\n")
                f.write("1. 添加媒体查询以适配不同设备\n")
                f.write("2. 将固定宽度改为弹性布局\n")
                f.write("3. 为导航栏添加移动设备折叠功能\n")
            
            # 性能优化建议
            f.write("\n## 性能优化建议\n\n")
            tag_count = sum(html_analysis.get('structure', {}).get('tag_counts', {}).values())
            
            if tag_count > 200:
                f.write("页面元素较多，建议注意以下性能优化：\n\n")
                f.write("1. 使用组件懒加载\n")
                f.write("2. 图片使用延迟加载\n")
                f.write("3. 考虑分割大型组件\n")
                f.write("4. 使用虚拟滚动处理长列表\n")
            else:
                f.write("页面结构较为简单，基本优化建议：\n\n")
                f.write("1. 优化图片资源\n")
                f.write("2. 最小化CSS和JavaScript文件\n")
                f.write("3. 使用适当的缓存策略\n")
    
    def _convert_to_html(self):
        """将所有Markdown文档转换为HTML格式"""
        logger.info("转换文档为HTML格式...")
        
        try:
            # 尝试导入markdown模块
            import markdown
        except ImportError:
            logger.warning("未安装markdown模块，跳过HTML转换")
            return
        
        # 获取所有Markdown文件
        md_files = [f for f in os.listdir(self.output_dir) if f.endswith('.md')]
        
        for md_file in md_files:
            # 读取Markdown内容
            md_path = os.path.join(self.output_dir, md_file)
            try:
                with open(md_path, 'r', encoding='utf-8') as f:
                    md_content = f.read()
            except Exception as e:
                logger.error(f"读取文件 {md_path} 时出错: {str(e)}")
                continue
            
            # 转换为HTML
            try:
                # 使用基本扩展
                html_content = markdown.markdown(md_content, extensions=[
                    'tables', 'fenced_code'
                ])
            except Exception as e:
                logger.error(f"转换Markdown到HTML时出错: {str(e)}")
                continue
            
            # 添加基本样式
            styled_html = f"""
            <!DOCTYPE html>
            <html lang="zh-CN">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>{md_file.replace('.md', '')}</title>
                <style>
                    body {{
                        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
                        line-height: 1.6;
                        max-width: 900px;
                        margin: 0 auto;
                        padding: 20px;
                        color: #333;
                    }}
                    pre {{
                        background-color: #f5f5f5;
                        padding: 15px;
                        border-radius: 5px;
                        overflow-x: auto;
                    }}
                    code {{
                        font-family: Consolas, Monaco, 'Andale Mono', monospace;
                    }}
                    table {{
                        border-collapse: collapse;
                        width: 100%;
                        margin: 20px 0;
                    }}
                    table, th, td {{
                        border: 1px solid #ddd;
                    }}
                    th, td {{
                        padding: 12px;
                        text-align: left;
                    }}
                    th {{
                        background-color: #f2f2f2;
                    }}
                    a {{
                        color: #0366d6;
                        text-decoration: none;
                    }}
                    a:hover {{
                        text-decoration: underline;
                    }}
                </style>
            </head>
            <body>
                {html_content}
                <hr>
                <footer>
                    <p><small>由 Web Clone Agent 生成</small></p>
                </footer>
            </body>
            </html>
            """
            
            # 保存HTML文件
            html_path = os.path.join(self.output_dir, md_file.replace('.md', '.html'))
            try:
                with open(html_path, 'w', encoding='utf-8') as f:
                    f.write(styled_html)
                logger.info(f"已生成HTML文档: {html_path}")
            except Exception as e:
                logger.error(f"保存HTML文件 {html_path} 时出错: {str(e)}")
    
    def generate_document(self, html_analysis, style_analysis, url):
        """
        生成完整的网页设计文档
        
        这是主要的公共方法，协调整个文档生成过程。
        
        参数:
            html_analysis (dict): HTML分析结果，包含页面结构和组件信息
            style_analysis (dict): CSS样式分析结果，包含颜色、字体和组件样式
            url (str): 分析的网页URL
            
        返回:
            bool: 生成是否成功
        """
        logger.info(f"开始生成网页文档到目录: {self.output_dir}")
        
        try:
            # 生成元数据文档
            self._generate_metadata_document(html_analysis)
            
            # 生成结构文档
            self._generate_structure_document(html_analysis)
            
            # 生成组件文档
            self._generate_components_document(html_analysis)
            
            # 生成样式文档
            self._generate_styles_document(style_analysis)
            
            # 生成实现建议文档
            self._generate_implementation_document(html_analysis, style_analysis)
            
            # 生成索引文档
            self._generate_index_document(html_analysis, style_analysis, url)
            
            # 转换所有文档为HTML格式
            self._convert_to_html()
            
            # 生成YAML数据文件（方便机器读取）
            self._generate_yaml_data(html_analysis, style_analysis, url)
            
            logger.info("✅ 网页设计文档生成成功!")
            return True
            
        except Exception as e:
            logger.error(f"❌ 生成网页文档时出错: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return False
    
    def _generate_yaml_data(self, html_analysis, style_analysis, url):
        """
        生成YAML格式的数据文件
        
        参数:
            html_analysis (dict): HTML分析结果
            style_analysis (dict): 样式分析结果
            url (str): 分析的网页URL
        """
        logger.info("生成YAML数据文件...")
        
        # 准备数据
        data = {
            'url': url,
            'generated_at': datetime.now().isoformat(),
            'page_title': html_analysis.get('title', '未命名网页'),
            'meta': html_analysis.get('meta', {}),
            'components': [
                {
                    'type': c.get('type'),
                    'element': c.get('element'),
                    'id': c.get('id', ''),
                    'classes': c.get('classes', []),
                }
                for c in html_analysis.get('components', [])
            ],
            'layout': html_analysis.get('layout', {}),
            'colors': [
                {
                    'color': c.get('color'),
                    'count': c.get('count'),
                    'properties': c.get('properties', [])
                }
                for c in (style_analysis.get('colors', [])[:10] if isinstance(style_analysis.get('colors', []), list) else [])
            ],
            'fonts': [
                {
                    'font_family': f.get('font_family'),
                    'count': f.get('count')
                }
                for f in style_analysis.get('fonts', [])
            ]
        }
        
        # 保存YAML文件
        yaml_path = os.path.join(self.output_dir, "site_data.yaml")
        with open(yaml_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, sort_keys=False, default_flow_style=False, allow_unicode=True)