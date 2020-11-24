# -*- coding: utf-8 -*-
import datetime
import json
from hashlib import md5
from urllib.parse import quote

import scrapy
from TwitterSpider.items import TweetItem, CommentItem


class Twitter1Spider(scrapy.Spider):
    name = 'twitter_search'
    url_api = "https://twitter.com/i/api/2/search/adaptive.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_ext_alt_text=true&include_quote_count=true&include_reply_count=1&tweet_mode=extended&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&send_error_codes=true&simple_quoted_tweet=true&q={keyword}&tweet_search_mode=live&count=20&query_source=typed_query&pc=1&spelling_corrections=1&ext=mediaStats%2ChighlightedLabel"
    comment_api = "https://twitter.com/i/api/2/timeline/conversation/{id_str}.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_ext_alt_text=true&include_quote_count=true&include_reply_count=1&tweet_mode=extended&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&send_error_codes=true&simple_quoted_tweet=true&count=20&include_ext_has_birdwatch_notes=false&ext=mediaStats%2ChighlightedLabel"
    next_comment_api = "https://api.twitter.com/2/timeline/conversation/{id_str}.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_ext_alt_text=true&include_quote_count=true&include_reply_count=1&tweet_mode=extended&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&send_error_codes=true&simple_quoted_tweet=true&referrer=tweet&controller_data=DAACDAAFDAABDAABDAABCgABAAAAAAAAAAAAAAwAAgoAAQAAAAAAAAABCgACALz4GwCn3T4LAAMAAAAIZWxlY3Rpb24AAAAAAA%3D%3D&count=20&cursor={cursor}&include_ext_has_birdwatch_notes=false&ext=mediaStats%2ChighlightedLabel"
    first_url = "https://twitter.com/i/api/2/timeline/profile/{user_id}.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_ext_alt_text=true&include_quote_count=true&include_reply_count=1&tweet_mode=extended&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&send_error_codes=true&simple_quoted_tweet=true&include_tweet_replies=false&count=20&userId={user_id}&ext=mediaStats%2ChighlightedLabel"
    next_url = "https://twitter.com/i/api/2/timeline/profile/{user_id}.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_ext_alt_text=true&include_quote_count=true&include_reply_count=1&tweet_mode=extended&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&send_error_codes=true&simple_quoted_tweet=true&include_tweet_replies=false&count=20&cursor={cursor}&userId={user_id}&ext=mediaStats%2ChighlightedLabel"
    #设置爬取的关键词
    keywords = ["world of warcraft"]
    #设置爬取几天内的数据，如爬取近7天的数据
    day = 7

    def start_requests(self):
        for keyword in self.keywords:
            headers = self.settings['TWITTER_HEADERS']
            url = self.url_api.format(keyword=keyword)
            yield scrapy.Request(url,
                                  headers=headers,
                                  meta={"keyword":keyword,"headers":headers},
                                  dont_filter=True)


    def parse(self, response):
        keyword = response.meta['keyword']
        headers = response.meta['headers']
        tweet_info = json.loads(response.body.decode())
        tweets = tweet_info['globalObjects']['tweets']
        user_datas = tweet_info['globalObjects']['users']
        for post_id,status in tweets.items():
            created_time = self.format_time(status['created_at'])
            if created_time <= (datetime.datetime.now() - datetime.timedelta(days=self.day)).strftime('%Y-%m-%d %H:%M:%S'):
                break
            item = TweetItem()
            user_id = status['user_id_str']
            item['user'] = user_datas[user_id]['name']
            item['user_id'] = user_id
            item['post_time'] = created_time
            item['content'] = status['full_text']
            item['comment_num'] = status['reply_count']
            item['repost_num'] = status['retweet_count']
            item['like_num'] = status['favorite_count']
            id_str = status['id_str']
            item['id_str'] = id_str
            url = f'https://twitter.com/{user_datas[user_id]["screen_name"]}/status/{status["id_str"]}'
            item['url'] = url
            item['keyword'] = keyword
            item['ts'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            item['hash_id'] = id_str
            yield item
            comment_url = self.comment_api.format(id_str=id_str)
            yield scrapy.Request(comment_url,
                                 callback=self.parse_comment,
                                 headers=headers,
                                 meta={'keyword': keyword,"dont_merge_cookies":True,
                                       "id_str":id_str,"comment_num":status['reply_count'],
                                       "headers":headers}, dont_filter=True)

    def parse_comment(self, response):
        keyword = response.meta['keyword']
        headers = response.meta['headers']
        page = response.meta.get('page',1)
        comment_num = response.meta['comment_num']
        id_str = response.meta['id_str']
        tweet_info = json.loads(response.body.decode())
        tweets = tweet_info['globalObjects']['tweets']
        user_datas = tweet_info['globalObjects']['users']
        for post_id,status in tweets.items():
            item = CommentItem()
            user_id = status['user_id_str']
            item['comment_id'] = status['id_str']
            item['conversation_id'] = id_str
            item['user'] = user_datas[user_id]['name']
            item['user_id'] = user_id
            item['reply_time_dt'] = self.format_time(status['created_at'])
            item['content'] = status['full_text']
            item['reply_num'] = status['retweet_count']
            item['repost_num'] = status['retweet_count']
            item['like_num'] = status['favorite_count']
            item['ts'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            item['keyword'] = keyword
            item['tweet_id'] = id_str
            item['hash_id'] =item['comment_id']
            yield item

        #一页前20条评论，可以算出总共要翻多少页
        pages = int(comment_num) // 20 +1
        if page < pages:
            page+=1
            cursor = tweet_info['timeline']['instructions'][0]['addEntries']['entries'][-1]['content']['operation']['cursor']['value']
            next_url = self.next_comment_api.format(id_str=id_str,cursor=quote(cursor))
            yield scrapy.Request(next_url,callback=self.parse_comment,
                                  headers=headers,
                                  meta={"headers":headers,"page":page,'keyword': keyword,
                                        "id_str":id_str,"comment_num":comment_num},
                                  dont_filter=True)



    def format_time(self, dt):
        dt_obj = datetime.datetime.strptime(dt, '%a %b %d %H:%M:%S %z %Y').astimezone(tz=None)
        return dt_obj.strftime('%Y-%m-%d %H:%M:%S')