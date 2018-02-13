#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by aneasystone on 2018/2/13
from selenium import webdriver
from browsermobproxy import Server

# bmp can downloaded from: https://github.com/lightbody/browsermob-proxy/releases
server = Server("D:/browsermob-proxy-2.1.4/bin/browsermob-proxy")
server.start()
proxy = server.create_proxy()


''' 拦截请求，对请求参数进行修改，或者直接返回伪造响应
proxyServer.addRequestFilter(new RequestFilter() {
    @Override
    public io.netty.handler.codec.http.HttpResponse filterRequest(
            io.netty.handler.codec.http.HttpRequest request,
            net.lightbody.bmp.util.HttpMessageContents contents,
            net.lightbody.bmp.util.HttpMessageInfo messageInfo) {
        String url = messageInfo.getOriginalUrl();
        if (url.contains("twitter.com") || url.contains("google.com") || url.contains("doubleclick.net")) {
            HttpResponse response = new io.netty.handler.codec.http.DefaultFullHttpResponse(HttpVersion.HTTP_1_1, HttpResponseStatus.NOT_FOUND);
            HttpHeaders.setContentLength(response, 0L);
            return response;
        }
        return null;
    }
});
'''

# request_js = (
#     '''
#     var url = messageInfo.getOriginalUrl();
#     if (url.contains("google") || url.contains("yahoo") || url.contains("twitter") || url.contains("facebook")) {
#         //return new io.netty.handler.codec.http.DefaultFullHttpResponse(
#         //    io.netty.handler.codec.http.HttpVersion.HTTP_1_1,
#         //    io.netty.handler.codec.http.HttpResponseStatus.NOT_FOUND
#         //);
#     }
#     '''
# )
# proxy.request_interceptor(request_js)

proxy.blacklist(".*google-analytics.*", 404)
proxy.blacklist(".*google.*", 404)
proxy.blacklist(".*yahoo.*", 404)
proxy.blacklist(".*facebook.*", 404)
proxy.blacklist(".*twitter.*", 404)
# proxy.blacklist(".*flypeach.*", 404)

# webdriver.Proxy(proxy.proxy)                          # not work

profile = webdriver.FirefoxProfile()
profile.set_proxy(proxy.selenium_proxy())           # deprecated, but works

browser = webdriver.Firefox(
    executable_path="./drivers/geckodriver.exe",
    firefox_profile=profile,
    # proxy=proxy.selenium_proxy()                    # not work
)
browser.get('http://www.flypeach.com/pc/hk')

server.stop()
browser.quit()

# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--proxy-server={0}".format(proxy.proxy))
# browser = webdriver.Chrome(chrome_options = chrome_options)