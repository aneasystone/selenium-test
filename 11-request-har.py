#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by aneasystone on 2018/3/1
import json
from selenium import webdriver
from browsermobproxy import Server
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.support import expected_conditions as Expect

# bmp can downloaded from: https://github.com/lightbody/browsermob-proxy/releases
server = Server("D:/browsermob-proxy-2.1.4/bin/browsermob-proxy")
server.start()
proxy = server.create_proxy()

proxy.blacklist(".*gov.cn.*", 404)
proxy.new_har(options={
    'captureContent': True
})

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--proxy-server={0}".format(proxy.proxy))
browser = webdriver.Chrome(
    executable_path="./drivers/chromedriver.exe",
    chrome_options=chrome_options
)
browser.get('http://www.tuniu.com/flight/intel/sha-bkk')
Wait(browser, 60).until(
    Expect.text_to_be_present_in_element((By.ID, "loadingStatus"), u"共搜索")
)

for entry in proxy.har['log']['entries']:
    if 'remote/searchFlights' in entry['request']['url']:
        result = json.loads(entry['response']['content']['text'])
        for key, item in result['data']['flightInfo'].items():
            print(key)

server.stop()
browser.quit()