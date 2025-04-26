# Web Clone Agent (网页克隆代理)

这是一个能够分析现有网页并生成对应Vue项目的工具。该工具可以深度复制网页的结构、样式和部分功能，帮助开发者快速创建与目标网页相似的Vue应用。

## 功能特点

- 自动抓取目标网页的HTML、CSS和JavaScript代码
- 分析网页结构并将其转换为Vue组件结构
- 提取网页样式并生成对应的CSS/SCSS文件
- 识别基本交互功能并尝试使用Vue实现
- 自动生成Vue项目脚手架，包括路由和状态管理配置

## 安装依赖

```bash
cd web-clone-agent
pip install -r requirements.txt
```

## 使用方法

```bash
python main.py --url https://example.com --output my-vue-project
```

参数说明：
- `--url`: 要克隆的目标网页URL
- `--output`: 生成的Vue项目路径

## 项目结构

- `main.py`: 主程序入口
- `web_scraper.py`: 网页抓取模块
- `html_analyzer.py`: HTML分析和Vue组件生成模块
- `style_extractor.py`: CSS样式提取和转换模块
- `vue_generator.py`: Vue项目生成模块
- `agent.py`: Agent代理核心逻辑 