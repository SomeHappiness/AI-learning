#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from website_document_generator import WebsiteDocumentGenerator

def test_generator():
    try:
        # 创建测试数据
        test_data = {
            'colors': [{'color': '#fff', 'count': 10}],
            'fonts': []
        }
        
        # 创建生成器实例
        gen = WebsiteDocumentGenerator()
        
        # 调用生成YAML数据的方法
        gen._generate_yaml_data({}, test_data, 'https://example.com')
        
        print('测试成功！')
        
    except Exception as e:
        print(f'测试失败，错误信息：{str(e)}')
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_generator() 