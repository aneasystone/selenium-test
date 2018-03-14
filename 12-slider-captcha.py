#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by aneasystone on 2018/3/2
import random

from PIL import Image, ImageChops
from numpy import array
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.support import expected_conditions as Expect
import requests, io, re
import easing


def convert_css_to_offset(px):
    ps = px.replace('px', '').split(' ')
    x = -int(ps[0])
    y = -int(ps[1])
    return x, y, x + 10, y + 58


def convert_index_to_offset(index):
    row = int(index / 26)
    col = index % 26
    x = col * 10
    y = row * 58
    return x, y, x + 10, y + 58


def get_slider_offset_from_diff_image(diff):
    im = array(diff)
    width, height = diff.size
    diff = []
    for i in range(height):
        for j in range(width):
            # black is not only (0,0,0)
            if im[i, j, 0] > 15 or im[i, j, 1] > 15 or im[i, j, 1] > 15:
                diff.append(j)
                break
    return min(diff)


def get_slider_offset(image_url, image_url_bg, css):
    image_file = io.BytesIO(requests.get(image_url).content)
    im = Image.open(image_file)
    image_file_bg = io.BytesIO(requests.get(image_url_bg).content)
    im_bg = Image.open(image_file_bg)
    # im.show()
    # im_bg.show()

    # 10*58 26/row => background image size = 260*116
    captcha = Image.new('RGB', (260, 116))
    captcha_bg = Image.new('RGB', (260, 116))
    for i, px in enumerate(css):
        offset = convert_css_to_offset(px)
        region = im.crop(offset)
        region_bg = im_bg.crop(offset)
        offset = convert_index_to_offset(i)
        captcha.paste(region, offset)
        captcha_bg.paste(region_bg, offset)
    diff = ImageChops.difference(captcha, captcha_bg)
    # captcha.show()
    # captcha_bg.show()
    # diff.show()
    diff.save('D:/diff.png')
    return get_slider_offset_from_diff_image(diff)


def get_image_css(images):
    css = []
    for image in images:
        position = get_image_position_from_style(image.get_attribute("style"))
        css.append(position)
    return css


def get_image_url_from_style(style):
    match = re.match('background-image: url\("(.*?)"\); background-position: (.*?);', style)
    return match.group(1)


def get_image_position_from_style(style):
    match = re.match('background-image: url\("(.*?)"\); background-position: (.*?);', style)
    return match.group(2)


def get_slice_offset(slice):
    style = slice.get_attribute("style")
    match = re.search('background-image: url\("(.*?)"\);', style)
    url = match.group(1)
    image_file = io.BytesIO(requests.get(url).content)
    im = Image.open(image_file)
    im.save('D:/slice.png')
    return get_slider_offset_from_diff_image(im)


# refer: https://ask.hellobi.com/blog/cuiqingcai/9796
def get_track(distance):
    track = []
    current = 0
    mid = distance * 4 / 5
    t = 0.2
    v = 0

    while current < distance:
        if current < mid:
            a = 2
        else:
            a = -3
        v0 = v
        v = v0 + a * t
        move = v0 * t + 1 / 2 * a * t * t
        current += move
        track.append(round(move))
    return track


def fake_drag(browser, knob, offset):
    # seconds = random.uniform(2, 6)
    # print(seconds)
    # samples = int(seconds*10)
    # diffs = sorted(random.sample(range(0, offset), samples-1))
    # diffs.insert(0, 0)
    # diffs.append(offset)
    # ActionChains(browser).click_and_hold(knob).perform()
    # for i in range(samples):
    #     ActionChains(browser).pause(seconds/samples).move_by_offset(diffs[i+1]-diffs[i], 0).perform()
    # ActionChains(browser).release().perform()

    # tracks = get_track(offset)
    offsets, tracks = easing.get_tracks(offset, 12, 'ease_out_expo')
    print(offsets)
    ActionChains(browser).click_and_hold(knob).perform()
    for x in tracks:
        ActionChains(browser).move_by_offset(x, 0).perform()
    ActionChains(browser).pause(0.5).release().perform()

    return


def do_crack(browser):
    slice = browser.find_element_by_class_name("gt_slice")
    slice_offset = get_slice_offset(slice)
    print(slice_offset)

    images = browser.find_elements_by_class_name("gt_cut_fullbg_slice")
    images_bg = browser.find_elements_by_class_name("gt_cut_bg_slice")
    image_url = get_image_url_from_style(images[0].get_attribute("style"))
    image_url_bg = get_image_url_from_style(images_bg[0].get_attribute("style"))
    css = get_image_css(images)
    offset = get_slider_offset(image_url, image_url_bg, css)
    print(offset)

    knob = browser.find_element_by_class_name("gt_slider_knob")
    # ActionChains(browser).drag_and_drop_by_offset(knob, offset - slice_offset, 0).perform()
    fake_drag(browser, knob, offset - slice_offset)
    return

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")
browser = webdriver.Chrome(
    executable_path="./drivers/chromedriver.exe",
    chrome_options=chrome_options
)
browser.get('https://account.ch.com/NonRegistrations-Regist')
Wait(browser, 60).until(
    Expect.visibility_of_element_located((By.CSS_SELECTOR, "div[data-target='account-login']"))
)
email = browser.find_element_by_css_selector("div[data-target='account-login']")
email.click()

Wait(browser, 60).until(
    Expect.visibility_of_element_located((By.ID, "emailRegist"))
)
register = browser.find_element_by_id("emailRegist")
register.click()

do_crack(browser)
