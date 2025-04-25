#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试WebScraper功能的脚本
"""

import os
import sys
from web_scraper import WebScraper

def main():
    """
    主函数，测试WebScraper的基本功能
    """
    # 创建一个输出目录用于保存网页
    output_dir = "test_output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    print("初始化WebScraper...")
    # 初始化WebScraper，不使用Selenium，改用requests
    scraper = WebScraper(
        use_selenium=False,  # 不使用Selenium，避免版本不匹配问题
        wait_time=5,        # 网页加载等待时间（秒）
        temp_dir="temp"     # 临时文件目录
    )
    
    try:
        # 测试访问一个简单的网站
        url = "https://www.baidu.com"
        print(f"正在获取网页: {url}")
        
        # 使用WebScraper获取页面
        result = scraper.fetch_url(url)
        
        # 保存主HTML文件
        index_path = os.path.join(output_dir, "index.html")
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(result['html'])
        
        print(f"已保存HTML到: {index_path}")
        print(f"找到 {len(result['css_files']) + len(result['js_files'])} 个资源文件")
        
        # 显示CSS文件
        for i, css_file in enumerate(result['css_files']):
            if i < 3:  # 只显示前3个资源
                print(f"CSS 文件 {i+1}: {css_file}")
            
        # 显示JS文件
        for i, js_file in enumerate(result['js_files']):
            if i < 3:  # 只显示前3个资源
                print(f"JS 文件 {i+1}: {js_file}")
                
        # 显示图片文件
        for i, img_url in enumerate(result['images']):
            if i < 3:  # 只显示前3个图片
                print(f"图片 {i+1}: {img_url}")
                
        print("测试完成!")
        
    except Exception as e:
        print(f"测试过程中出错: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # 关闭WebScraper（清理资源）
        scraper.close()

if __name__ == "__main__":
    main() 