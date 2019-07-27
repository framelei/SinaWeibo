# -*- coding: utf-8 -*-



BOT_NAME = 'SinaWeibo'
SPIDER_MODULES = ['SinaWeibo.spiders']
NEWSPIDER_MODULE = 'SinaWeibo.spiders'


ROBOTSTXT_OBEY = False
DOWNLOAD_DELAY = 0.25


DOWNLOADER_MIDDLEWARES = {
    'SinaWeibo.middlewares.UserAgentMiddleware': 300,
    # 'SinaWeibo.middlewares.CookiesMiddleware': 310,
    # 'SinaWeibo.middlewares.ProxyMiddleware': 320
}

ITEM_PIPELINES = {
    'SinaWeibo.pipelines.TimePipeline': 300,
    'SinaWeibo.pipelines.SinaweiboPipeline': 310,
    'SinaWeibo.pipelines.CleanTimePipeline': 315,
    'SinaWeibo.pipelines.Fanscount_2_int': 316,
    # 'SinaWeibo.pipelines.MongoDBPipeline': 320,
    'SinaWeibo.pipelines.MysqlTwistedPipline': 325,

}


KEYWORD = '天使投资人'

MONGO_DB = 'sinaweibo'
MONGO_URI = 'localhost'
MONGO_USER = 'root'
MONGO_PWD = 'Mongo_Lei'

MYSQL_HOST = '127.0.0.1'
MYSQL_DATABASE = 'sinaweibo'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'Sql_Lei'

MYSQL_TABLE = 'articles'

#日志显示级别
# LOG等级
# LOG_LEVEL = 'DEBUG'
# #指定日志输出的文件名，也可指定到标准输出端口
# LOG_FILE = "SinaWeibo.log"

COOKIES_URL = 'http://127.0.0.1:5555/weibo/random'
# COOKIES_URL = 'http://192.168.43.212:5555/weibo/random'
PROXY_URL = 'http://192.168.43.212:5556/random'
