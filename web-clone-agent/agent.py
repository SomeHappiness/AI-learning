#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
克隆代理核心模块
负责协调各个组件完成网页克隆任务
"""

import os
import logging
import time
from tqdm import tqdm
from colorama import Fore

# LangChain 导入
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

logger = logging.getLogger(__name__)

class CloneAgent:
    """网页克隆代理，协调各模块完成克隆任务"""
    
    def __init__(self, web_scraper, html_analyzer, style_extractor, vue_generator):
        """
        初始化克隆代理
        
        Args:
            web_scraper: WebScraper实例
            html_analyzer: HtmlAnalyzer实例
            style_extractor: StyleExtractor实例
            vue_generator: VueGenerator实例
        """
        self.web_scraper = web_scraper
        self.html_analyzer = html_analyzer
        self.style_extractor = style_extractor
        self.vue_generator = vue_generator
        
        # 初始化LLM，如果有API密钥
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key:
            self.llm = OpenAI(temperature=0.3)
            self.use_llm = True
        else:
            self.use_llm = False
            logger.warning("未找到OPENAI_API_KEY环境变量，将不使用LLM辅助")
    
    def clone_website(self, url, output_dir):
        """
        执行网页克隆流程
        
        Args:
            url (str): 目标网页URL
            output_dir (str): 输出目录
        
        Returns:
            bool: 克隆是否成功
        """
        try:
            # 步骤1: 抓取网页内容
            print(f"{Fore.CYAN}步骤1/5: 抓取网页内容 - {url}{Fore.RESET}")
            page_data = self.web_scraper.fetch_url(url)
            
            # 步骤2: 分析HTML结构
            print(f"{Fore.CYAN}步骤2/5: 分析HTML结构{Fore.RESET}")
            html_analysis = self.html_analyzer.analyze(page_data['html'])
            
            # 步骤3: 提取和处理样式
            print(f"{Fore.CYAN}步骤3/5: 提取样式信息{Fore.RESET}")
            style_analysis = self.style_extractor.extract_styles(
                page_data['css_files'],
                page_data['css_content'],
                page_data['html'],
                page_data['base_url']
            )
            
            # 提取颜色和字体
            color_analysis = self.style_extractor.extract_color_palette(page_data['css_content'])
            
            # 步骤4: 使用LLM增强分析（如果可用）
            if self.use_llm:
                print(f"{Fore.CYAN}步骤4/5: 使用AI增强分析{Fore.RESET}")
                try:
                    self._enhance_analysis_with_llm(html_analysis, style_analysis, page_data)
                except Exception as e:
                    logger.error(f"使用LLM增强分析时出错: {str(e)}")
                    print(f"{Fore.YELLOW}警告: AI增强分析失败，将使用基本分析结果继续。{Fore.RESET}")
            else:
                print(f"{Fore.YELLOW}跳过步骤4/5: 未配置OpenAI API密钥，无法使用AI增强分析{Fore.RESET}")
            
            # 步骤5: 生成Vue项目
            print(f"{Fore.CYAN}步骤5/5: 生成Vue项目{Fore.RESET}")
            success = self.vue_generator.generate_project(
                html_analysis,
                style_analysis,
                html_analysis['meta']
            )
            
            if success:
                print(f"\n{Fore.GREEN}✓ 完成! 已成功克隆网页并生成Vue项目。{Fore.RESET}")
                return True
            else:
                print(f"\n{Fore.RED}✗ 生成Vue项目失败。{Fore.RESET}")
                return False
            
        except Exception as e:
            logger.exception(f"克隆网页时出错: {str(e)}")
            print(f"\n{Fore.RED}✗ 克隆过程中出现错误: {str(e)}{Fore.RESET}")
            return False
        
        finally:
            # 清理资源
            if hasattr(self.web_scraper, 'close'):
                self.web_scraper.close()
    
    def _enhance_analysis_with_llm(self, html_analysis, style_analysis, page_data):
        """
        使用LLM增强分析结果
        
        Args:
            html_analysis (dict): HTML分析结果
            style_analysis (dict): 样式分析结果
            page_data (dict): 页面数据
        """
        if not self.use_llm:
            return
        
        logger.info("使用LLM增强分析")
        
        # 提取页面内容摘要
        page_content = page_data['html'][:5000]  # 只取前5000个字符作为摘要
        
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
        
        # 准备进度条
        print("使用AI分析组件...")
        components_str = str(html_analysis['components'])
        
        try:
            # 执行LLM链来分析组件
            component_chain = LLMChain(llm=self.llm, prompt=component_prompt)
            component_result = component_chain.run(
                page_content=page_content,
                components=components_str
            )
            
            # 解析结果（省略，实际实现中需要解析JSON并更新html_analysis）
            # 这里简单打印结果
            logger.debug(f"LLM组件分析结果: {component_result}")
            
            # 同样方式分析布局
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
            
            print("使用AI分析页面布局...")
            layout_chain = LLMChain(llm=self.llm, prompt=layout_prompt)
            layout_result = layout_chain.run(
                page_content=page_content,
                layout=str(html_analysis['layout'])
            )
            
            logger.debug(f"LLM布局分析结果: {layout_result}")
            
        except Exception as e:
            logger.error(f"LLM增强分析失败: {str(e)}")
            raise 