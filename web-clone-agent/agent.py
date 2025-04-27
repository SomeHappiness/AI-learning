#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
克隆代理核心模块 (agent.py)
------------------------
这个模块是整个Web Clone Agent的核心，负责协调各个组件完成网页克隆任务。

主要功能:
1. 协调网页抓取、HTML分析、样式提取和Vue项目生成等模块
2. 按步骤执行克隆流程
3. 可选地使用OpenAI API进行增强分析

工作流程:
1. 抓取网页内容
2. 分析HTML结构
3. 提取和处理样式
4. (可选)使用AI增强分析
5. 生成Vue项目
"""

import os
import logging
import time
from tqdm import tqdm
from colorama import Fore

# LangChain相关导入，用于AI增强功能
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 配置日志
logger = logging.getLogger(__name__)

class CloneAgent:
    """
    网页克隆代理类，负责协调各模块完成克隆任务
    
    这个类是整个系统的"大脑"，控制各个组件按顺序执行，
    并处理它们之间的数据传递。
    """
    
    def __init__(self, web_scraper, html_analyzer, style_extractor, vue_generator):
        """
        初始化克隆代理
        
        参数:
            web_scraper (WebScraper): 网页抓取器实例
            html_analyzer (HtmlAnalyzer): HTML分析器实例
            style_extractor (StyleExtractor): 样式提取器实例
            vue_generator (VueGenerator): Vue项目生成器实例
        """
        # 保存各个组件
        self.web_scraper = web_scraper
        self.html_analyzer = html_analyzer
        self.style_extractor = style_extractor
        self.vue_generator = vue_generator
        
        # 检查并初始化OpenAI功能（如果有API密钥）
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key:
            self.llm = OpenAI(temperature=0.3)
            self.use_llm = True
            logger.info("已成功配置OpenAI API，将使用AI辅助分析功能")
        else:
            self.use_llm = False
            logger.warning("未找到OPENAI_API_KEY环境变量，将不使用AI辅助分析")
    
    def clone_website(self, url, output_dir):
        """
        执行网页克隆的完整流程
        
        参数:
            url (str): 目标网页URL
            output_dir (str): 输出目录路径
        
        返回:
            bool: 克隆是否成功
        """
        try:
            # === 步骤1: 抓取网页内容 ===
            print(f"{Fore.CYAN}步骤1/5: 抓取网页内容 - {url}{Fore.RESET}")
            page_data = self.web_scraper.fetch_url(url)
            
            # === 步骤2: 分析HTML结构 ===
            print(f"{Fore.CYAN}步骤2/5: 分析HTML结构{Fore.RESET}")
            html_analysis = self.html_analyzer.analyze(page_data['html'])
            
            # === 步骤3: 提取和处理样式 ===
            print(f"{Fore.CYAN}步骤3/5: 提取样式信息{Fore.RESET}")
            # 提取CSS样式
            style_analysis = self.style_extractor.extract_styles(
                page_data['css_files'],
                page_data['css_content'],
                page_data['html'],
                page_data['base_url']
            )
            
            # 提取颜色方案和字体
            color_analysis = self.style_extractor.extract_color_palette(page_data['css_content'])
            
            # === 步骤4: 使用AI增强分析(如果可用) ===
            if self.use_llm:
                print(f"{Fore.CYAN}步骤4/5: 使用AI增强分析{Fore.RESET}")
                try:
                    self._enhance_analysis_with_llm(html_analysis, style_analysis, page_data)
                except Exception as e:
                    logger.error(f"使用AI增强分析时出错: {str(e)}")
                    print(f"{Fore.YELLOW}警告: AI增强分析失败，将使用基本分析结果继续。{Fore.RESET}")
            else:
                print(f"{Fore.YELLOW}跳过步骤4/5: 未配置OpenAI API密钥，无法使用AI增强分析{Fore.RESET}")
            
            # === 步骤5: 生成Vue项目 ===
            print(f"{Fore.CYAN}步骤5/5: 生成Vue项目{Fore.RESET}")
            success = self.vue_generator.generate_project(
                html_analysis,
                style_analysis,
                html_analysis['meta']
            )
            
            # 显示最终结果
            if success:
                print(f"\n{Fore.GREEN}✓ 完成! 已成功克隆网页并生成Vue项目。{Fore.RESET}")
                return True
            else:
                print(f"\n{Fore.RED}✗ 生成Vue项目失败。{Fore.RESET}")
                return False
            
        except Exception as e:
            # 捕获并记录所有未处理的异常
            logger.exception(f"克隆网页时出错: {str(e)}")
            print(f"\n{Fore.RED}✗ 克隆过程中出现错误: {str(e)}{Fore.RESET}")
            return False
        
        finally:
            # 确保清理资源（例如关闭Selenium浏览器）
            if hasattr(self.web_scraper, 'close'):
                self.web_scraper.close()
    
    def _enhance_analysis_with_llm(self, html_analysis, style_analysis, page_data):
        """
        使用OpenAI LLM增强分析结果
        
        这个方法使用AI来改进组件识别和布局分析，
        使生成的Vue项目更符合人类的理解方式。
        
        参数:
            html_analysis (dict): HTML分析结果
            style_analysis (dict): 样式分析结果
            page_data (dict): 页面数据
        """
        if not self.use_llm:
            return
        
        logger.info("使用AI增强分析")
        
        # 提取页面内容摘要(为了避免超出token限制，只取前5000字符)
        page_content = page_data['html'][:5000]  # 只取前5000个字符作为摘要
        
        # === 1. 增强组件分析 ===
        
        # 准备组件分析提示
        component_prompt = PromptTemplate(
            input_variables=["page_content", "components"],
            template="""
            分析以下网页内容和已识别的组件，提供更好的组件分类：
            
            网页内容摘要:
            {page_content}
            
            已识别的组件:
            {components}
            
            请对上述组件进行改进，给出以下信息:
            1. 每个组件的改进名称（使用语义化名称）
            2. 组件的主要作用
            3. 组件中可能的交互功能
            
            以JSON格式回答:
            ```json
            [
              {{
                "original_type": "组件原始类型",
                "improved_name": "改进的语义化名称",
                "purpose": "组件目的",
                "interactions": ["可能的交互1", "可能的交互2"]
              }}
            ]
            ```
            只返回JSON，不要有其他内容。
            """
        )
        
        # 显示进度信息
        print("使用AI分析组件...")
        components_str = str(html_analysis['components'])
        
        try:
            # 执行LLM链来分析组件
            component_chain = LLMChain(llm=self.llm, prompt=component_prompt)
            component_result = component_chain.run(
                page_content=page_content,
                components=components_str
            )
            
            # 解析结果（实际实现中需要解析JSON并更新html_analysis）
            # 这里简单记录结果
            logger.debug(f"AI组件分析结果: {component_result}")
            
            # === 2. 增强布局分析 ===
            
            # 准备布局分析提示
            layout_prompt = PromptTemplate(
                input_variables=["page_content", "layout"],
                template="""
                分析以下网页内容和已识别的布局，提供更好的布局分析：
                
                网页内容摘要:
                {page_content}
                
                已识别的布局:
                {layout}
                
                请分析这个布局，给出:
                1. 布局类型名称（如 landing-page, blog, e-commerce, dashboard 等）
                2. 布局主要部分及其作用
                3. 推荐的Vue组件结构
                
                以简洁描述回答，不要冗长。
                """
            )
            
            # 显示进度信息
            print("使用AI分析页面布局...")
            layout_chain = LLMChain(llm=self.llm, prompt=layout_prompt)
            layout_result = layout_chain.run(
                page_content=page_content,
                layout=str(html_analysis['layout'])
            )
            
            # 记录布局分析结果
            logger.debug(f"AI布局分析结果: {layout_result}")
            
        except Exception as e:
            logger.error(f"AI增强分析失败: {str(e)}")
            raise 