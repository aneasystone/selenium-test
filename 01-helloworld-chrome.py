#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by aneasystone on 2018/2/13
from selenium import webdriver

# chromedriver can downloaded from: https://sites.google.com/a/chromium.org/chromedriver/
browser = webdriver.Chrome(executable_path="./drivers/chromedriver.exe")
browser.get('https://www.baidu.com')