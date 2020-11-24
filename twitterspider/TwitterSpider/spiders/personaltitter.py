# -*- coding: utf-8 -*-
import scrapy
import json
import datetime
from TwitterSpider.items import TweetItem, CommentItem
from urllib.parse import quote


class PersonaltitterSpider(scrapy.Spider):
    name = 'personaltitter'
    url_api = "https://twitter.com/i/api/graphql/jMaTS-_Ea8vh9rpKggJbCQ/UserByScreenName?variables=%7B%22screen_name%22%3A%22{screen_name}%22%2C%22withHighlightedLabel%22%3Atrue%7D"
    comment_api = "https://twitter.com/i/api/2/timeline/conversation/{id_str}.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_ext_alt_text=true&include_quote_count=true&include_reply_count=1&tweet_mode=extended&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&send_error_codes=true&simple_quoted_tweet=true&count=20&include_ext_has_birdwatch_notes=false&ext=mediaStats%2ChighlightedLabel"
    next_comment_api = "https://api.twitter.com/2/timeline/conversation/{id_str}.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_ext_alt_text=true&include_quote_count=true&include_reply_count=1&tweet_mode=extended&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&send_error_codes=true&simple_quoted_tweet=true&referrer=tweet&controller_data=DAACDAAFDAABDAABDAABCgABAAAAAAAAAAAAAAwAAgoAAQAAAAAAAAABCgACALz4GwCn3T4LAAMAAAAIZWxlY3Rpb24AAAAAAA%3D%3D&count=20&cursor={cursor}&include_ext_has_birdwatch_notes=false&ext=mediaStats%2ChighlightedLabel"

    first_url = "https://twitter.com/i/api/2/timeline/profile/{user_id}.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_ext_alt_text=true&include_quote_count=true&include_reply_count=1&tweet_mode=extended&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&send_error_codes=true&simple_quoted_tweet=true&include_tweet_replies=false&count=20&userId={user_id}&ext=mediaStats%2ChighlightedLabel"
    next_url = "https://twitter.com/i/api/2/timeline/profile/{user_id}.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_ext_alt_text=true&include_quote_count=true&include_reply_count=1&tweet_mode=extended&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&send_error_codes=true&simple_quoted_tweet=true&include_tweet_replies=false&count=20&cursor={cursor}&userId={user_id}&ext=mediaStats%2ChighlightedLabel"

    #这里填写作者详情页链接，可以填写多个作者
    user_urls = ["https://twitter.com/JustinAaronUH91"]

    #设置爬取几天内的数据，如爬取近7天的数据
    day = 7


    def start_requests(self):
        """
        根据user_urls中的链接获取user_id，使用user_id才能抓取数据
        """
        headers = self.settings['TWITTER_HEADERS']
        for url in self.user_urls:
            screen_name = url.split("com/")[-1]
            author_url = self.url_api.format(screen_name=screen_name)
            yield scrapy.Request(author_url,
                                  headers=headers,
                                  meta={"headers":headers,'name':screen_name},
                                  dont_filter=True)

    def parse(self, response):
        """
        获取到user_id,构造first_url，发起请求
        """
        headers = response.meta['headers']
        name = response.meta['name']
        datas = json.loads(response.text)
        user_id = datas['data']['user']['rest_id']
        first_url = self.first_url.format(user_id=user_id)
        yield scrapy.Request(first_url,callback=self.parse_post_list,
                              headers=headers,
                              meta={"user_id":user_id,"headers":headers,"page":1,"stop":False,'name':name},
                              dont_filter=True)


    def parse_post_list(self, response):
        """
        获取到个人主页下面的帖子信息，解析数据
        """
        page = response.meta['page']
        name = response.meta['name']
        stop = response.meta['stop']
        user_id = response.meta['user_id']
        headers = response.meta['headers']
        tweet_info = json.loads(response.body.decode())
        try:
            tweets = tweet_info['globalObjects']['tweets']
        except:
            print("token失效，换一个x-guest-token参数再试一下")
            return
        user_datas = tweet_info['globalObjects']['users']
        for post_id,status in tweets.items():
            created_time = self.format_time(status['created_at'])
            #如果发帖时间小于设定的时间，就不再往下抓了
            if created_time <= (datetime.datetime.now() - datetime.timedelta(days=self.day)).strftime('%Y-%m-%d %H:%M:%S'):
                stop = True
                break
            item = TweetItem()
            user_id1 = status['user_id_str']
            item['user'] = user_datas[user_id1]['name']
            item['user_id'] = user_id1
            item['post_time'] = created_time
            item['content'] = status['full_text']
            comment_num = status['reply_count']
            item['comment_num'] = comment_num
            item['repost_num'] = status['retweet_count']
            item['like_num'] = status['favorite_count']
            id_str = status['id_str']
            item['id_str'] = id_str
            url = f'https://twitter.com/{user_datas[user_id]["screen_name"]}/status/{status["id_str"]}'
            item['url'] = url
            item['name'] = name
            yield item

            #如果该帖子有评论就去抓取评论
            if int(comment_num):
                comment_url = self.comment_api.format(id_str=id_str)
                yield scrapy.Request(comment_url,
                                     callback=self.parse_comment,
                                     headers=headers,
                                     meta={"url":url,"id_str":id_str,"comment_num":comment_num,
                                           "page":1,"headers": headers}, dont_filter=True)

        tweet_post_nums = user_datas[user_id]['statuses_count'] #帖子总数
        pages = int(tweet_post_nums) // 20 +1  #获取帖子页数，然后遍历
        if page < pages and not stop: #如果还在需要爬取的时间内且总页数没有翻完，就继续翻页
            page+=1
            cursor = tweet_info['timeline']['instructions'][0]['addEntries']['entries'][-1]['content']['operation']['cursor']['value']
            next_url = self.next_url.format(user_id=user_id,cursor=quote(cursor))
            yield scrapy.Request(next_url,callback=self.parse_post_list,
                                  headers=headers,
                                  meta={"user_id":user_id,"headers":headers,"page":page,'name':name},
                                  dont_filter=True)


    def parse_comment(self, response):
        """
        解析提取评论
        """
        headers = response.meta['headers']
        comment_num = response.meta['comment_num']
        page = response.meta['page']
        id_str = response.meta['id_str']
        tweet_info = json.loads(response.body.decode())
        try:
            tweets = tweet_info['globalObjects']['tweets']
        except:
            print(tweet_info)
            return
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
            item['tweet_id'] = id_str
            yield item
        pages = int(comment_num) // 20 + 1 #获取评论页数
        print("当前页:", page)
        if page < pages:
            page += 1
            cursor = \
            tweet_info['timeline']['instructions'][0]['addEntries']['entries'][-1]['content']['operation']['cursor'][
                'value']
            next_url = self.next_comment_api.format(id_str=id_str, cursor=quote(cursor))
            yield scrapy.Request(next_url, callback=self.parse_comment,
                                 headers=headers,
                                 meta={"headers": headers, "page": page,
                                       "id_str": id_str, "comment_num": comment_num},
                                 dont_filter=True)


    def format_time(self, dt):
        dt_obj = datetime.datetime.strptime(dt, '%a %b %d %H:%M:%S %z %Y').astimezone(tz=None)
        return dt_obj.strftime('%Y-%m-%d %H:%M:%S')