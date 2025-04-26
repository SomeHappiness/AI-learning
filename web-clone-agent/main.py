#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Web Clone Agent主程序
用于解析命令行参数并启动克隆过程
"""

import os
import argparse
import logging
from colorama import init, Fore
from dotenv import load_dotenv

from web_scraper import WebScraper
from html_analyzer import HtmlAnalyzer
from style_extractor import StyleExtractor
from vue_generator import VueGenerator
from agent import CloneAgent

# 初始化colorama用于彩色终端输出
init()

# 配置日志
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
    """设置命令行参数解析"""
    parser = argparse.ArgumentParser(description='Web Clone Agent - 将网页克隆为Vue项目')
    parser.add_argument('--url', type=str, required=True, help='目标网页URL')
    parser.add_argument('--output', type=str, default='vue-project', help='输出Vue项目的路径')
    parser.add_argument('--use-selenium', action='store_true', help='使用Selenium进行动态网页爬取')
    parser.add_argument('--debug', action='store_true', help='启用调试模式')
    parser.add_argument('--no-cleanup', action='store_true', help='完成后不清理临时文件')
    return parser.parse_args()

def main():
    """主函数"""
    # 加载环境变量
    load_dotenv()
    
    # 解析命令行参数
    args = setup_argparse()
    
    # 设置日志级别
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("调试模式已启用")
    
    # 打印欢迎信息
    print(f"{Fore.CYAN}========================================{Fore.RESET}")
    print(f"{Fore.GREEN}Web Clone Agent - 网页克隆为Vue项目{Fore.RESET}")
    print(f"{Fore.CYAN}========================================{Fore.RESET}")
    print(f"目标URL: {Fore.YELLOW}{args.url}{Fore.RESET}")
    print(f"输出路径: {Fore.YELLOW}{args.output}{Fore.RESET}")
    print(f"使用Selenium: {Fore.YELLOW}{args.use_selenium}{Fore.RESET}")
    print(f"{Fore.CYAN}========================================{Fore.RESET}\n")
    
    try:
        # 创建输出目录
        os.makedirs(args.output, exist_ok=True)
        
        # 初始化组件
        web_scraper = WebScraper(use_selenium=args.use_selenium)
        html_analyzer = HtmlAnalyzer()
        style_extractor = StyleExtractor()
        vue_generator = VueGenerator(output_dir=args.output)
        
        # 创建并运行克隆代理
        agent = CloneAgent(
            web_scraper=web_scraper,
            html_analyzer=html_analyzer,
            style_extractor=style_extractor,
            vue_generator=vue_generator
        )
        
        # 执行克隆过程
        success = agent.clone_website(args.url, args.output)
        
        if success:
            print(f"\n{Fore.GREEN}✓ 克隆成功!{Fore.RESET} Vue项目已生成在 {Fore.YELLOW}{os.path.abspath(args.output)}{Fore.RESET}")
            print(f"\n运行以下命令启动项目:")
            print(f"{Fore.CYAN}cd {args.output}{Fore.RESET}")
            print(f"{Fore.CYAN}npm install{Fore.RESET}")
            print(f"{Fore.CYAN}npm run serve{Fore.RESET}")
        else:
            print(f"\n{Fore.RED}✗ 克隆过程中出现错误。请查看日志获取详细信息。{Fore.RESET}")
    
    except Exception as e:
        logger.exception("克隆过程中出现未处理的异常:")
        print(f"\n{Fore.RED}错误: {str(e)}{Fore.RESET}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    exit(exit_code) 