#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by aneasystone on 2018/2/28
import os, shutil
import zipfile
from selenium import webdriver

extension_dir = './extensions'
proxy = {
    'schema': 'http',
    'host': '127.0.0.1',
    'port': 8118,
    'username': '',
    'password': ''
}


def get_manifest_content():
    return '''
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    '''


def get_background_content():
    return '''
    chrome.proxy.settings.set({{
        value: {{
            mode: "fixed_servers",
            rules: {{
                singleProxy: {{
                    scheme: {0},
                    host: "{1}",
                    port: {2}
                }},
                bypassList: ["foobar.com"]
            }}
        }},
        scope: "regular"
    }}, function() {{}});

    chrome.webRequest.onAuthRequired.addListener(
        function (details) {{
            return {{
                authCredentials: {{
                    username: "{3}",
                    password: "{4}"
                }}
            }};
        }},
        {{ urls: ["<all_urls>"] }},
        [ 'blocking' ]
    );
    '''.format(proxy['schema'], proxy['host'], proxy['port'], proxy['username'], proxy['password'])


def get_extension_file_path():
    path = "{0}/{1}_{2}.zip".format(extension_dir, proxy['host'], proxy['port'])
    if os.path.exists(path):
        os.remove(path)

    zf = zipfile.ZipFile(path, mode='w')
    zf.writestr('manifest.json', get_manifest_content())
    zf.writestr('background.js', get_background_content())
    zf.close()
    return path


def get_extension_dir_path():
    path = "{0}/{1}_{2}".format(extension_dir, proxy['host'], proxy['port'])
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)

    with open(path + '/manifest.json', 'wb') as f:
        f.write(get_manifest_content())
    with open(path + '/background.js', 'wb') as f:
        f.write(get_background_content())
    return path

chrome_options = webdriver.ChromeOptions()
chrome_options.add_extension(get_extension_file_path())
# chrome_options.add_argument('--load-extension={0}'.format(get_extension_dir_path()))

browser = webdriver.Chrome(
    executable_path="./drivers/chromedriver.exe",
    chrome_options=chrome_options
)
browser.get('http://ip138.com')