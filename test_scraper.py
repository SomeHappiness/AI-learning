#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试WebScraper功能的脚本
"""

import os
import sys
import json
from web_scraper import WebScraper

def generate_api_doc(apis, output_file):
    """
    生成API文档
    
    Args:
        apis (list): API列表
        output_file (str): 输出文件路径
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# 网页接口文档\n\n")
        f.write("本文档由自动化工具生成，列出了页面中检测到的所有API接口。\n\n")
        
        # 按类型分组
        form_apis = [api for api in apis if api.get('type') == 'FORM']
        ajax_apis = [api for api in apis if api.get('type') == 'AJAX']
        
        # 表单接口
        if form_apis:
            f.write("## 表单接口\n\n")
            for i, api in enumerate(form_apis):
                f.write(f"### {i+1}. {api['method']} {api['url']}\n\n")
                f.write("**参数列表：**\n\n")
                if api.get('parameters'):
                    f.write("| 参数名 | 类型 | 是否必填 |\n")
                    f.write("|--------|------|----------|\n")
                    for param in api['parameters']:
                        required = "是" if param.get('required') else "否"
                        f.write(f"| {param['name']} | {param.get('type', '文本')} | {required} |\n")
                else:
                    f.write("无参数\n")
                f.write("\n")
        
        # AJAX接口
        if ajax_apis:
            f.write("## AJAX接口\n\n")
            for i, api in enumerate(ajax_apis):
                f.write(f"### {i+1}. {api['method']} {api['url']}\n\n")
                f.write(f"**来源：** {api.get('source', '未知')}\n\n")
                f.write("\n")
        
        # 如果没有发现任何API
        if not form_apis and not ajax_apis:
            f.write("**未检测到任何API接口**\n\n")
            f.write("可能的原因：\n")
            f.write("1. 页面使用了动态加载技术，需要启用Selenium模式\n")
            f.write("2. 页面上没有表单或者AJAX调用\n")
            f.write("3. 页面使用了自定义的API调用方式，无法被自动检测\n")

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
        
        # 保存原始API数据为JSON
        api_json_path = os.path.join(output_dir, "apis.json")
        with open(api_json_path, "w", encoding="utf-8") as f:
            json.dump(result['apis'], f, ensure_ascii=False, indent=2)
            
        # 生成API文档
        api_doc_path = os.path.join(output_dir, "api_document.md")
        generate_api_doc(result['apis'], api_doc_path)
        
        print(f"找到 {len(result['apis'])} 个API接口")
        print(f"已保存API文档到: {api_doc_path}")
        print(f"已保存API原始数据到: {api_json_path}")
                
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