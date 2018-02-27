#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by aneasystone on 2018/2/13
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# chromedriver can downloaded from: https://sites.google.com/a/chromium.org/chromedriver/
browser = webdriver.Chrome(executable_path="./drivers/chromedriver.exe")
browser.get('https://www.baidu.com')

kw = browser.find_element_by_id("kw")
su = browser.find_element_by_id("su")

#
# input
#

# method 1, send keys with return
# kw.send_keys("Selenium", Keys.RETURN)

# method 2, send keys then click submit button
# kw.send_keys("Selenium")
# su.click()

# method 3, send keys then submit form
# kw.send_keys("Selenium")
# kw.submit()

# method 4, execute javascript
browser.execute_script(
    '''
    var kw = document.getElementById('kw');
    var su = document.getElementById('su');
    kw.value = 'Selenium';
    su.click();
    '''
)

time.sleep(3)

#
# output
#

# method 1, parse page_source
# print(browser.page_source)

# method 2, find elements
results = browser.find_elements_by_css_selector("#content_left .c-container")
for result in results:
    print(result.get_attribute("id"))
    # //h3/a searches the whole page for the XPath expression.
    # .//h3/a takes the specified element as root
    link = result.find_element_by_xpath(".//h3/a")
    print(link.text)