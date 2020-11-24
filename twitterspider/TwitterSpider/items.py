# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class TweetItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    user = Field()
    name = Field()
    user_id = Field()
    post_time = Field()
    content = Field()
    comment_num = Field()
    repost_num = Field()
    like_num = Field()
    id_str = Field()
    url = Field()
    keyword = Field()
    game = Field()
    ts = Field()
    hash_id = Field()

    # def __repr__(self):
    #     return '============Tweet Saved=============='


class CommentItem(Item):
    comment_id = Field()
    conversation_id = Field()
    url = Field()
    user = Field()
    user_id = Field()
    reply_time_dt = Field()
    content = Field()
    reply_num = Field()
    repost_num = Field()
    like_num = Field()
    game = Field()
    keyword = Field()
    tweet_id = Field()
    ts = Field()
    hash_id = Field()

    # def __repr__(self):
    #     return '=================Comment Saved=============='
