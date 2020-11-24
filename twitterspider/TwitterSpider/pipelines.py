# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from TwitterSpider.items import TweetItem, CommentItem
import pymongo

class TwitterspiderPipeline(object):
    def __init__(self):
        self.mongo_client1 = pymongo.MongoClient("mongodb://localhost:27017").twitter.tweet
        self.mongo_client2 = pymongo.MongoClient("mongodb://localhost:27017").twitter.comments
        self.mongo_client3 = pymongo.MongoClient("mongodb://localhost:27017").twitter.userinfo

    def process_item(self, item, spider):
        if isinstance(item, TweetItem):
            self.process_insertdb(item, self.mongo_client1,'id_str')
        elif isinstance(item, CommentItem):
            self.process_insertdb(item, self.mongo_client2,'comment_id')
        else:
            self.process_insertdb(item, self.mongo_client3, 'hash_id')
        return item


    def process_insertdb(self, item,mongo_client,hash_id):
        result = mongo_client.find_one({hash_id: item[hash_id]})
        if not result:
            mongo_client.insert_one(dict(item))


