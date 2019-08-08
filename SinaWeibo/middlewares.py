# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import random
import requests
import json


class UserAgentMiddleware(object):

    def process_request(self,request,spider):
        # 在百度里搜索user_agent_list粘进来
        user_agent_list = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
       ]
        agent = random.choice(user_agent_list)
        # 同样在setting里开启
        request.headers['User_Agent'] = agent


class CookiesMiddleware(object):
    #调用cookies池发起请求

    def __init__(self,cookies_url):
        self.cookies_url = cookies_url

    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            cookies_url = crawler.settings.get('COOKIES_URL')
        )

    def get_random_cookies(self):
        #请求目标url获取随机cookies
        try:
            response = requests.get(self.cookies_url)
            response.raise_for_status()
            cookies = json.loads(response.text)
            return cookies
        except:
            print('cookies请求失败')

    def process_request(self,request,spider):
        #使用代理池中的cookies发起请求
        cookies = self.get_random_cookies()
        if cookies:
            request.cookies = cookies
            print('正在使用代理cookies：',cookies)

# 使用讯代理对接代理池
class ProxyMiddleware():

    def __init__(self, proxy_url):
        self.proxy_url = proxy_url

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            proxy_url=crawler.settings.get('PROXY_URL')
        )

    def get_random_proxy(self):
        #请求目标url获取随机ip
        try:
            response = requests.get(self.proxy_url)
            response.raise_for_status()
            proxy = response.text
            return proxy
        except:
            print('ip请求失败')

    def process_request(self, request, spider):
        #使用代理池中的ip发起请求
        #retry_times，当第一次请求失败时再启动代理ip。因为本机ip更稳定
        if request.meta.get('retry_times'):
            proxy = self.get_random_proxy()
            if proxy:
                uri = 'https://{proxy}'.format(proxy=proxy)
                print('正在使用代理',uri)
                request.meta['proxy'] = uri


# 使用阿布云代理隧道
import base64
# 1、代理服务器
proxyServer = "http://http-dyn.abuyun.com:9020"
# 2、代理隧道验证信息
proxyUser = "HK7S2A2KW3ME8T8D"
proxyPass = "E22841FF90C9065D"
# 3、对用户名、密码进行加密，注意空格"Basic "
proxyAuth = "Basic " + base64.urlsafe_b64encode(bytes((proxyUser + ":" + proxyPass), "ascii")).decode("utf8")
print(proxyAuth)        #Basic SDAxMjM0NTY3ODkwMTIzRDowMTIzNDU2Nzg5MDEyMzQ1
# 4、在process_request()方法中设置代理
class ProxyMiddleware_Abuyun(object):
    def process_request(self, request, spider):
        request.meta["proxy"] = proxyServer
        request.headers["Proxy-Authorization"] = proxyAuth