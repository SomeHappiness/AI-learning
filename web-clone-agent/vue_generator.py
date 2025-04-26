#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Vue项目生成器模块
负责生成Vue项目的各个组件和配置文件
"""

import os
import re
import json
import shutil
import logging
import jsbeautifier
from tqdm import tqdm

logger = logging.getLogger(__name__)

class VueGenerator:
    """Vue项目生成器类，用于生成Vue项目结构和文件"""
    
    def __init__(self, output_dir="vue-project"):
        """
        初始化Vue项目生成器
        
        Args:
            output_dir (str): 输出目录
        """
        self.output_dir = output_dir
        
        # JS格式化选项
        self.js_options = jsbeautifier.default_options()
        self.js_options.indent_size = 2
    
    def generate_project(self, html_analysis, style_analysis, page_meta):
        """
        生成完整的Vue项目
        
        Args:
            html_analysis (dict): HTML分析结果
            style_analysis (dict): 样式分析结果
            page_meta (dict): 页面元数据
        
        Returns:
            bool: 生成是否成功
        """
        logger.info(f"开始生成Vue项目到 {self.output_dir}")
        
        try:
            # 创建项目目录结构
            self._create_project_structure()
            
            # 生成组件
            self._generate_components(html_analysis, style_analysis)
            
            # 生成视图
            self._generate_views(html_analysis, style_analysis, page_meta)
            
            # 生成路由
            self._generate_router()
            
            # 生成状态管理
            self._generate_store()
            
            # 生成主文件
            self._generate_main_files(page_meta)
            
            # 生成配置文件
            self._generate_config_files()
            
            # 复制样式文件
            if os.path.exists(os.path.join("output", "styles")):
                shutil.copytree(
                    os.path.join("output", "styles"),
                    os.path.join(self.output_dir, "src", "assets", "styles"),
                    dirs_exist_ok=True
                )
            
            logger.info("Vue项目生成成功")
            return True
        
        except Exception as e:
            logger.error(f"生成Vue项目时出错: {str(e)}")
            return False
    
    def _create_project_structure(self):
        """创建Vue项目目录结构"""
        logger.info("创建项目目录结构")
        
        # 创建主要目录
        dirs = [
            '',  # 项目根目录
            'public',
            'src',
            'src/assets',
            'src/assets/images',
            'src/assets/styles',
            'src/components',
            'src/views',
            'src/router',
            'src/store',
            'src/utils'
        ]
        
        for d in dirs:
            os.makedirs(os.path.join(self.output_dir, d), exist_ok=True)
    
    def _generate_components(self, html_analysis, style_analysis):
        """
        生成Vue组件
        
        Args:
            html_analysis (dict): HTML分析结果
            style_analysis (dict): 样式分析结果
        """
        logger.info("生成Vue组件")
        
        # 生成Header组件
        if html_analysis['layout']['header']:
            self._create_component(
                'Header',
                html_analysis['layout']['header']['element'],
                style_analysis,
                'layout'
            )
        
        # 生成Footer组件
        if html_analysis['layout']['footer']:
            self._create_component(
                'Footer',
                html_analysis['layout']['footer']['element'],
                style_analysis,
                'layout'
            )
        
        # 生成Sidebar组件
        if html_analysis['layout']['sidebar']:
            self._create_component(
                'Sidebar',
                html_analysis['layout']['sidebar']['element'],
                style_analysis,
                'layout'
            )
        
        # 生成识别出的组件
        for component in html_analysis['components']:
            component_name = component['type'].capitalize()
            if component_name.lower() in ['card', 'navigation', 'form', 'table']:
                self._create_component(
                    component_name,
                    component['sample'],
                    style_analysis,
                    component_name.lower()
                )
    
    def _create_component(self, name, html_content, style_analysis, component_type):
        """
        创建单个Vue组件
        
        Args:
            name (str): 组件名称
            html_content (str): HTML内容
            style_analysis (dict): 样式分析结果
            component_type (str): 组件类型
        """
        # 格式化组件名称为PascalCase
        formatted_name = ''.join(word.capitalize() for word in re.split(r'[-_\s]', name))
        file_path = os.path.join(self.output_dir, 'src', 'components', f'{formatted_name}.vue')
        
        # 简化HTML内容
        html_content = self._simplify_html(html_content)
        
        # 创建Vue组件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('<template>\n')
            f.write(f'  <div class="v-{component_type.lower()}">\n')
            
            # 去除无效的HTML标签和属性
            cleaned_html = self._clean_html_for_vue(html_content)
            indented_html = '\n'.join(f'    {line}' for line in cleaned_html.split('\n'))
            f.write(indented_html)
            
            f.write('\n  </div>\n')
            f.write('</template>\n\n')
            
            f.write('<script>\nexport default {\n')
            f.write('  name: \'' + formatted_name + '\',\n')
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
            else:
                f.write('    // 自定义props\n')
            
            f.write('  },\n')
            f.write('  data() {\n    return {\n      // 组件数据\n    }\n  },\n')
            f.write('  methods: {\n    // 组件方法\n  }\n')
            f.write('}\n</script>\n\n')
            
            f.write('<style lang="scss" scoped>\n')
            f.write(f'@import "@/assets/styles/{component_type.lower()}.scss";\n')
            
            # 添加特定于组件的样式
            f.write('\n// 组件特定样式\n')
            f.write(f'.v-{component_type.lower()} {{\n  // 自定义样式\n}}\n')
            
            f.write('</style>\n')
        
        logger.info(f"已创建组件: {formatted_name}")
            
    def _clean_html_for_vue(self, html_content):
        """
        清理HTML使其适合Vue模板
        
        Args:
            html_content (str): 原始HTML内容
        
        Returns:
            str: 清理后的HTML
        """
        # 替换HTML特性为Vue特性
        replacements = {
            'class=': ':class=',
            'onclick=': '@click=',
            'onchange=': '@change=',
            'onsubmit=': '@submit=',
            'href=': ':to=',
            '<a ': '<router-link ',
            '</a>': '</router-link>'
        }
        
        result = html_content
        for old, new in replacements.items():
            result = result.replace(old, new)
        
        # 移除脚本和样式标签
        result = re.sub(r'<script.*?</script>', '', result, flags=re.DOTALL)
        result = re.sub(r'<style.*?</style>', '', result, flags=re.DOTALL)
        
        return result
    
    def _simplify_html(self, html_content):
        """
        简化HTML内容
        
        Args:
            html_content (str): 原始HTML内容
        
        Returns:
            str: 简化后的HTML
        """
        # 移除注释
        html_content = re.sub(r'<!--.*?-->', '', html_content, flags=re.DOTALL)
        
        # 移除DOCTYPE、html、head和body标签
        html_content = re.sub(r'<!DOCTYPE.*?>', '', html_content, flags=re.IGNORECASE)
        html_content = re.sub(r'<html.*?>|</html>', '', html_content, flags=re.IGNORECASE)
        html_content = re.sub(r'<head.*?>.*?</head>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
        html_content = re.sub(r'<body.*?>|</body>', '', html_content, flags=re.IGNORECASE)
        
        return html_content
    
    def _generate_views(self, html_analysis, style_analysis, page_meta):
        """
        生成Vue视图
        
        Args:
            html_analysis (dict): HTML分析结果
            style_analysis (dict): 样式分析结果
            page_meta (dict): 页面元数据
        """
        logger.info("生成Vue视图")
        
        # 创建Home.vue视图
        home_path = os.path.join(self.output_dir, 'src', 'views', 'Home.vue')
        
        with open(home_path, 'w', encoding='utf-8') as f:
            f.write('<template>\n')
            f.write('  <div class="home">\n')
            
            # 添加布局组件
            if html_analysis['layout']['header']:
                f.write('    <Header />\n')
            
            if html_analysis['layout']['sidebar']:
                sidebar_position = html_analysis['layout']['sidebar'].get('position', 'left')
                f.write(f'    <div class="content-with-sidebar {sidebar_position}-sidebar">\n')
                f.write('      <Sidebar />\n')
                f.write('      <main class="main-content">\n')
                
                # 添加主要内容
                self._add_content_sections(f, html_analysis)
                
                f.write('      </main>\n')
                f.write('    </div>\n')
            else:
                f.write('    <main class="main-content">\n')
                
                # 添加主要内容
                self._add_content_sections(f, html_analysis)
                
                f.write('    </main>\n')
            
            if html_analysis['layout']['footer']:
                f.write('    <Footer />\n')
            
            f.write('  </div>\n')
            f.write('</template>\n\n')
            
            # 添加脚本部分
            f.write('<script>\n')
            
            # 导入组件
            f.write('// 导入组件\n')
            if html_analysis['layout']['header']:
                f.write("import Header from '@/components/Header.vue'\n")
            if html_analysis['layout']['footer']:
                f.write("import Footer from '@/components/Footer.vue'\n")
            if html_analysis['layout']['sidebar']:
                f.write("import Sidebar from '@/components/Sidebar.vue'\n")
            
            # 导入内容组件
            component_imports = set()
            for component in html_analysis['components']:
                if component['type'].lower() in ['card', 'navigation', 'form', 'table']:
                    component_name = component['type'].capitalize()
                    formatted_name = ''.join(word.capitalize() for word in re.split(r'[-_\s]', component_name))
                    component_imports.add(f"import {formatted_name} from '@/components/{formatted_name}.vue'")
            
            for import_stmt in component_imports:
                f.write(f"{import_stmt}\n")
            
            # 组件导出
            f.write('\nexport default {\n')
            f.write(f"  name: 'Home',\n")
            f.write('  components: {\n')
            
            if html_analysis['layout']['header']:
                f.write('    Header,\n')
            if html_analysis['layout']['footer']:
                f.write('    Footer,\n')
            if html_analysis['layout']['sidebar']:
                f.write('    Sidebar,\n')
            
            # 添加内容组件
            for component in html_analysis['components']:
                if component['type'].lower() in ['card', 'navigation', 'form', 'table']:
                    component_name = component['type'].capitalize()
                    formatted_name = ''.join(word.capitalize() for word in re.split(r'[-_\s]', component_name))
                    f.write(f'    {formatted_name},\n')
            
            f.write('  },\n')
            
            # 数据部分
            f.write('  data() {\n')
            f.write('    return {\n')
            f.write('      title: ' + json.dumps(page_meta.get('title', 'Home Page')) + ',\n')
            
            # 为Card组件生成示例数据
            if any(c['type'] == 'card' for c in html_analysis['components']):
                f.write('      cards: [\n')
                f.write('        { id: 1, title: "Card 1", content: "Card 1 content", image: "" },\n')
                f.write('        { id: 2, title: "Card 2", content: "Card 2 content", image: "" },\n')
                f.write('        { id: 3, title: "Card 3", content: "Card 3 content", image: "" }\n')
                f.write('      ],\n')
            
            # 为Table组件生成示例数据
            if any(c['type'] == 'table' for c in html_analysis['components']):
                f.write('      tableHeaders: ["ID", "Name", "Email", "Status"],\n')
                f.write('      tableItems: [\n')
                f.write('        { id: 1, name: "User 1", email: "user1@example.com", status: "Active" },\n')
                f.write('        { id: 2, name: "User 2", email: "user2@example.com", status: "Inactive" },\n')
                f.write('        { id: 3, name: "User 3", email: "user3@example.com", status: "Active" }\n')
                f.write('      ],\n')
            
            f.write('    }\n')
            f.write('  }\n')
            f.write('}\n')
            f.write('</script>\n\n')
            
            # 添加样式部分
            f.write('<style lang="scss">\n')
            f.write('@import "@/assets/styles/main.scss";\n\n')
            
            # 添加页面特定样式
            f.write('.home {\n')
            f.write('  display: flex;\n')
            f.write('  flex-direction: column;\n')
            f.write('  min-height: 100vh;\n')
            f.write('}\n\n')
            
            f.write('.content-with-sidebar {\n')
            f.write('  display: flex;\n')
            f.write('  flex: 1;\n')
            f.write('}\n\n')
            
            f.write('.left-sidebar {\n')
            f.write('  flex-direction: row;\n')
            f.write('}\n\n')
            
            f.write('.right-sidebar {\n')
            f.write('  flex-direction: row-reverse;\n')
            f.write('}\n\n')
            
            f.write('.main-content {\n')
            f.write('  flex: 1;\n')
            f.write('  padding: 1rem;\n')
            f.write('}\n')
            
            f.write('</style>\n')
        
        logger.info("已创建Home视图")
    
    def _add_content_sections(self, file, html_analysis):
        """
        添加内容部分到视图
        
        Args:
            file: 文件对象
            html_analysis (dict): HTML分析结果
        """
        # 添加卡片组件
        card_components = [c for c in html_analysis['components'] if c['type'] == 'card']
        if card_components:
            file.write('        <h2>Featured Items</h2>\n')
            file.write('        <div class="card-container">\n')
            file.write('          <Card v-for="card in cards" :key="card.id" :title="card.title" :content="card.content" :image="card.image" />\n')
            file.write('        </div>\n')
        
        # 添加表格组件
        table_components = [c for c in html_analysis['components'] if c['type'] == 'table']
        if table_components:
            file.write('        <h2>Data Table</h2>\n')
            file.write('        <Table :headers="tableHeaders" :items="tableItems" />\n')
        
        # 添加表单组件
        form_components = [c for c in html_analysis['components'] if c['type'] == 'form']
        if form_components:
            file.write('        <h2>Contact Form</h2>\n')
            file.write('        <Form />\n')
    
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