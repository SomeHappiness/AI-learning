#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Vue项目生成器模块 (vue_generator.py)
------------------------------
该模块负责根据HTML和CSS分析结果生成完整的Vue项目，包括组件、视图、路由、状态管理等。

主要功能:
1. 创建Vue项目的基本目录结构
2. 根据提取的组件生成Vue单文件组件(.vue文件)
3. 生成页面视图组件
4. 配置路由和状态管理
5. 生成项目配置文件

工作原理:
模块分析HTML和CSS的结构信息，将其转换为Vue项目的各个部分，生成可运行的Vue应用。
生成的项目符合Vue最佳实践，包含响应式设计和组件化结构。
"""

import os
import re
import json
import shutil
import logging
import jsbeautifier
from tqdm import tqdm

# 配置日志
logger = logging.getLogger(__name__)

class VueGenerator:
    """
    Vue项目生成器类
    
    负责将网页分析结果转换为完整的Vue.js项目，
    包括组件、视图、路由、状态管理和样式。
    """
    
    def __init__(self, output_dir="vue-project"):
        """
        初始化Vue项目生成器
        
        参数:
            output_dir (str): 生成的Vue项目输出目录
        """
        self.output_dir = output_dir
        
        # JS代码格式化选项，用于生成美观的代码
        self.js_options = jsbeautifier.default_options()
        self.js_options.indent_size = 2
        
        # Vue项目的版本和依赖配置
        self.vue_version = "^3.2.47"
        self.dependencies = {
            "vue": self.vue_version,
            "vue-router": "^4.1.6",
            "vuex": "^4.1.0",
            "axios": "^1.3.4"
        }
        
        # 为开发环境配置的依赖
        self.dev_dependencies = {
            "@vitejs/plugin-vue": "^4.1.0",
            "sass": "^1.59.3",
            "vite": "^4.2.0"
        }
    
    def generate_project(self, html_analysis, style_analysis, page_meta):
        """
        生成完整的Vue项目
        
        这是主要的公共方法，协调整个项目生成过程。
        
        参数:
            html_analysis (dict): HTML分析结果，包含页面结构和组件信息
            style_analysis (dict): CSS样式分析结果，包含颜色、字体和组件样式
            page_meta (dict): 页面元数据，如标题、描述等
        
        返回:
            bool: 生成是否成功
        """
        logger.info(f"开始生成Vue项目到目录: {self.output_dir}")
        
        try:
            # 第1步: 创建项目目录结构
            self._create_project_structure()
            
            # 第2步: 生成组件
            self._generate_components(html_analysis, style_analysis)
            
            # 第3步: 生成视图页面
            self._generate_views(html_analysis, style_analysis, page_meta)
            
            # 第4步: 配置路由
            self._generate_router()
            
            # 第5步: 配置状态管理
            self._generate_store()
            
            # 第6步: 生成主要文件(main.js, App.vue等)
            self._generate_main_files(page_meta)
            
            # 第7步: 生成项目配置文件(package.json, vite.config.js等)
            self._generate_config_files()
            
            # 第8步: 复制样式文件(如果存在)
            if os.path.exists(os.path.join("output", "styles")):
                shutil.copytree(
                    os.path.join("output", "styles"),
                    os.path.join(self.output_dir, "src", "assets", "styles"),
                    dirs_exist_ok=True
                )
            
            logger.info("✅ Vue项目生成成功!")
            return True
        
        except Exception as e:
            logger.error(f"❌ 生成Vue项目时出错: {str(e)}")
            return False
    
    def _create_project_structure(self):
        """
        创建Vue项目的目录结构
        
        创建标准的Vue项目目录结构，包括:
        - public: 静态资源目录
        - src: 源代码目录
          - assets: 资源文件(图片、样式等)
          - components: 组件目录
          - views: 视图页面
          - router: 路由配置
          - store: 状态管理
          - utils: 工具函数
        """
        logger.info("创建项目目录结构...")
        
        # 定义需要创建的目录列表
        dirs = [
            '',                  # 项目根目录
            'public',            # 静态资源目录
            'src',               # 源代码目录
            'src/assets',        # 资源文件目录
            'src/assets/images', # 图片目录
            'src/assets/styles', # 样式目录
            'src/components',    # 组件目录
            'src/views',         # 视图页面目录
            'src/router',        # 路由配置目录
            'src/store',         # 状态管理目录
            'src/utils'          # 工具函数目录
        ]
        
        # 创建每个目录，如果已存在则不报错
        for d in dirs:
            dir_path = os.path.join(self.output_dir, d)
            os.makedirs(dir_path, exist_ok=True)
            logger.debug(f"创建目录: {dir_path}")
    
    def _generate_components(self, html_analysis, style_analysis):
        """
        生成Vue组件文件
        
        根据HTML分析结果生成Vue单文件组件(.vue文件)。
        主要生成的组件包括:
        - 布局组件(Header, Footer, Sidebar)
        - 内容组件(Card, Navigation, Form, Table等)
        
        参数:
            html_analysis (dict): HTML分析结果
            style_analysis (dict): 样式分析结果
        """
        logger.info("生成Vue组件...")
        
        # 生成Header组件 (如果存在)
        if 'layout' in html_analysis and html_analysis['layout'].get('header'):
            self._create_component(
                'Header',  # 组件名称
                html_analysis['layout']['header']['element'],  # HTML内容
                style_analysis,  # 样式信息
                'layout'  # 组件类型
            )
        
        # 生成Footer组件 (如果存在)
        if 'layout' in html_analysis and html_analysis['layout'].get('footer'):
            self._create_component(
                'Footer',
                html_analysis['layout']['footer']['element'],
                style_analysis,
                'layout'
            )
        
        # 生成Sidebar组件 (如果存在)
        if 'layout' in html_analysis and html_analysis['layout'].get('sidebar'):
            self._create_component(
                'Sidebar',
                html_analysis['layout']['sidebar']['element'],
                style_analysis,
                'layout'
            )
        
        # 生成识别出的其他组件
        for component in html_analysis.get('components', []):
            # 只生成特定类型的组件
            if 'type' in component:
                component_name = component['type'].capitalize()
                if component_name.lower() in ['card', 'navigation', 'form', 'table', 'button', 'modal']:
                    # 获取组件HTML内容 (优先使用html字段，否则使用sample字段)
                    html_content = component.get('html', component.get('sample', ''))
                    
                    self._create_component(
                        component_name,
                        html_content,
                        style_analysis,
                        component_name.lower()
                    )
    
    def _create_component(self, name, html_content, style_analysis, component_type):
        """
        创建单个Vue组件文件
        
        生成包含模板、脚本和样式的Vue单文件组件(.vue)。
        
        参数:
            name (str): 组件名称
            html_content (str): 组件的HTML内容
            style_analysis (dict): 样式分析结果
            component_type (str): 组件类型(layout, card, navigation等)
        """
        # 格式化组件名称为PascalCase (Vue组件命名规范)
        formatted_name = ''.join(word.capitalize() for word in re.split(r'[-_\s]', name))
        file_path = os.path.join(self.output_dir, 'src', 'components', f'{formatted_name}.vue')
        
        # 简化和清理HTML内容，使其适合Vue模板
        if html_content:
            html_content = self._simplify_html(html_content)
        else:
            # 如果没有HTML内容，创建一个简单的占位符
            html_content = f'<div><!-- {formatted_name} 组件 --></div>'
        
        # 创建Vue组件文件
        with open(file_path, 'w', encoding='utf-8') as f:
            # 1. 组件模板部分 (template)
            f.write('<template>\n')
            f.write(f'  <div class="v-{component_type.lower()}">\n')
            
            # 清理HTML并进行缩进
            cleaned_html = self._clean_html_for_vue(html_content)
            indented_html = '\n'.join(f'    {line}' for line in cleaned_html.split('\n'))
            f.write(indented_html)
            
            f.write('\n  </div>\n')
            f.write('</template>\n\n')
            
            # 2. 组件脚本部分 (script)
            f.write('<script>\nexport default {\n')
            f.write(f'  name: \'{formatted_name}\',\n')
            f.write('  props: {\n')
            
            # 根据组件类型添加适当的props
            if component_type.lower() == 'card':
                f.write('    title: {\n      type: String,\n      default: \'\'\n    },\n')
                f.write('    content: {\n      type: String,\n      default: \'\'\n    },\n')
                f.write('    image: {\n      type: String,\n      default: \'\'\n    }\n')
            elif component_type.lower() == 'navigation':
                f.write('    items: {\n      type: Array,\n      default: () => []\n    }\n')
            elif component_type.lower() == 'table':
                f.write('    headers: {\n      type: Array,\n      default: () => []\n    },\n')
                f.write('    items: {\n      type: Array,\n      default: () => []\n    }\n')
            elif component_type.lower() == 'form':
                f.write('    formData: {\n      type: Object,\n      default: () => ({})\n    },\n')
                f.write('    submitUrl: {\n      type: String,\n      default: \'\'\n    }\n')
            elif component_type.lower() == 'button':
                f.write('    text: {\n      type: String,\n      default: \'按钮\'\n    },\n')
                f.write('    type: {\n      type: String,\n      default: \'primary\'\n    }\n')
            else:
                f.write('    // 自定义props\n')
            
            f.write('  },\n')
            
            # 组件数据
            f.write('  data() {\n    return {\n      // 组件数据\n    }\n  },\n')
            
            # 组件方法
            f.write('  methods: {\n')
            # 为特定组件添加方法
            if component_type.lower() == 'form':
                f.write('    submitForm() {\n')
                f.write('      // 表单提交逻辑\n')
                f.write('      this.$emit(\'submit\', this.formData);\n')
                f.write('    },\n')
                f.write('    resetForm() {\n')
                f.write('      // 重置表单逻辑\n')
                f.write('    }\n')
            elif component_type.lower() == 'navigation':
                f.write('    navigate(item) {\n')
                f.write('      // 导航逻辑\n')
                f.write('    }\n')
            else:
                f.write('    // 组件方法\n')
            f.write('  }\n')
            f.write('}\n</script>\n\n')
            
            # 3. 组件样式部分 (style)
            f.write('<style lang="scss" scoped>\n')
            # 导入相关样式
            f.write(f'@import "@/assets/styles/{component_type.lower()}.scss";\n')
            
            # 添加特定组件样式
            f.write('\n// 组件特定样式\n')
            f.write(f'.v-{component_type.lower()} {{\n')
            
            # 检查是否有此组件的样式
            if component_type.lower() in style_analysis.get('component_styles', {}):
                # 提取部分样式规则
                styles = style_analysis['component_styles'][component_type.lower()]
                if styles:
                    # 简化输出样式
                    for i, (selector, rules) in enumerate(styles.items()):
                        if i < 3:  # 限制输出规则数量
                            for prop, value in rules.items():
                                f.write(f'  {prop}: {value};\n')
            else:
                f.write('  // 自定义样式\n')
            
            f.write('}}\n')
            f.write('</style>\n')
        
        logger.info(f"已创建组件: {formatted_name}")
            
    def _clean_html_for_vue(self, html_content):
        """
        清理HTML使其适合Vue模板语法
        
        这个方法将标准HTML转换为Vue模板格式:
        - 将常规HTML属性转换为Vue指令(如class变为:class)
        - 将传统事件处理器转换为Vue事件处理器(如onclick变为@click)
        - 将<a>标签转换为<router-link>组件
        - 移除脚本和样式标签
        
        参数:
            html_content (str): 原始HTML内容
        
        返回:
            str: 转换后适合Vue的HTML内容
        """
        # 如果HTML内容为空，返回空字符串
        if not html_content:
            return ""
            
        # 定义HTML属性到Vue指令的转换规则
        replacements = {
            'class=': ':class=',              # 动态class绑定
            'onclick=': '@click=',            # 点击事件
            'onchange=': '@change=',          # 变更事件
            'onsubmit=': '@submit.prevent=',  # 表单提交事件(带有prevent默认行为)
            'onmouseover=': '@mouseover=',    # 鼠标悬停事件
            'onmouseout=': '@mouseout=',      # 鼠标离开事件
            'href=': ':to=',                  # 路由链接
            '<a ': '<router-link ',           # 路由链接组件
            '</a>': '</router-link>'          # 路由链接组件闭合标签
        }
        
        # 应用替换规则
        result = html_content
        for old, new in replacements.items():
            result = result.replace(old, new)
        
        # 移除脚本标签及其内容
        result = re.sub(r'<script.*?</script>', '', result, flags=re.DOTALL)
        
        # 移除样式标签及其内容
        result = re.sub(r'<style.*?</style>', '', result, flags=re.DOTALL)
        
        # 移除HTML注释
        result = re.sub(r'<!--.*?-->', '', result, flags=re.DOTALL)
        
        # 修复可能的语法问题
        # 将纯文本引号替换为转义引号，防止Vue模板解析错误
        result = result.replace('"', '&quot;').replace("'", '&apos;')
        # 恢复Vue指令中的引号
        result = result.replace(':class=&quot;', ':class="').replace(':class=&apos;', ":class='")
        result = result.replace('@click=&quot;', '@click="').replace('@click=&apos;', "@click='")
        
        return result
    
    def _simplify_html(self, html_content):
        """
        简化HTML内容，使其更适合Vue组件
        
        这个方法:
        - 移除不必要的嵌套结构
        - 删除多余的属性和内联样式
        - 保留关键内容和结构
        - 限制HTML内容长度，避免生成过大的组件
        
        参数:
            html_content (str): 原始HTML内容
        
        返回:
            str: 简化后的HTML内容
        """
        if not html_content:
            return ""
        
        # 处理可能的字符串情况
        if isinstance(html_content, str):
            # 如果内容太长，截断它
            if len(html_content) > 2000:
                html_content = html_content[:2000] + "..."
            
            # 移除常见的无用属性
            for attr in ['data-', 'aria-', 'xmlns', 'itemscope', 'itemtype']:
                html_content = re.sub(r'\s+' + attr + r'[^\s>]*', '', html_content)
            
            # 移除内联样式(在Vue中我们使用组件样式)
            html_content = re.sub(r'\s+style="[^"]*"', '', html_content)
            
            # 移除JavaScript事件属性(在Vue中我们使用@事件语法)
            html_content = re.sub(r'\s+on\w+="[^"]*"', '', html_content)
            
            # 移除id属性(在Vue组件中通常不需要)
            html_content = re.sub(r'\s+id="[^"]*"', '', html_content)
            
            # 简化链接，保持基本结构
            html_content = re.sub(r'<a\s+[^>]*>(.*?)</a>', r'<a href="#">\1</a>', html_content)
            
            # 移除图片的src，在Vue中使用:src绑定
            html_content = re.sub(r'<img\s+[^>]*src="[^"]*"([^>]*)>', r'<img :src="imageUrl"\1>', html_content)
            
            # 保留表单元素，但简化属性
            html_content = re.sub(r'<input\s+[^>]*>', r'<input v-model="formData.field">', html_content)
            html_content = re.sub(r'<textarea\s+[^>]*>', r'<textarea v-model="formData.field"></textarea>', html_content)
            html_content = re.sub(r'<select\s+[^>]*>(.*?)</select>', r'<select v-model="formData.field">\1</select>', html_content)
        
        return html_content
    
    def _generate_views(self, html_analysis, style_analysis, page_meta):
        """
        生成Vue视图页面组件
        
        视图页面是应用程序的主要界面，通常包含多个小组件。
        本方法根据HTML分析结果生成主要视图页面。
        
        参数:
            html_analysis (dict): HTML分析结果
            style_analysis (dict): 样式分析结果
            page_meta (dict): 页面元数据
        """
        logger.info("生成Vue视图页面...")
        
        # 创建Home视图(首页)
        self._create_home_view(html_analysis, style_analysis, page_meta)
        
        # 根据组件类型创建其他视图
        self._create_additional_views(html_analysis)
    
    def _create_home_view(self, html_analysis, style_analysis, page_meta):
        """
        创建首页视图组件
        
        首页是应用的主要入口点，通常包含布局组件和主要内容。
        
        参数:
            html_analysis (dict): HTML分析结果
            style_analysis (dict): 样式分析结果
            page_meta (dict): 页面元数据
        """
        file_path = os.path.join(self.output_dir, 'src', 'views', 'HomeView.vue')
        
        with open(file_path, 'w', encoding='utf-8') as f:
            # 1. 模板部分
            f.write('<template>\n')
            f.write('  <div class="home">\n')
            
            # 添加Header组件(如果存在)
            if 'layout' in html_analysis and html_analysis['layout'].get('header'):
                f.write('    <Header />\n')
            
            # 创建主内容区域的布局
            has_sidebar = 'layout' in html_analysis and html_analysis['layout'].get('sidebar')
            
            # 根据是否有侧边栏决定布局
            if has_sidebar:
                # 带侧边栏的两栏布局
                sidebar_position = html_analysis['layout']['sidebar'].get('position', 'left')
                
                f.write('    <div class="main-container">\n')
                
                if sidebar_position == 'left':
                    f.write('      <Sidebar class="sidebar" />\n')
                    f.write('      <main class="content">\n')
                    self._add_content_sections(f, html_analysis)
                    f.write('      </main>\n')
                else:
                    f.write('      <main class="content">\n')
                    self._add_content_sections(f, html_analysis)
                    f.write('      </main>\n')
                    f.write('      <Sidebar class="sidebar" />\n')
                
                f.write('    </div>\n')
            else:
                # 单栏布局
                f.write('    <main class="content">\n')
                self._add_content_sections(f, html_analysis)
                f.write('    </main>\n')
            
            # 添加Footer组件(如果存在)
            if 'layout' in html_analysis and html_analysis['layout'].get('footer'):
                f.write('    <Footer />\n')
            
            f.write('  </div>\n')
            f.write('</template>\n\n')
            
            # 2. 脚本部分
            f.write('<script>\n')
            
            # 导入组件
            f.write('// 导入布局组件\n')
            imports = []
            
            if 'layout' in html_analysis and html_analysis['layout'].get('header'):
                imports.append('import Header from "../components/Header.vue";')
            
            if 'layout' in html_analysis and html_analysis['layout'].get('footer'):
                imports.append('import Footer from "../components/Footer.vue";')
            
            if has_sidebar:
                imports.append('import Sidebar from "../components/Sidebar.vue";')
            
            # 导入内容组件
            f.write('// 导入内容组件\n')
            content_components = []
            
            for component in html_analysis.get('components', []):
                if 'type' in component and component['type'].lower() in ['card', 'form', 'table']:
                    component_name = component['type'].capitalize()
                    import_stmt = f'import {component_name} from "../components/{component_name}.vue";'
                    if import_stmt not in imports and import_stmt not in content_components:
                        content_components.append(import_stmt)
            
            # 写入所有导入语句
            for imp in imports + content_components:
                f.write(imp + '\n')
            
            # 组件定义
            f.write('\nexport default {\n')
            f.write('  name: "HomeView",\n')
            
            # 注册组件
            f.write('  components: {\n')
            components = []
            
            if 'layout' in html_analysis and html_analysis['layout'].get('header'):
                components.append('    Header')
            
            if 'layout' in html_analysis and html_analysis['layout'].get('footer'):
                components.append('    Footer')
            
            if has_sidebar:
                components.append('    Sidebar')
            
            # 添加内容组件
            for component in html_analysis.get('components', []):
                if 'type' in component and component['type'].lower() in ['card', 'form', 'table']:
                    component_name = component['type'].capitalize()
                    if component_name not in [c.strip() for c in components]:
                        components.append(f'    {component_name}')
            
            f.write(',\n'.join(components))
            f.write('\n  },\n')
            
            # 添加数据
            f.write('  data() {\n')
            f.write('    return {\n')
            f.write(f'      title: "{page_meta.get("title", "首页")}",\n')
            
            # 根据分析结果添加适当的数据
            if any(c.get('type') == 'card' for c in html_analysis.get('components', [])):
                f.write('      cards: [\n')
                f.write('        { id: 1, title: "卡片1", content: "卡片内容1", image: "" },\n')
                f.write('        { id: 2, title: "卡片2", content: "卡片内容2", image: "" },\n')
                f.write('      ],\n')
            
            if any(c.get('type') == 'table' for c in html_analysis.get('components', [])):
                f.write('      tableData: {\n')
                f.write('        headers: ["列1", "列2", "列3"],\n')
                f.write('        rows: [\n')
                f.write('          ["数据1-1", "数据1-2", "数据1-3"],\n')
                f.write('          ["数据2-1", "数据2-2", "数据2-3"]\n')
                f.write('        ]\n')
                f.write('      },\n')
            
            f.write('    };\n')
            f.write('  },\n')
            
            # 添加方法
            f.write('  methods: {\n')
            f.write('    // 页面方法\n')
            f.write('  }\n')
            f.write('};\n')
            f.write('</script>\n\n')
            
            # 3. 样式部分
            f.write('<style lang="scss">\n')
            f.write('/* 首页样式 */\n')
            f.write('.home {\n')
            f.write('  display: flex;\n')
            f.write('  flex-direction: column;\n')
            f.write('  min-height: 100vh;\n')
            f.write('}\n\n')
            
            # 主容器样式
            f.write('.main-container {\n')
            f.write('  display: flex;\n')
            f.write('  flex: 1;\n')
            
            # 根据侧边栏位置设置方向
            if has_sidebar:
                sidebar_position = html_analysis['layout']['sidebar'].get('position', 'left')
                if sidebar_position == 'right':
                    f.write('  flex-direction: row;\n')
                else:
                    f.write('  flex-direction: row;\n')
            
            f.write('}\n\n')
            
            # 侧边栏样式
            if has_sidebar:
                f.write('.sidebar {\n')
                f.write('  width: 250px;\n')
                f.write('  padding: 20px;\n')
                f.write('  background-color: #f5f5f5;\n')
                f.write('}\n\n')
            
            # 内容区域样式
            f.write('.content {\n')
            f.write('  flex: 1;\n')
            f.write('  padding: 20px;\n')
            f.write('}\n\n')
            
            # 卡片容器样式
            if any(c.get('type') == 'card' for c in html_analysis.get('components', [])):
                f.write('.card-container {\n')
                f.write('  display: grid;\n')
                f.write('  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));\n')
                f.write('  gap: 20px;\n')
                f.write('  margin-bottom: 20px;\n')
                f.write('}\n')
            
            f.write('</style>\n')
        
        logger.info("已创建 HomeView 组件")
    
    def _create_additional_views(self, html_analysis):
        """
        创建其他视图页面
        
        根据HTML分析中识别出的组件创建额外的视图页面。
        例如，如果存在表单组件，可能需要创建表单页面。
        
        参数:
            html_analysis (dict): HTML分析结果
        """
        # 检查是否需要创建表单页面
        has_form = any(c.get('type') == 'form' for c in html_analysis.get('components', []))
        if has_form:
            self._create_form_view()
        
        # 检查是否需要创建关于页面
        if html_analysis.get('meta', {}).get('description'):
            self._create_about_view(html_analysis.get('meta', {}))
    
    def _create_form_view(self):
        """创建表单页面视图"""
        file_path = os.path.join(self.output_dir, 'src', 'views', 'FormView.vue')
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('<template>\n')
            f.write('  <div class="form-page">\n')
            f.write('    <h1>表单页面</h1>\n')
            f.write('    <Form :formData="formData" @submit="handleSubmit" />\n')
            f.write('  </div>\n')
            f.write('</template>\n\n')
            
            f.write('<script>\n')
            f.write('import Form from "../components/Form.vue";\n\n')
            f.write('export default {\n')
            f.write('  name: "FormView",\n')
            f.write('  components: {\n')
            f.write('    Form\n')
            f.write('  },\n')
            f.write('  data() {\n')
            f.write('    return {\n')
            f.write('      formData: {}\n')
            f.write('    };\n')
            f.write('  },\n')
            f.write('  methods: {\n')
            f.write('    handleSubmit(data) {\n')
            f.write('      console.log("表单提交数据:", data);\n')
            f.write('      // 处理表单提交\n')
            f.write('    }\n')
            f.write('  }\n')
            f.write('};\n')
            f.write('</script>\n\n')
            
            f.write('<style lang="scss">\n')
            f.write('.form-page {\n')
            f.write('  padding: 20px;\n')
            f.write('  max-width: 800px;\n')
            f.write('  margin: 0 auto;\n')
            f.write('}\n')
            f.write('</style>\n')
        
        logger.info("已创建 FormView 组件")
    
    def _create_about_view(self, meta):
        """
        创建关于页面视图
        
        参数:
            meta (dict): 页面元数据
        """
        file_path = os.path.join(self.output_dir, 'src', 'views', 'AboutView.vue')
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('<template>\n')
            f.write('  <div class="about">\n')
            f.write('    <h1>关于我们</h1>\n')
            
            # 使用meta描述
            if meta.get('description'):
                f.write(f'    <p>{meta["description"]}</p>\n')
            else:
                f.write('    <p>这是关于页面。</p>\n')
            
            f.write('  </div>\n')
            f.write('</template>\n\n')
            
            f.write('<style lang="scss">\n')
            f.write('.about {\n')
            f.write('  padding: 20px;\n')
            f.write('  max-width: 800px;\n')
            f.write('  margin: 0 auto;\n')
            f.write('}\n')
            f.write('</style>\n')
        
        logger.info("已创建 AboutView 组件")
    
    def _add_content_sections(self, file, html_analysis):
        """
        向视图添加内容区域
        
        根据分析的组件添加内容区域，如卡片、表单等。
        
        参数:
            file: 文件对象，用于写入内容
            html_analysis (dict): HTML分析结果
        """
        # 添加主标题
        file.write('        <h1>{{ title }}</h1>\n')
        
        # 添加卡片区域
        if any(c.get('type') == 'card' for c in html_analysis.get('components', [])):
            file.write('        <section class="card-container">\n')
            file.write('          <Card v-for="card in cards" :key="card.id"\n')
            file.write('                :title="card.title"\n')
            file.write('                :content="card.content"\n')
            file.write('                :image="card.image" />\n')
            file.write('        </section>\n')
        
        # 添加表格区域
        if any(c.get('type') == 'table' for c in html_analysis.get('components', [])):
            file.write('        <section class="table-section">\n')
            file.write('          <h2>数据表格</h2>\n')
            file.write('          <Table :headers="tableData.headers" :items="tableData.rows" />\n')
            file.write('        </section>\n')
    
    def _generate_router(self):
        """生成Vue路由配置"""
        logger.info("生成路由配置")
        
        router_dir = os.path.join(self.output_dir, 'src', 'router')
        router_path = os.path.join(router_dir, 'index.js')
        
        with open(router_path, 'w', encoding='utf-8') as f:
            f.write("import { createRouter, createWebHistory } from 'vue-router'\n")
            f.write("import Home from '../views/Home.vue'\n\n")
            
            f.write("const routes = [\n")
            f.write("  {\n")
            f.write("    path: '/',\n")
            f.write("    name: 'Home',\n")
            f.write("    component: Home\n")
            f.write("  },\n")
            f.write("  {\n")
            f.write("    path: '/about',\n")
            f.write("    name: 'About',\n")
            f.write("    // 路由级代码分割，生成分离的块\n")
            f.write("    component: () => import('../views/About.vue')\n")
            f.write("  }\n")
            f.write("]\n\n")
            
            f.write("const router = createRouter({\n")
            f.write("  history: createWebHistory(process.env.BASE_URL),\n")
            f.write("  routes\n")
            f.write("})\n\n")
            
            f.write("export default router\n")
        
        # 创建一个简单的About视图
        about_path = os.path.join(self.output_dir, 'src', 'views', 'About.vue')
        with open(about_path, 'w', encoding='utf-8') as f:
            f.write("<template>\n")
            f.write("  <div class=\"about\">\n")
            f.write("    <h1>About Page</h1>\n")
            f.write("    <p>This page was automatically generated by WebCloneAgent.</p>\n")
            f.write("  </div>\n")
            f.write("</template>\n")
    
    def _generate_store(self):
        """生成Vuex状态管理配置"""
        logger.info("生成状态管理配置")
        
        store_dir = os.path.join(self.output_dir, 'src', 'store')
        store_path = os.path.join(store_dir, 'index.js')
        
        with open(store_path, 'w', encoding='utf-8') as f:
            f.write("import { createStore } from 'vuex'\n\n")
            
            f.write("export default createStore({\n")
            f.write("  state: {\n")
            f.write("    // 全局状态\n")
            f.write("  },\n")
            f.write("  mutations: {\n")
            f.write("    // 修改状态的方法\n")
            f.write("  },\n")
            f.write("  actions: {\n")
            f.write("    // 异步操作\n")
            f.write("  },\n")
            f.write("  modules: {\n")
            f.write("    // 模块\n")
            f.write("  }\n")
            f.write("})\n")
    
    def _generate_main_files(self, page_meta):
        """
        生成Vue主文件
        
        Args:
            page_meta (dict): 页面元数据
        """
        logger.info("生成主文件")
        
        # 创建main.js
        main_path = os.path.join(self.output_dir, 'src', 'main.js')
        with open(main_path, 'w', encoding='utf-8') as f:
            f.write("import { createApp } from 'vue'\n")
            f.write("import App from './App.vue'\n")
            f.write("import router from './router'\n")
            f.write("import store from './store'\n")
            f.write("import './assets/styles/main.scss'\n\n")
            
            f.write("createApp(App).use(store).use(router).mount('#app')\n")
        
        # 创建App.vue
        app_path = os.path.join(self.output_dir, 'src', 'App.vue')
        with open(app_path, 'w', encoding='utf-8') as f:
            f.write("<template>\n")
            f.write("  <router-view/>\n")
            f.write("</template>\n\n")
            
            f.write("<style lang=\"scss\">\n")
            f.write("// 全局样式\n")
            f.write("body {\n")
            f.write("  margin: 0;\n")
            f.write("  font-family: Arial, sans-serif;\n")
            f.write("}\n")
            f.write("</style>\n")
        
        # 创建index.html
        index_path = os.path.join(self.output_dir, 'public', 'index.html')
        title = page_meta.get('title', 'Vue App')
        
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write("<!DOCTYPE html>\n")
            f.write("<html lang=\"en\">\n")
            f.write("<head>\n")
            f.write("  <meta charset=\"utf-8\">\n")
            f.write("  <meta http-equiv=\"X-UA-Compatible\" content=\"IE=edge\">\n")
            f.write("  <meta name=\"viewport\" content=\"width=device-width,initial-scale=1.0\">\n")
            f.write(f"  <title>{title}</title>\n")
            f.write("</head>\n")
            f.write("<body>\n")
            f.write("  <noscript>\n")
            f.write("    <strong>We're sorry but this app doesn't work properly without JavaScript enabled. Please enable it to continue.</strong>\n")
            f.write("  </noscript>\n")
            f.write("  <div id=\"app\"></div>\n")
            f.write("  <!-- built files will be auto injected -->\n")
            f.write("</body>\n")
            f.write("</html>\n")
    
    def _generate_config_files(self):
        """生成Vue项目配置文件"""
        logger.info("生成配置文件")
        
        # 创建package.json
        package_path = os.path.join(self.output_dir, 'package.json')
        with open(package_path, 'w', encoding='utf-8') as f:
            package_content = {
                "name": "web-clone",
                "version": "0.1.0",
                "private": True,
                "scripts": {
                    "serve": "vue-cli-service serve",
                    "build": "vue-cli-service build",
                    "lint": "vue-cli-service lint"
                },
                "dependencies": {
                    "core-js": "^3.8.3",
                    "vue": "^3.2.13",
                    "vue-router": "^4.0.3",
                    "vuex": "^4.0.0"
                },
                "devDependencies": {
                    "@vue/cli-plugin-babel": "~5.0.0",
                    "@vue/cli-plugin-router": "~5.0.0",
                    "@vue/cli-plugin-vuex": "~5.0.0",
                    "@vue/cli-service": "~5.0.0",
                    "sass": "^1.32.7",
                    "sass-loader": "^12.0.0"
                },
                "browserslist": [
                    "> 1%",
                    "last 2 versions",
                    "not dead",
                    "not ie 11"
                ]
            }
            
            json.dump(package_content, f, indent=2)
        
        # 创建README.md
        readme_path = os.path.join(self.output_dir, 'README.md')
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write("# Web Clone Vue Project\n\n")
            f.write("This project was automatically generated by WebCloneAgent.\n\n")
            
            f.write("## Project setup\n")
            f.write("```\n")
            f.write("npm install\n")
            f.write("```\n\n")
            
            f.write("### Compiles and hot-reloads for development\n")
            f.write("```\n")
            f.write("npm run serve\n")
            f.write("```\n\n")
            
            f.write("### Compiles and minifies for production\n")
            f.write("```\n")
            f.write("npm run build\n")
            f.write("```\n\n")
            
            f.write("### Customize configuration\n")
            f.write("See [Configuration Reference](https://cli.vuejs.org/config/).\n") 