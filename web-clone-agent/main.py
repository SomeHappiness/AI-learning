#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Web Clone Agent主程序 - 网页克隆为Vue项目工具
作用：解析命令行参数并启动网页克隆过程

使用方法:
    python main.py --url https://example.com --output my-vue-project

可选参数:
    --url: 要克隆的目标网页URL（必需）
    --output: 生成的Vue项目路径（默认: vue-project）
    --use-selenium: 使用Selenium处理JS渲染的动态页面
    --debug: 启用调试模式，输出详细日志
    --no-cleanup: 完成后保留临时文件
"""

import os
import argparse
import logging
from colorama import init, Fore
from dotenv import load_dotenv

# 导入项目自定义模块
from web_scraper import WebScraper         # 网页抓取模块
from html_analyzer import HtmlAnalyzer     # HTML分析模块
from style_extractor import StyleExtractor # 样式提取模块
from vue_generator import VueGenerator     # Vue项目生成模块
from agent import CloneAgent               # 克隆代理核心模块

# 初始化colorama用于彩色终端输出
init()

# 配置日志系统
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("web_clone.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def setup_argparse():
    """
    设置命令行参数解析器
    返回：解析后的参数对象
    """
    # 创建参数解析器对象
    parser = argparse.ArgumentParser(
        description='Web Clone Agent - 将网页克隆为Vue项目',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter  # 显示默认值
    )
    
    # 添加命令行参数
    parser.add_argument('--url', 
                      type=str, 
                      required=True, 
                      help='目标网页URL（必需）')
    
    parser.add_argument('--output', 
                      type=str, 
                      default='vue-project', 
                      help='输出Vue项目的路径')
    
    parser.add_argument('--use-selenium', 
                      action='store_true', 
                      help='使用Selenium进行动态网页爬取（处理JS渲染的页面）')
    
    parser.add_argument('--debug', 
                      action='store_true', 
                      help='启用调试模式，输出详细日志')
    
    parser.add_argument('--no-cleanup', 
                      action='store_true', 
                      help='完成后保留临时文件')
    
    return parser.parse_args()

def main():
    """
    主函数 - 程序执行入口
    处理流程：
    1. 加载环境变量
    2. 解析命令行参数
    3. 初始化组件
    4. 创建克隆代理
    5. 执行克隆过程
    """
    # 1. 加载环境变量（用于OpenAI API等）
    load_dotenv()
    
    # 2. 解析命令行参数
    args = setup_argparse()
    
    # 设置日志级别
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("调试模式已启用")
    
    # 打印欢迎信息和参数
    print(f"{Fore.CYAN}========================================{Fore.RESET}")
    print(f"{Fore.GREEN}Web Clone Agent - 网页克隆为Vue项目{Fore.RESET}")
    print(f"{Fore.CYAN}========================================{Fore.RESET}")
    print(f"目标URL: {Fore.YELLOW}{args.url}{Fore.RESET}")
    print(f"输出路径: {Fore.YELLOW}{args.output}{Fore.RESET}")
    print(f"使用Selenium: {Fore.YELLOW}{args.use_selenium}{Fore.RESET}")
    print(f"{Fore.CYAN}========================================{Fore.RESET}\n")
    
    try:
        # 创建输出目录（如果不存在）
        os.makedirs(args.output, exist_ok=True)
        
        # 3. 初始化各个模块组件
        # 3.1 网页抓取模块 - 负责获取目标网页的HTML、CSS和JS
        web_scraper = WebScraper(use_selenium=args.use_selenium)
        
        # 3.2 HTML分析模块 - 分析网页结构
        html_analyzer = HtmlAnalyzer()
        
        # 3.3 样式提取模块 - 提取和处理CSS样式
        style_extractor = StyleExtractor()
        
        # 3.4 Vue项目生成模块 - 生成Vue组件和项目
        vue_generator = VueGenerator(output_dir=args.output)
        
        # 4. 创建并运行克隆代理 - 协调各模块完成克隆任务
        agent = CloneAgent(
            web_scraper=web_scraper,
            html_analyzer=html_analyzer,
            style_extractor=style_extractor,
            vue_generator=vue_generator
        )
        
        # 5. 执行克隆过程
        success = agent.clone_website(args.url, args.output)
        
        # 显示克隆结果
        if success:
            print(f"\n{Fore.GREEN}✓ 克隆成功!{Fore.RESET} Vue项目已生成在 {Fore.YELLOW}{os.path.abspath(args.output)}{Fore.RESET}")
            print(f"\n运行以下命令启动项目:")
            print(f"{Fore.CYAN}cd {args.output}{Fore.RESET}")
            print(f"{Fore.CYAN}npm install{Fore.RESET}")
            print(f"{Fore.CYAN}npm run serve{Fore.RESET}")
        else:
            print(f"\n{Fore.RED}✗ 克隆过程中出现错误。请查看日志获取详细信息。{Fore.RESET}")
    
    except Exception as e:
        # 捕获并记录所有未处理的异常
        logger.exception("克隆过程中出现未处理的异常:")
        print(f"\n{Fore.RED}错误: {str(e)}{Fore.RESET}")
        return 1
    
    return 0

# 程序入口点
if __name__ == "__main__":
    exit_code = main()
    exit(exit_code) 