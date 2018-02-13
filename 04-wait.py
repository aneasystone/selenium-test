#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by aneasystone on 2018/2/13
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.support import expected_conditions as Expect

browser = webdriver.Chrome(executable_path="./drivers/chromedriver.exe")
browser.get('http://www.tuniu.com/flight/intel/sha-sel')
Wait(browser, 60).until(
    Expect.text_to_be_present_in_element((By.ID, "loadingStatus"), u"共搜索")
)

flight_items = browser.find_elements_by_class_name("flight-item")
for flight_item in flight_items:
    flight_price_row = flight_item.find_element_by_class_name("flight-price-row")
    print(flight_price_row.get_attribute("data-no"))