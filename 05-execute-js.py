#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by aneasystone on 2018/2/13
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.support import expected_conditions as Expect
from selenium.webdriver.support.select import Select

browser = webdriver.Chrome(executable_path="./drivers/chromedriver.exe")
browser.get('http://www.tuniu.com/flight_intel/')

# method 1 totally simulate human action
depart = browser.find_element_by_name("departCityName")
depart.click()
depart.send_keys("BJS")
Wait(browser, 10).until(
    Expect.presence_of_element_located((By.CLASS_NAME, "tn-city-node"))
)
depart.send_keys(Keys.RETURN)

dest = browser.find_element_by_name("destCityName")
dest.click()
dest.send_keys("SEL")
Wait(browser, 10).until(
    Expect.presence_of_element_located((By.CLASS_NAME, "tn-city-node"))
)
dest.send_keys(Keys.RETURN)

# method 2 execute javascript
browser.execute_script("$('input[name=departCityName]').val('CAN')")
browser.execute_script("$('input[name=destCityName]').val('MFM')")
browser.execute_script("$('input[name=departDate]').val('2018-10-01')")
browser.execute_script("$('input[name=destDate]').val('2018-10-05')")
browser.execute_script("$('select[name=adultQuantity]').setValue(2)")

adultQuantity = browser.find_element_by_name("adultQuantity")
Select(adultQuantity).select_by_value("4")

browser.execute_script("arguments[0].click();", browser.find_element_by_xpath("//div[@data-name='typeSelect']/span[1]"))
# browser.execute_script("arguments[0].click();", browser.find_element_by_id("searchIntl"))