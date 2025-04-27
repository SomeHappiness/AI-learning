#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
网页抓取模块 (web_scraper.py)
--------------------------
这个模块负责获取目标网页的HTML、CSS和JavaScript代码。
它是整个克隆过程的第一步，提供后续分析所需的原始数据。

主要功能:
1. 抓取网页HTML内容
2. 下载并保存CSS样式文件
3. 下载并保存JavaScript脚本文件
4. 提取图片URL

支持两种抓取模式:
- 普通模式: 使用requests库抓取静态内容
- Selenium模式: 可以执行JavaScript，抓取动态渲染的内容
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
from tqdm import tqdm  # 进度条库

# 配置日志
logger = logging.getLogger(__name__)

class WebScraper:
    """
    网页抓取器类
    
    负责从指定URL获取网页内容及相关资源(CSS、JS、图片)。
    支持普通抓取和使用Selenium的动态页面抓取。
    """
    
    def __init__(self, use_selenium=False, wait_time=5, temp_dir="temp"):
        """
        初始化WebScraper
        
        参数:
            use_selenium (bool): 是否使用Selenium进行动态网页爬取
            wait_time (int): 使用Selenium时等待页面加载的时间(秒)
            temp_dir (str): 临时文件保存目录
        """
        self.use_selenium = use_selenium  # 是否使用Selenium
        self.wait_time = wait_time        # Selenium等待时间
        self.temp_dir = temp_dir          # 临时文件目录
        self.driver = None                # Selenium WebDriver
        
        # 创建临时目录(如果不存在)
        os.makedirs(temp_dir, exist_ok=True)
        
        # 如果需要使用Selenium，初始化WebDriver
        if self.use_selenium:
            self._init_selenium()
    
    def _init_selenium(self):
        """
        初始化Selenium WebDriver
        
        这个方法配置并启动Chrome浏览器的WebDriver，
        用于抓取需要JavaScript渲染的动态网页。
        """
        try:
            logger.info("正在初始化Selenium WebDriver...")
            
            # 配置Chrome浏览器选项
            chrome_options = Options()
            chrome_options.add_argument("--headless")        # 无头模式(不显示浏览器窗口)
            chrome_options.add_argument("--disable-gpu")     # 禁用GPU加速
            chrome_options.add_argument("--no-sandbox")      # 禁用沙盒
            chrome_options.add_argument("--disable-dev-shm-usage")  # 禁用/dev/shm使用
            
            # 安装并启动Chrome驱动
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            logger.info("Selenium WebDriver初始化成功")
            
        except Exception as e:
            logger.error(f"初始化Selenium WebDriver失败: {str(e)}")
            raise
    
    def fetch_url(self, url):
        """
        抓取指定URL的内容
        
        这是主要的公共方法，根据配置选择使用requests或Selenium抓取页面。
        
        参数:
            url (str): 要抓取的URL
        
        返回:
            dict: 包含HTML内容和页面资源的字典，结构如下:
                {
                    'html': 页面HTML内容,
                    'base_url': 原始URL,
                    'css_files': CSS文件名列表,
                    'js_files': JS文件名列表,
                    'css_content': CSS内容字典,
                    'js_content': JS内容字典,
                    'images': 图片URL列表
                }
        """
        logger.info(f"开始抓取URL: {url}")
        
        # 根据配置选择抓取方法
        if self.use_selenium:
            return self._fetch_with_selenium(url)
        else:
            return self._fetch_with_requests(url)
    
    def _fetch_with_requests(self, url):
        """
        使用requests库抓取页面
        
        适用于静态页面或不需要JavaScript渲染的页面。
        
        参数:
            url (str): 要抓取的URL
            
        返回:
            dict: 抓取结果字典
        """
        try:
            # 设置请求头，模拟浏览器请求
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            }
            
            # 发送GET请求
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()  # 如果返回4xx/5xx状态码，抛出异常
            
            # 获取页面内容并解析
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # 处理页面内容并返回结果
            return self._process_page(url, html_content, soup)
        
        except Exception as e:
            logger.error(f"使用requests抓取页面失败: {str(e)}")
            raise
    
    def _fetch_with_selenium(self, url):
        """
        使用Selenium抓取页面
        
        适用于需要JavaScript渲染的动态页面。
        
        参数:
            url (str): 要抓取的URL
            
        返回:
            dict: 抓取结果字典
        """
        try:
            # 确保WebDriver已初始化
            if not self.driver:
                self._init_selenium()
            
            # 打开URL
            self.driver.get(url)
            
            # 等待页面加载(让JavaScript有时间执行)
            time.sleep(self.wait_time)
            
            # 获取渲染后的页面内容
            html_content = self.driver.page_source
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # 处理页面内容并返回结果
            return self._process_page(url, html_content, soup)
        
        except Exception as e:
            logger.error(f"使用Selenium抓取页面失败: {str(e)}")
            raise
    
    def _process_page(self, base_url, html_content, soup):
        """
        处理页面内容，提取CSS和JavaScript资源
        
        这个方法负责:
        1. 保存HTML内容
        2. 提取并下载CSS文件
        3. 提取并下载JavaScript文件
        4. 提取内联样式和脚本
        5. 提取图片URL
        
        参数:
            base_url (str): 页面URL
            html_content (str): 页面HTML内容
            soup (BeautifulSoup): 解析后的HTML
            
        返回:
            dict: 包含所有提取资源的字典
        """
        # 初始化结果字典
        result = {
            'html': html_content,
            'base_url': base_url,
            'css_files': [],
            'js_files': [],
            'css_content': {},
            'js_content': {},
            'images': []
        }
        
        # 保存HTML内容到临时文件
        html_file = os.path.join(self.temp_dir, 'index.html')
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # === 1. 提取并下载CSS文件 ===
        css_links = soup.find_all('link', rel='stylesheet')
        logger.info(f"找到 {len(css_links)} 个CSS文件")
        
        # 使用tqdm显示下载进度
        for link in tqdm(css_links, desc="下载CSS文件"):
            href = link.get('href')
            if href:
                # 将相对URL转为绝对URL
                css_url = urljoin(base_url, href)
                
                # 生成文件名(使用URL的最后部分或自动生成)
                css_filename = os.path.basename(urlparse(css_url).path) or f"style_{len(result['css_files'])}.css"
                css_path = os.path.join(self.temp_dir, css_filename)
                
                try:
                    # 下载CSS内容
                    css_content = requests.get(css_url).text
                    
                    # 保存到文件
                    with open(css_path, 'w', encoding='utf-8') as f:
                        f.write(css_content)
                    
                    # 添加到结果中
                    result['css_files'].append(css_filename)
                    result['css_content'][css_filename] = css_content
                except Exception as e:
                    logger.warning(f"下载CSS文件失败 {css_url}: {str(e)}")
        
        # === 2. 提取并下载JavaScript文件 ===
        js_tags = soup.find_all('script', src=True)
        logger.info(f"找到 {len(js_tags)} 个JavaScript文件")
        
        for script in tqdm(js_tags, desc="下载JavaScript文件"):
            src = script.get('src')
            if src:
                # 将相对URL转为绝对URL
                js_url = urljoin(base_url, src)
                
                # 生成文件名
                js_filename = os.path.basename(urlparse(js_url).path) or f"script_{len(result['js_files'])}.js"
                js_path = os.path.join(self.temp_dir, js_filename)
                
                try:
                    # 下载JS内容
                    js_content = requests.get(js_url).text
                    
                    # 保存到文件
                    with open(js_path, 'w', encoding='utf-8') as f:
                        f.write(js_content)
                    
                    # 添加到结果中
                    result['js_files'].append(js_filename)
                    result['js_content'][js_filename] = js_content
                except Exception as e:
                    logger.warning(f"下载JavaScript文件失败 {js_url}: {str(e)}")
        
        # === 3. 提取内联样式和脚本 ===
        
        # 提取内联CSS
        style_tags = soup.find_all('style')
        if style_tags:
            # 合并所有内联样式
            inline_css = "\n".join([style.string or "" for style in style_tags])
            inline_css_file = "inline_styles.css"
            
            # 保存到文件
            with open(os.path.join(self.temp_dir, inline_css_file), 'w', encoding='utf-8') as f:
                f.write(inline_css)
                
            # 添加到结果中
            result['css_files'].append(inline_css_file)
            result['css_content'][inline_css_file] = inline_css
        
        # 提取内联JavaScript
        inline_scripts = soup.find_all('script', src=False)
        if inline_scripts:
            # 合并所有内联脚本
            inline_js = "\n".join([script.string or "" for script in inline_scripts if script.string])
            inline_js_file = "inline_scripts.js"
            
            # 保存到文件
            with open(os.path.join(self.temp_dir, inline_js_file), 'w', encoding='utf-8') as f:
                f.write(inline_js)
                
            # 添加到结果中
            result['js_files'].append(inline_js_file)
            result['js_content'][inline_js_file] = inline_js
        
        # === 4. 提取图片URL ===
        images = soup.find_all('img')
        for img in images:
            src = img.get('src')
            if src:
                # 将相对URL转为绝对URL
                img_url = urljoin(base_url, src)
                result['images'].append(img_url)
        
        return result
    
    def close(self):
        """
        关闭资源
        
        关闭Selenium WebDriver并释放资源
        """
        if self.driver:
            self.driver.quit()
            self.driver = None
            logger.info("已关闭Selenium WebDriver")

    def __del__(self):
        """
        析构函数
        
        确保在对象被销毁时关闭WebDriver
        """
        self.close() 