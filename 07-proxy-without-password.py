#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by aneasystone on 2018/2/28
from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--proxy-server=127.0.0.1:8118')

browser = webdriver.Chrome(
    executable_path="./drivers/chromedriver.exe",
    chrome_options=chrome_options
)
browser.get('http://ip138.com')