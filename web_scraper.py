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
    
    # ... 其余代码保持不变 ... 