# Web Clone Agent (网页克隆代理)

这是一个能够分析现有网页并生成对应Vue项目的工具。该工具可以深度复制网页的结构、样式和部分功能，帮助开发者快速创建与目标网页相似的Vue应用。

## 功能特点

- 自动抓取目标网页的HTML、CSS和JavaScript代码
- 分析网页结构并将其转换为Vue组件结构
- 提取网页样式并生成对应的CSS/SCSS文件
- 识别基本交互功能并尝试使用Vue实现
- 自动生成Vue项目脚手架，包括路由和状态管理配置

## 安装步骤

1. 确保已安装Python 3.6+
2. 克隆此仓库到本地
3. 安装依赖包：

```bash
cd web-clone-agent
pip install -r requirements.txt
```

## 使用方法

### 基本用法

克隆一个网页并生成Vue项目：

```bash
python main.py --url https://example.com --output my-vue-project
```

### 参数说明

- `--url`: 要克隆的目标网页URL（必须）
- `--output`: 生成的Vue项目路径（默认：vue-project）
- `--use-selenium`: 使用Selenium进行动态网页爬取（处理JavaScript渲染的页面）
- `--debug`: 启用调试模式，输出更详细的日志
- `--no-cleanup`: 完成后不清理临时文件

### 实际示例

```bash
# 克隆百度首页
python main.py --url https://www.baidu.com --output baidu-clone

# 克隆动态渲染的页面
python main.py --url https://vuejs.org --output vue-site-clone --use-selenium
```

## 项目结构说明

```
web-clone-agent/
├── main.py              # 主程序入口，处理命令行参数
├── agent.py             # 核心代理，协调各组件完成克隆任务
├── web_scraper.py       # 网页抓取模块，获取HTML/CSS/JS
├── html_analyzer.py     # HTML分析器，解析网页结构
├── style_extractor.py   # 样式提取器，分析CSS样式
├── vue_generator.py     # Vue项目生成器，创建Vue组件和项目
├── requirements.txt     # 项目依赖列表
├── env_example.txt      # 环境变量示例文件
└── test/                # 测试目录
    ├── agent_test_simple.py    # 简化版测试脚本
    ├── agent_test_scraper.py   # 网页抓取测试脚本
    └── web_scraper.py          # 独立测试用的抓取脚本
```

## 详细模块说明

### 1. 主程序 (main.py)
程序入口，解析命令行参数并启动克隆过程。

### 2. 克隆代理 (agent.py)
核心协调模块，管理整个克隆流程，调用其他模块完成克隆任务。如果配置了OpenAI API，还可以使用AI辅助分析。

### 3. 网页抓取器 (web_scraper.py)
负责获取目标网页的HTML、CSS和JavaScript代码。支持两种模式：
- 普通模式：使用requests库抓取静态内容
- Selenium模式：可以处理动态渲染的JavaScript页面

### 4. HTML分析器 (html_analyzer.py)
分析网页HTML结构，识别页面组件和布局，为Vue组件生成做准备。

### 5. 样式提取器 (style_extractor.py)
提取和分析CSS样式，包括颜色方案、字体、布局等，转换为Vue组件可用的样式。

### 6. Vue生成器 (vue_generator.py)
根据分析结果生成完整的Vue项目，包括组件、路由和样式文件。

## 小白使用指南

如果你是第一次使用这个工具，请按照以下步骤操作：

1. 安装Python（如果没有）
2. 下载本项目并解压
3. 打开命令行，进入项目目录
4. 运行 `pip install -r requirements.txt` 安装依赖
5. 运行 `python main.py --url 你想克隆的网址 --output 输出目录名`
6. 等待程序完成，然后在输出目录中找到生成的Vue项目

## 常见问题

**Q: 为什么有些网页无法正确克隆？**  
A: 复杂的动态网页可能需要使用 `--use-selenium` 参数。有些网站可能有反爬虫措施。

**Q: 生成的Vue项目不完整怎么办？**  
A: 当前版本主要关注UI克隆，复杂的交互功能需要手动补充。

**Q: 如何使用AI增强功能？**  
A: 创建一个.env文件，添加你的OpenAI API密钥：`OPENAI_API_KEY=你的密钥`

## 许可证

MIT 