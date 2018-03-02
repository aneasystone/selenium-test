#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by aneasystone on 2018/3/2
from PIL import Image, ImageChops
import requests, io

url = "https://static.geetest.com/pictures/gt/73f2074d1/73f2074d1.webp"
image_file = io.BytesIO(requests.get(url).content)
im = Image.open(image_file)

url_bg = "https://static.geetest.com/pictures/gt/73f2074d1/bg/72a6e6d79.webp"
image_file_bg = io.BytesIO(requests.get(url_bg).content)
im_bg = Image.open(image_file_bg)

# im.save('D:/b.jpeg')
# im.show()

css = [
    "-157px -58px",
    "-145px -58px",
    "-265px -58px",
    "-277px -58px",
    "-181px -58px",
    "-169px -58px",
    "-241px -58px",
    "-253px -58px",
    "-109px -58px",
    "-97px -58px",
    "-289px -58px",
    "-301px -58px",
    "-85px -58px",
    "-73px -58px",
    "-25px -58px",
    "-37px -58px",
    "-13px -58px",
    "-1px -58px",
    "-121px -58px",
    "-133px -58px",
    "-61px -58px",
    "-49px -58px",
    "-217px -58px",
    "-229px -58px",
    "-205px -58px",
    "-193px -58px",
    "-145px 0px",
    "-157px 0px",
    "-277px 0px",
    "-265px 0px",
    "-169px 0px",
    "-181px 0px",
    "-253px 0px",
    "-241px 0px",
    "-97px 0px",
    "-109px 0px",
    "-301px 0px",
    "-289px 0px",
    "-73px 0px",
    "-85px 0px",
    "-37px 0px",
    "-25px 0px",
    "-1px 0px",
    "-13px 0px",
    "-133px 0px",
    "-121px 0px",
    "-49px 0px",
    "-61px 0px",
    "-229px 0px",
    "-217px 0px",
    "-193px 0px",
    "-205px 0px"
    ]


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

#
# 10*58 26/row => background image size = 260*116
#
captcha = Image.new('RGB', (260, 116))
captcha_bg = Image.new('RGB', (260, 116))
for i, px in enumerate(css):
    offset = convert_css_to_offset(px)
    region = im.crop(offset)
    region_bg = im_bg.crop(offset)
    offset = convert_index_to_offset(i)
    captcha.paste(region, offset)
    captcha_bg.paste(region_bg, offset)
# captcha.show()
# captcha_bg.show()
diff = ImageChops.difference(captcha, captcha_bg)
diff.show()