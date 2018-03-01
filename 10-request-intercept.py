#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by aneasystone on 2018/3/1
from selenium import webdriver
from browsermobproxy import Server

# bmp can downloaded from: https://github.com/lightbody/browsermob-proxy/releases
server = Server("D:/browsermob-proxy-2.1.4/bin/browsermob-proxy")
server.start()
proxy = server.create_proxy()

request_js = (
    '''
    request.headers().remove('User-Agent');
    request.headers().add('User-Agent', 'My-Custom-User-Agent-String 1.0');
    '''
)
response_js = (
    '''
    if (messageInfo.getOriginalUrl().contains("remote/searchFlights")) {
        contents.setTextContents('Hello World');
    }
    '''
)
proxy.request_interceptor(request_js)
proxy.response_interceptor(response_js)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--proxy-server={0}".format(proxy.proxy))
browser = webdriver.Chrome(
    executable_path="./drivers/chromedriver.exe",
    chrome_options = chrome_options
)
browser.get('http://www.tuniu.com/flight/intel/sha-bkk')

server.stop()
# browser.quit()