人工智能学习空间
# 人工智能学习空间

## 项目简介
这是一个专注于人工智能技术学习和实践的项目空间，包含多个子项目和实践案例。本仓库涵盖了从基础机器学习到高级AI应用的多个领域，旨在提供一个完整的AI学习路径。

## 目录结构
```
AI-learning/
├── agent_interview_prep/       # AI Agent开发工程师面试准备材料
├── machine-learning/           # 机器学习相关项目
│   ├── lesson1/               # 第一课：基础概念和实现
│   └── lesson2/               # 第二课：进阶算法
├── web-clone-agent/           # 网页克隆AI代理项目
│   ├── agent.py              # 主要代理逻辑
│   ├── html_analyzer.py      # HTML分析器
│   ├── style_extractor.py    # 样式提取器
│   ├── vue_generator.py      # Vue代码生成器
│   ├── web_scraper.py        # 网页抓取工具
│   └── requirements.txt      # 项目依赖
└── tests/                     # 测试代码目录
    └── web-clone-agent/      # 网页克隆项目测试
        ├── root_test_*.py    # 根目录测试文件
        └── agent_test_*.py   # 代理相关测试文件

```

## 项目模块说明

### 1. Web Clone Agent (网页克隆代理)
- 功能：自动分析和克隆网页结构，生成对应的Vue组件
- 主要特点：
  - 智能HTML结构分析
  - CSS样式提取和优化
  - Vue组件自动生成
  - 支持动态内容处理

### 2. Machine Learning (机器学习)
- 包含基础算法实现和实践案例
- 课程进度：
  - Lesson 1: 基础概念和算法实现
  - Lesson 2: 进阶算法和实际应用

### 3. Agent Interview Prep (AI代理开发面试准备)
- 面试题集合和答案
- 包含：
  - Python基础知识
  - LLM和Prompt工程
  - 代理开发实践
  - 系统设计案例

## 环境要求
- Python 3.8+
- 相关依赖请参考各子项目中的requirements.txt

## 使用说明
1. 克隆仓库
```bash
git clone https://github.com/SomeHappiness/AI-learning.git
```

2. 安装依赖
```bash
cd AI-learning
pip install -r web-clone-agent/requirements.txt  # 安装网页克隆代理依赖
```

3. 运行测试
```bash
# 运行网页克隆代理测试
python -m pytest tests/web-clone-agent/
```

## 贡献指南
- 欢迎提交Issue和Pull Request
- 请确保提交前已运行测试并通过
- 新功能请添加对应的测试用例

## 许可证
MIT License

## 联系方式
- GitHub: [SomeHappiness](https://github.com/SomeHappiness)
