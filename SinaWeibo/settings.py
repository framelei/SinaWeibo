# -*- coding: utf-8 -*-



BOT_NAME = 'SinaWeibo'
SPIDER_MODULES = ['SinaWeibo.spiders']
NEWSPIDER_MODULE = 'SinaWeibo.spiders'


ROBOTSTXT_OBEY = False

DOWNLOAD_DELAY = 1


DOWNLOADER_MIDDLEWARES = {
    'SinaWeibo.middlewares.UserAgentMiddleware': 300,
    'SinaWeibo.middlewares.CookiesMiddleware': 310,
    # 'SinaWeibo.middlewares.ProxyMiddleware': 320
}

ITEM_PIPELINES = {
    'SinaWeibo.pipelines.TimePipeline': 300,
    'SinaWeibo.pipelines.SinaweiboPipeline': 310,
    'SinaWeibo.pipelines.CleanTimePipeline': 315,
    'SinaWeibo.pipelines.MongoDBPipeline': 320,
}


KEYWORD = '天使投资人'

MONGO_DB = 'Weibo'
MONGO_URI = 'localhost'
MONGO_USER = 'root'
MONGO_PWD = '123456'


COOKIES_URL = 'http://192.168.43.212:5555/weibo/random'
PROXY_URL = 'http://192.168.43.212:5556/random'
