# -*- coding: utf-8 -*-
import re
import scrapy
import json
from urllib.parse import quote

class UserinfoSpider(scrapy.Spider):
    name = 'userinfo'
    url_api = "https://twitter.com/i/api/graphql/jMaTS-_Ea8vh9rpKggJbCQ/UserByScreenName?variables=%7B%22screen_name%22%3A%22{screen_name}%22%2C%22withHighlightedLabel%22%3Atrue%7D"
    # comment_api = "https://twitter.com/i/api/2/timeline/conversation/{id_str}.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_ext_alt_text=true&include_quote_count=true&include_reply_count=1&tweet_mode=extended&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&send_error_codes=true&simple_quoted_tweet=true&count=20&include_ext_has_birdwatch_notes=false&ext=mediaStats%2ChighlightedLabel"
    following_api = "https://twitter.com/i/api/graphql/cu-dBcAhjEzWdJgzNrj1YA/Following?variables=%7B%22userId%22%3A%22{userId}%22%2C%22count%22%3A20%2C%22withHighlightedLabel%22%3Afalse%2C%22withTweetQuoteCount%22%3Afalse%2C%22includePromotedContent%22%3Afalse%2C%22withTweetResult%22%3Afalse%2C%22withUserResult%22%3Afalse%7D"
    next_following_api = "https://twitter.com/i/api/graphql/cu-dBcAhjEzWdJgzNrj1YA/Following?variables=%7B%22userId%22%3A%22{userId}%22%2C%22count%22%3A20%2C%22cursor%22%3A%22{cursor}%22%2C%22withHighlightedLabel%22%3Afalse%2C%22withTweetQuoteCount%22%3Afalse%2C%22includePromotedContent%22%3Afalse%2C%22withTweetResult%22%3Afalse%2C%22withUserResult%22%3Afalse%7D"

    next_follower_api = "https://twitter.com/i/api/graphql/r2R0IAcCNr8WkScmDhqDUA/Followers?variables=%7B%22userId%22%3A%22{userId}%22%2C%22count%22%3A20%2C%22cursor%22%3A%22{cursor}%22%2C%22withHighlightedLabel%22%3Afalse%2C%22withTweetQuoteCount%22%3Afalse%2C%22includePromotedContent%22%3Afalse%2C%22withTweetResult%22%3Afalse%2C%22withUserResult%22%3Afalse%7D"
    follower_api = "https://twitter.com/i/api/graphql/r2R0IAcCNr8WkScmDhqDUA/Followers?variables=%7B%22userId%22%3A%22{userId}%22%2C%22count%22%3A20%2C%22withHighlightedLabel%22%3Afalse%2C%22withTweetQuoteCount%22%3Afalse%2C%22includePromotedContent%22%3Afalse%2C%22withTweetResult%22%3Afalse%2C%22withUserResult%22%3Afalse%7D"

    headers = {
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
        "content-type": "application/json",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36",
        "x-csrf-token": "b638906b6557556107a57ea08b3d62c8c65de70efc45604729cdb1fb8507dc21ca71280cdba2f92ee286cb6e0535504f4e4050869e53312e19bc62450730319b2cb3cc724fd13220901c4e19c26ca349",
        "x-twitter-active-user": "yes",
        "x-twitter-auth-type": "OAuth2Session",
        "x-twitter-client-language": "en",
    }
    first_url = "https://twitter.com/i/api/2/timeline/profile/{user_id}.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_ext_alt_text=true&include_quote_count=true&include_reply_count=1&tweet_mode=extended&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&send_error_codes=true&simple_quoted_tweet=true&include_tweet_replies=false&count=20&userId={user_id}&ext=mediaStats%2ChighlightedLabel"
    next_url = "https://twitter.com/i/api/2/timeline/profile/{user_id}.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_ext_alt_text=true&include_quote_count=true&include_reply_count=1&tweet_mode=extended&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&send_error_codes=true&simple_quoted_tweet=true&include_tweet_replies=false&count=20&cursor={cursor}&userId={user_id}&ext=mediaStats%2ChighlightedLabel"
    cookies = {
    "_ga":"GA1.2.1402331764.1603453697",
    "des_opt_in":"Y",
    "dnt":"1",
    "kdt":"lBpP42UsD0C96Gbc2APX3Xwd2BPpdDSepZzagPyp",
    "remember_checked_on":"1",
    "eu_cn":"1",
    "personalization_id":"\"v1_xuLHbbFcQ/jnPMTrEAAimw==\"",
    "guest_id":"v1%3A160431694077568763",
    "twid":"u%3D1323227694935408641",
    "cd_user_id":"17588ddd78031d-0596250a2a7c01-303464-144000-17588ddd781480",
    "mbox":"PC#ae8f0c915499423ea4fa17a9a71cd200.38_0#1667564317|session#3529cc01a90f4291ba9cb365b9b2f785#1604320946",
    "external_referer":"padhuUp37zjgzgv1mFWxJ12Ozwit7owX|0|8e8t2xd8A2w%3D",
    "auth_token":"c88bd50fd6487def32488a596264e392b4d88efa",
    "ct0":"b638906b6557556107a57ea08b3d62c8c65de70efc45604729cdb1fb8507dc21ca71280cdba2f92ee286cb6e0535504f4e4050869e53312e19bc62450730319b2cb3cc724fd13220901c4e19c26ca349",
    "_gid":"GA1.2.243080580.1605894225",
    "lang":"en"
}



    #这里填写作者详情页链接
    user_urls = ["https://twitter.com/RyanCampbell89"]

    def start_requests(self):
        headers = self.settings['TWITTER_HEADERS']
        for url in self.user_urls:
            screen_name = url.split("com/")[-1]
            author_url = self.url_api.format(screen_name=screen_name)
            yield scrapy.Request(author_url,headers=headers,dont_filter=True,meta={"user_name":screen_name})

    def parse(self, response):
        user_name = response.meta['user_name']
        datas = json.loads(response.text)
        user_id = datas['data']['user']['rest_id']
        # following
        following_api = self.following_api.format(userId=user_id)
        yield scrapy.Request(following_api,callback=self.parse_post_list,
                              headers=self.headers,
                              meta={"user_id":user_id,"type":"following","user_name":user_name},
                              dont_filter=True,cookies=self.cookies)
        #follower
        follower_api = self.follower_api.format(userId=user_id)
        yield scrapy.Request(follower_api,callback=self.parse_post_list,
                              headers=self.headers,
                              meta={"user_id":user_id,"type":"followers","user_name":user_name},
                              dont_filter=True,cookies=self.cookies)


    def parse_post_list(self, response):
        type = response.meta['type']
        user_name = response.meta['user_name']
        user_id = response.meta['user_id']
        tweet_info = json.loads(response.body.decode())
        if type == "following":
            try:
                tweets = tweet_info['data']['user']['following_timeline']['timeline']['instructions'][2]['entries']
            except Exception:
                tweets = tweet_info['data']['user']['following_timeline']['timeline']['instructions'][0]['entries']
        else:
            try:
                tweets = tweet_info['data']['user']['followers_timeline']['timeline']['instructions'][2]['entries']
            except Exception:
                tweets = tweet_info['data']['user']['followers_timeline']['timeline']['instructions'][0]['entries']

        for status in tweets:
            try:
                item = {}
                item['user_name'] = user_name
                item['user'] = status['content']['itemContent']['user']['legacy']['screen_name']
                item['id'] = status['content']['itemContent']['user']['id']
                item['description'] = status['content']['itemContent']['user']['legacy']['description']
                item['favourites_count'] = status['content']['itemContent']['user']['legacy']['favourites_count']
                item['followers_count'] = status['content']['itemContent']['user']['legacy']['followers_count']
                item['friends_count'] = status['content']['itemContent']['user']['legacy']['friends_count']
                item['media_count'] = status['content']['itemContent']['user']['legacy']['media_count']
                item['statuses_count'] = status['content']['itemContent']['user']['legacy']['statuses_count']
                item['rest_id'] = status['content']['itemContent']['user']['rest_id']
                item['hash_id'] = str(user_id)+str(item['rest_id'])
                item['type'] = type
                yield item
            except:
                continue

        cursor = re.search('"content":{"entryType":"TimelineTimelineCursor","value":"(.*?)","cursorType":"Bottom"}}',response.text).group(1)
        if type == "following":
            next_url = self.next_following_api.format(userId=user_id,cursor=quote(cursor))
        else:
            next_url = self.next_follower_api.format(userId=user_id, cursor=quote(cursor))
        yield scrapy.Request(next_url,callback=self.parse_post_list,
                              headers=self.headers,cookies=self.cookies,
                              meta={"user_id":user_id,"type":type,"user_name":user_name},
                              dont_filter=True)

