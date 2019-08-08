# -*- coding: utf-8 -*-



BOT_NAME = 'SinaWeibo'
SPIDER_MODULES = ['SinaWeibo.spiders']
NEWSPIDER_MODULE = 'SinaWeibo.spiders'


ROBOTSTXT_OBEY = False
DOWNLOAD_DELAY = 0.1



DOWNLOADER_MIDDLEWARES = {
    'SinaWeibo.middlewares.UserAgentMiddleware': 300,
    'SinaWeibo.middlewares.CookiesMiddleware': 310,
    # 'SinaWeibo.middlewares.ProxyMiddleware': 320,
    # 'SinaWeibo.middlewares.ProxyMiddleware_Abuyun': 320,
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

MYSQL_HOST = 'localhost'
MYSQL_DATABASE = 'sinaweibo'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'Sql_Lei'

MYSQL_TABLE = 'articles'

#日志显示级别
# LOG等级
# LOG_LEVEL = 'INFO'
# 指定日志输出的文件名，也可指定到标准输出端口
# LOG_FILE = "SinaWeibo.log"

COOKIES_URL = 'http://129.28.200.147:5555/weibo/random'
PROXY_URL = 'http://129.28.200.147:5557/random'


# 设置最大等待时间、失败重试次数
#默认响应时间是180s，长时间不释放会占用一个并发量影响效率
DOWNLOAD_TIMEOUT = 10
# 是否进行失败重试
RETRY_ENABLED = True
# 失败重试的次数，连续失败3次后会抛出TimeOut异常被errback捕获
RETRY_TIMES = 3