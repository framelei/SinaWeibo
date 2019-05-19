# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from SinaWeibo.items import Weiboitem,Useritem
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
            date = time.strftime('%Y-%m-%d', time.localtime() - 24 * 60 * 60) + ' ' + date
        if re.match('\d{2}-\d{2}', date):
            date = time.strftime('%Y-', time.localtime()) + date
        return date

    def process_item(self, item, spider):
        created_time = item['created_at']
        #发布时间可能为空，防止出现  KeyError: 'created_at'
        if created_time:
            item['created_at'] = self.parse_time(created_time)
            return item