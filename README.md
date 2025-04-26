# 人工智能学习空间

## 项目简介
这是一个专注于人工智能技术学习和实践的项目空间，包含多个子项目和实践案例。本仓库涵盖了从基础机器学习到高级AI应用的多个领域，旨在提供一个完整的AI学习路径。

## 目录结构
```
AI-learning/
├── web-clone-agent/           # 网页克隆AI代理项目
│   ├── agent.py              # 主要代理逻辑
│   ├── html_analyzer.py      # HTML分析器
│   ├── style_extractor.py    # 样式提取器
│   ├── vue_generator.py      # Vue代码生成器
│   ├── web_scraper.py        # 网页抓取工具
│   ├── main.py              # 主程序入口
│   ├── requirements.txt      # 项目依赖
│   ├── env_example.txt      # 环境变量示例
│   ├── test/                # 单元测试目录
│   ├── test_output/         # 测试输出目录
│   └── temp/                # 临时文件目录
├── machine-learning/         # 机器学习课程实践
│   ├── lession1/            # 第一课：基础概念和实现
│   ├── lession2/            # 第二课：进阶算法
│   └── lession8/            # 第八课：高级应用
└── agent_interview_prep/     # AI代理开发面试准备
    ├── interview_questions.md    # 面试问题集
    ├── technical_concepts.md     # 技术概念详解
    ├── langchain_interview_questions.md  # LangChain相关面试题
    └── README.md                 # 面试准备指南
```

## 项目模块说明

### 1. Web Clone Agent (网页克隆代理)
- 功能：自动分析和克隆网页结构，生成对应的Vue组件
- 主要特点：
  - 智能HTML结构分析
  - CSS样式提取和优化
  - Vue组件自动生成
  - 支持动态内容处理
- 核心组件：
  - `agent.py`: 智能代理核心逻辑
  - `html_analyzer.py`: HTML结构分析器
  - `style_extractor.py`: CSS样式提取器
  - `vue_generator.py`: Vue组件生成器
  - `web_scraper.py`: 网页内容抓取器

### 2. Machine Learning (机器学习)
- 课程实践项目集合
- 课程进度：
  - Lesson 1: 机器学习基础和算法实现
  - Lesson 2: 进阶算法和模型优化
  - Lesson 8: 高级应用实践

### 3. Agent Interview Prep (AI代理开发面试准备)
- 完整的面试资料集合：
  - 常见面试问题和答案
  - 核心技术概念解析
  - LangChain专题面试题
  - 详细的准备指南

## 环境要求
- Python 3.8+
- Node.js 14+ (用于Vue组件生成)
- Chrome/Firefox (用于网页克隆)
- 其他依赖详见各项目的requirements.txt

## 快速开始

### Web Clone Agent
```bash
# 安装依赖
cd web-clone-agent
pip install -r requirements.txt

# 设置环境变量
cp env_example.txt .env
# 编辑.env文件，填入必要的配置

# 运行测试
python -m pytest test/

# 启动程序
python main.py
```

### Machine Learning 课程
```bash
# 进入对应课程目录
cd machine-learning/lession1

# 运行示例代码
python main.py
```

## 开发指南
1. 克隆仓库
```bash
git clone https://github.com/SomeHappiness/AI-learning.git
cd AI-learning
```

2. 创建并激活虚拟环境
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

3. 安装开发依赖
```bash
pip install -r web-clone-agent/requirements.txt
```

## 贡献指南
- 欢迎提交Issue和Pull Request
- 请确保提交前已运行测试并通过
- 新功能请添加对应的测试用例
- 保持代码风格一致性

## 许可证
MIT License

## 联系方式
- GitHub: [SomeHappiness](https://github.com/SomeHappiness)
- 欢迎通过Issue或Discussion进行交流
