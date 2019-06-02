# -*- coding: utf-8 -*-
import scrapy
import json
from urllib.parse import quote
from SinaWeibo.items import Useritem,Weiboitem


class WeiboSpider(scrapy.Spider):
    name = 'weibo'
    allowed_domains = ['m.weibo.cn']
    keyword = quote('天使投资人')
    start_urls = 'https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D17%26q%3D{keyword}&page={page}'
    weibo_url = 'https://m.weibo.cn/api/container/getIndex?uid={uid}&type=uid&containerid=107603{uid}&page={page}'


    def start_requests(self):
        userinfo_url = self.start_urls.format(keyword=self.keyword,page=1)
        yield scrapy.Request(userinfo_url,callback=self.parse_user,meta={'page':1})

    # 解析用户信息
    def parse_user(self,response):
        result = json.loads(response.text)
        if result.get('ok') and result.get('data').get('cards') and len(result.get('data').get('cards')) and result.get('data').get('cards')[-1].get('card_group'):
            # user_infos = result.get('data').get('cards').get('1').get('card_group')
            user_infos = result.get('data').get('cards')[-1].get('card_group')
            user_item = Useritem()
            for user_info in user_infos:
                user_item['uid'] = user_info.get('user').get('id')
                user_item['name'] = user_info.get('user').get('screen_name')
                user_item['description'] = user_info.get('desc1')
                user_item['follows_count'] = user_info.get('user').get('follow_count')
                user_item['fans_count'] = user_info.get('user').get('followers_count')
                user_item['cover'] = user_info.get('user').get('profile_image_url')
                user_item['weibo_url'] = user_info.get('scheme')
                # user_item['crawled_at'] = user_info.get('user').get('')
                #1、存储用户信息
                yield user_item

                #2、爬取下一页用户信息
                page = response.meta.get('page') +1
                userinfo_url = self.start_urls.format(keyword=self.keyword,page=page)
                yield scrapy.Request(userinfo_url,callback=self.parse_user,meta={'page':page})

                #3、爬取用户微博
                uid = user_item['uid'] = user_info.get('user').get('id')
                weibo_url = self.weibo_url.format(uid=uid,page=1)
                yield scrapy.Request(weibo_url,callback=self.parse_weibo,meta={'uid':uid,'page':1})

    #解析用户微博
    def parse_weibo(self,response):
        result = json.loads(response.text)
        if result.get('ok') and result.get('data').get('cards') and len(result.get('data').get('cards')):
            weibo_infos = result.get('data').get('cards')
            weibo_item = Weiboitem()
            for weibo_info in weibo_infos:
                mblog = weibo_info.get('mblog')
                if mblog:
                    weibo_item['uid'] = mblog.get('user').get('id')
                    weibo_item['nickname'] = mblog.get('user').get('screen_name')
                    weibo_item['reposts_count'] = mblog.get('reposts_count')
                    weibo_item['comments_count'] = mblog.get('comments_count')
                    weibo_item['attitudes_count'] = mblog.get('attitudes_count')
                    weibo_item['text'] = mblog.get('text')
                    weibo_item['raw_text'] = mblog.get('raw_text')
                    weibo_item['pictures'] = mblog.get('pics')
                    weibo_item['source'] = mblog.get('source')
                    weibo_item['created_at'] = mblog.get('created_at')
                    weibo_item['thumbnail'] = weibo_info.get('scheme')
                    weibo_item['weibo_id'] = mblog.get('mid')
                    #1、存储用户信息
                    yield weibo_item

                    #2、爬取下一页微博
                    uid = response.meta.get('uid')
                    page = response.meta.get('page') + 1
                    weibo_url = self.weibo_url.format(uid=uid,page=page)
                    yield scrapy.Request(weibo_url,callback=self.parse_weibo,meta={'uid':uid,'page':page})
