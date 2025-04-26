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
        try:
            logger.info("初始化Selenium WebDriver...")
            chrome_options = Options()
            chrome_options.add_argument("--headless")  # 无头模式
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            logger.info("Selenium WebDriver初始化成功")
        except Exception as e:
            logger.error(f"初始化Selenium WebDriver失败: {str(e)}")
            raise
    
    def fetch_url(self, url):
        """
        抓取指定URL的内容
        
        Args:
            url (str): 要抓取的URL
        
        Returns:
            dict: 包含HTML内容和页面资源的字典
        """
        logger.info(f"开始抓取URL: {url}")
        
        if self.use_selenium:
            return self._fetch_with_selenium(url)
        else:
            return self._fetch_with_requests(url)
    
    def _fetch_with_requests(self, url):
        """使用requests库抓取页面"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            }
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')
            
            return self._process_page(url, html_content, soup)
        
        except Exception as e:
            logger.error(f"使用requests抓取页面失败: {str(e)}")
            raise
    
    def _fetch_with_selenium(self, url):
        """使用Selenium抓取页面"""
        try:
            if not self.driver:
                self._init_selenium()
            
            self.driver.get(url)
            time.sleep(self.wait_time)  # 等待页面加载
            
            html_content = self.driver.page_source
            soup = BeautifulSoup(html_content, 'html.parser')
            
            return self._process_page(url, html_content, soup)
        
        except Exception as e:
            logger.error(f"使用Selenium抓取页面失败: {str(e)}")
            raise
    
    def _process_page(self, base_url, html_content, soup):
        """处理页面内容，提取CSS和JavaScript资源"""
        result = {
            'html': html_content,
            'base_url': base_url,
            'css_files': [],
            'js_files': [],
            'css_content': {},
            'js_content': {},
            'images': []
        }
        
        # 保存HTML内容
        html_file = os.path.join(self.temp_dir, 'index.html')
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # 提取并下载CSS文件
        css_links = soup.find_all('link', rel='stylesheet')
        logger.info(f"找到 {len(css_links)} 个CSS文件")
        
        for link in tqdm(css_links, desc="下载CSS文件"):
            href = link.get('href')
            if href:
                css_url = urljoin(base_url, href)
                css_filename = os.path.basename(urlparse(css_url).path) or f"style_{len(result['css_files'])}.css"
                css_path = os.path.join(self.temp_dir, css_filename)
                
                try:
                    css_content = requests.get(css_url).text
                    with open(css_path, 'w', encoding='utf-8') as f:
                        f.write(css_content)
                    
                    result['css_files'].append(css_filename)
                    result['css_content'][css_filename] = css_content
                except Exception as e:
                    logger.warning(f"下载CSS文件失败 {css_url}: {str(e)}")
        
        # 提取并下载JavaScript文件
        js_tags = soup.find_all('script', src=True)
        logger.info(f"找到 {len(js_tags)} 个JavaScript文件")
        
        for script in tqdm(js_tags, desc="下载JavaScript文件"):
            src = script.get('src')
            if src:
                js_url = urljoin(base_url, src)
                js_filename = os.path.basename(urlparse(js_url).path) or f"script_{len(result['js_files'])}.js"
                js_path = os.path.join(self.temp_dir, js_filename)
                
                try:
                    js_content = requests.get(js_url).text
                    with open(js_path, 'w', encoding='utf-8') as f:
                        f.write(js_content)
                    
                    result['js_files'].append(js_filename)
                    result['js_content'][js_filename] = js_content
                except Exception as e:
                    logger.warning(f"下载JavaScript文件失败 {js_url}: {str(e)}")
        
        # 提取内联样式和脚本
        style_tags = soup.find_all('style')
        if style_tags:
            inline_css = "\n".join([style.string or "" for style in style_tags])
            inline_css_file = "inline_styles.css"
            with open(os.path.join(self.temp_dir, inline_css_file), 'w', encoding='utf-8') as f:
                f.write(inline_css)
            result['css_files'].append(inline_css_file)
            result['css_content'][inline_css_file] = inline_css
        
        inline_scripts = soup.find_all('script', src=False)
        if inline_scripts:
            inline_js = "\n".join([script.string or "" for script in inline_scripts if script.string])
            inline_js_file = "inline_scripts.js"
            with open(os.path.join(self.temp_dir, inline_js_file), 'w', encoding='utf-8') as f:
                f.write(inline_js)
            result['js_files'].append(inline_js_file)
            result['js_content'][inline_js_file] = inline_js
        
        # 提取图片URL
        images = soup.find_all('img')
        for img in images:
            src = img.get('src')
            if src:
                img_url = urljoin(base_url, src)
                result['images'].append(img_url)
        
        return result
    
    def close(self):
        """关闭资源"""
        if self.driver:
            self.driver.quit()
            self.driver = None

    def __del__(self):
        """析构函数，确保关闭WebDriver"""
        self.close() 