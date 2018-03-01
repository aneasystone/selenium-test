#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by aneasystone on 2018/3/1
from selenium import webdriver
from browsermobproxy import Server

# bmp can downloaded from: https://github.com/lightbody/browsermob-proxy/releases
server = Server("D:/browsermob-proxy-2.1.4/bin/browsermob-proxy")
server.start()
proxy = server.create_proxy()

proxy.blacklist(".*google-analytics.*", 404)
proxy.blacklist(".*google.*", 404)
proxy.blacklist(".*yahoo.*", 404)
proxy.blacklist(".*facebook.*", 404)
proxy.blacklist(".*twitter.*", 404)
# proxy.blacklist(".*flypeach.*", 404)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--proxy-server={0}".format(proxy.proxy))
browser = webdriver.Chrome(
    executable_path="./drivers/chromedriver.exe",
    chrome_options = chrome_options
)
browser.get('http://www.flypeach.com/pc/hk')

server.stop()
browser.quit()
