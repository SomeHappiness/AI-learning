#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
简化版的网页抓取测试脚本
"""

import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def main():
    """
    主函数，使用requests抓取网页
    """
    # 创建一个输出目录用于保存网页
    output_dir = "test_output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    print("开始抓取网页...")
    
    try:
        # 测试访问一个简单的网站
        url = "https://www.baidu.com"
        print(f"正在获取网页: {url}")
        
        # 使用requests获取页面
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # 获取HTML内容
        html_content = response.text
        
        # 解析页面
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 保存主HTML文件
        index_path = os.path.join(output_dir, "index.html")
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        print(f"已保存HTML到: {index_path}")
        
        # 提取CSS文件
        css_links = soup.find_all('link', rel='stylesheet')
        print(f"找到 {len(css_links)} 个CSS文件")
        
        # 提取JavaScript文件
        js_tags = soup.find_all('script', src=True)
        print(f"找到 {len(js_tags)} 个JavaScript文件")
        
        # 提取图片
        img_tags = soup.find_all('img')
        print(f"找到 {len(img_tags)} 个图片")
        
        # 显示一些资源信息
        print("\n资源列表:")
        
        # 显示CSS文件
        for i, link in enumerate(css_links):
            if i < 3 and link.get('href'):  # 只显示前3个资源
                print(f"CSS 文件 {i+1}: {link.get('href')}")
            
        # 显示JS文件
        for i, script in enumerate(js_tags):
            if i < 3 and script.get('src'):  # 只显示前3个资源
                print(f"JS 文件 {i+1}: {script.get('src')}")
                
        # 显示图片文件
        for i, img in enumerate(img_tags):
            if i < 3 and img.get('src'):  # 只显示前3个图片
                print(f"图片 {i+1}: {img.get('src')}")
                
        print("\n测试完成!")
        
    except Exception as e:
        print(f"测试过程中出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 