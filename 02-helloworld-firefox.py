#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by aneasystone on 2018/2/13
from selenium import webdriver

# geckodriver can downloaded from: https://github.com/mozilla/geckodriver/releases
browser = webdriver.Firefox(executable_path="./drivers/geckodriver.exe")
browser.get('https://www.baidu.com')