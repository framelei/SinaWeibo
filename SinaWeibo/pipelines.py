# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from SinaWeibo.items import Weiboitem,Useritem
from twisted.enterprise import adbapi   #enterprise:事业、企业
import MySQLdb.cursors
import time
import re


class SinaweiboPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item,Weiboitem):
            if item.get('pictures'):
                item['pictures'] = [pic.get('url') for pic in item['pictures']]
        return item


class MongoDBPipeline(object):
    #将数据写入MongoDB数据库

    def __init__(self,mongo_db,mongo_uri,mongo_user,mongo_pwd):
        self.mongo_db = mongo_db
        self.mongo_uri = mongo_uri
        self.mongo_user = mongo_user
        self.mongo_pwd = mongo_pwd

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_db = crawler.settings.get('MONGO_DB'),
            mongo_uri = crawler.settings.get('MONGO_URI'),
            mongo_user = crawler.settings.get('MONGO_USER'),
            mongo_pwd = crawler.settings.get('MONGO_PWD')
        )

    def open_spider(self,spider):
        self.client = pymongo.MongoClient(host=self.mongo_uri,username=self.mongo_user,password=self.mongo_pwd)
        self.db = self.client[self.mongo_db]

    def process_item(self,item,spider):
        name = item.collection
        #如果是用户信息，根据uid进行更新
        if isinstance(item,Useritem):
            self.db[name].update({'uid':item.get('uid')},{'$set':item},True)
        #如果是微博详情，根据weibo_id进行更新
        if isinstance(item,Weiboitem):
            self.db[name].update({'weibo_id':item.get('weibo_id')},{'$set':item},True)
        return item

    def close_spider(self,spider):
        self.client.close()



# 保存到MySQL
from twisted.enterprise import adbapi   #enterprise:事业、企业
import MySQLdb.cursors

class MysqlTwistedPipline(object):

    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host = settings["MYSQL_HOST"],					#host、db、user、passwd...必须写死 ，和底层代码一一对应 （passwd  password）
            db = settings["MYSQL_DATABASE"],					#因此下边的table不能传入
            user = settings["MYSQL_USER"],
            passwd = settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)
        return cls(dbpool)

    def process_item(self, item, spider):
        #使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider) #处理异常
        return item

    def handle_error(self, failure, item, spider):
        # 处理异步插入的异常
        print (failure)

    def do_insert(self, cursor, item):
        #执行具体的插入
        #根据不同的item 构建不同的sql语句并插入到mysql中
        data = dict(item)
        keys = ','.join(data.keys())
        values = ','.join(['%s']*len(data))
        sql = 'insert into %s(%s) value(%s)'%(item.collection,keys,values)		#数据库表名从items.py	详见P545
        cursor.execute(sql, tuple(data.values()))

class Fanscount_2_int():
    #将粉丝数转换为int类型

    def parse_number(self, date):
        # if re.match('\d+', date):
        #     date = int(date)
        if re.match('\d+万', date):
            date = int(re.match('(\d+)', date).group(1))*10000
        elif re.match('\d+亿', date):
            date = int(re.match('(\d+)', date).group(1))*100000000
        elif re.match('\d+', date):
            date = int(date)
        return date

    def process_item(self, item, spider):
        fans_count = item.get('fans_count')
        if fans_count:
            item['fans_count'] = self.parse_number(fans_count)
            print(item['fans_count'])
        return item

class TimePipeline():
    #设置爬取时间
    def process_item(self, item, spider):
        if isinstance(item, Useritem) or isinstance(item, Weiboitem):
            now = time.strftime('%Y-%m-%d %H:%M', time.localtime())
            item['crawled_at'] = now
        return item

class CleanTimePipeline():

    def parse_time(self, date):
        if re.match('刚刚', date):
            date = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))
        if re.match('\d+分钟前', date):
            minute = re.match('(\d+)', date).group(1)
            date = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time() - float(minute) * 60))
        if re.match('\d+小时前', date):
            hour = re.match('(\d+)', date).group(1)
            date = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time() - float(hour) * 60 * 60))
        if re.match('昨天.*', date):
            date = re.match('昨天(.*)', date).group(1).strip()
            date = time.strftime('%Y-%m-%d',time.localtime(time.time() - 24 * 60 * 60)) + ' ' + date
        if re.match('\d{2}-\d{2}', date):
            date = time.strftime('%Y-', time.localtime()) + date
        return date

    def process_item(self, item, spider):
        created_time = item.get('created_at')
        #发布时间可能为空，防止出现  KeyError: 'created_at'
        if created_time:
            item['created_at'] = self.parse_time(created_time)
        return item