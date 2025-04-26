#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
网页抓取模块
负责获取目标网页的HTML、CSS和JavaScript代码
"""

import os
import time
import logging
import requests
import re
import json
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from tqdm import tqdm

logger = logging.getLogger(__name__)

class WebScraper:
    """网页抓取器类，用于获取网页内容"""
    
    def __init__(self, use_selenium=False, wait_time=5, temp_dir="temp"):
        """
        初始化WebScraper
        
        Args:
            use_selenium (bool): 是否使用Selenium进行动态网页爬取
            wait_time (int): 使用Selenium时等待页面加载的时间(秒)
            temp_dir (str): 临时文件保存目录
        """
        self.use_selenium = use_selenium
        self.wait_time = wait_time
        self.temp_dir = temp_dir
        self.driver = None
        
        # 创建临时目录
        os.makedirs(temp_dir, exist_ok=True)
        
        # 初始化Selenium(如果需要)
        if self.use_selenium:
            self._init_selenium()
    
    def _init_selenium(self):
        """初始化Selenium WebDriver"""
        options = Options()
        options.add_argument("--headless")  # 无头模式
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
    
    def fetch_url(self, url):
        """
        获取指定URL的内容
        
        Args:
            url (str): 要抓取的URL
            
        Returns:
            dict: 包含HTML内容和资源文件的字典
        """
        result = {
            'html': '',
            'css_files': [],
            'js_files': [],
            'images': [],
            'apis': []  # 新增：存储API接口
        }
        
        try:
            if self.use_selenium:
                self.driver.get(url)
                time.sleep(self.wait_time)  # 等待页面加载
                html_content = self.driver.page_source
            else:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
                response = requests.get(url, headers=headers, timeout=30)
                response.raise_for_status()
                # 显式设置编码，让requests自动检测编码
                response.encoding = response.apparent_encoding
                html_content = response.text
            
            # 解析HTML
            soup = BeautifulSoup(html_content, 'html.parser')
            result['html'] = str(soup)
            
            # 提取CSS文件
            for css_tag in soup.find_all('link', rel='stylesheet'):
                if css_tag.get('href'):
                    css_url = urljoin(url, css_tag['href'])
                    result['css_files'].append(css_url)
            
            # 提取JS文件
            for js_tag in soup.find_all('script', src=True):
                js_url = urljoin(url, js_tag['src'])
                result['js_files'].append(js_url)
            
            # 提取图片
            for img_tag in soup.find_all('img', src=True):
                img_url = urljoin(url, img_tag['src'])
                result['images'].append(img_url)
            
            # 分析API接口
            result['apis'] = self._analyze_apis(soup, url, html_content)
                
            return result
            
        except Exception as e:
            logger.error(f"抓取URL {url} 时出错: {e}")
            raise
    
    def _analyze_apis(self, soup, base_url, html_content):
        """
        分析页面中的API接口
        
        Args:
            soup (BeautifulSoup): 解析后的HTML
            base_url (str): 基础URL
            html_content (str): 原始HTML内容
            
        Returns:
            list: API接口列表
        """
        apis = []
        
        # 1. 从表单中提取API
        for form in soup.find_all('form'):
            api = {
                'type': 'FORM',
                'method': form.get('method', 'GET').upper(),
                'url': urljoin(base_url, form.get('action', '')),
                'parameters': []
            }
            
            # 提取表单参数
            for input_tag in form.find_all(['input', 'select', 'textarea']):
                name = input_tag.get('name')
                if name:
                    api['parameters'].append({
                        'name': name,
                        'type': input_tag.get('type', 'text'),
                        'required': input_tag.get('required') is not None
                    })
            
            apis.append(api)
        
        # 2. 分析内联JavaScript中的API调用
        # 寻找常见的Ajax模式
        ajax_patterns = [
            r'(get|post|put|delete|patch)\s*\(\s*[\'"]([^\'")]+)[\'"]',  # jQuery和普通Ajax
            r'url\s*:\s*[\'"]([^\'")]+)[\'"]',  # Ajax配置
            r'fetch\s*\(\s*[\'"]([^\'")]+)[\'"]',  # Fetch API
            r'axios\.(get|post|put|delete|patch)\s*\(\s*[\'"]([^\'")]+)[\'"]'  # Axios
        ]
        
        # 从内联脚本提取
        for script in soup.find_all('script'):
            if not script.get('src'):  # 只分析内联脚本
                script_content = script.string
                if script_content:
                    for pattern in ajax_patterns:
                        for match in re.finditer(pattern, script_content, re.IGNORECASE):
                            # 这里简化处理，实际上需要更复杂的逻辑来确定HTTP方法
                            method = match.group(1).upper() if '(' in pattern and match.group(1) else 'GET'
                            url_group = 2 if '(' in pattern and len(match.groups()) > 1 else 1
                            url = match.group(url_group)
                            
                            # 过滤掉非API的URL（简单判断）
                            if url and not url.startswith(('http://', 'https://', '//', '/')):
                                continue
                                
                            full_url = url
                            if url.startswith('/'):
                                full_url = urljoin(base_url, url)
                                
                            # 避免重复添加
                            if not any(api['url'] == full_url and api['method'] == method for api in apis):
                                apis.append({
                                    'type': 'AJAX',
                                    'method': method,
                                    'url': full_url,
                                    'source': 'inline-script'
                                })
        
        # 3. 下载并分析外部JS文件中的API（这里只是示例，实际实现可能更复杂）
        # 注意：这部分可能会增加抓取时间，视情况启用
        '''
        for js_url in result['js_files'][:5]:  # 限制只分析前5个JS文件
            try:
                js_response = requests.get(js_url, headers=headers, timeout=10)
                js_content = js_response.text
                
                for pattern in ajax_patterns:
                    for match in re.finditer(pattern, js_content, re.IGNORECASE):
                        # 与上面类似的处理...
            except Exception as e:
                logger.warning(f"无法分析JS文件 {js_url}: {e}")
        '''
                
        return apis
    
    def close(self):
        """关闭WebScraper并释放资源"""
        if self.driver:
            self.driver.quit()
            self.driver = None

    # ... 其余代码保持不变 ... 