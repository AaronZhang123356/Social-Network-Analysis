# -*- coding: utf-8 -*-

# Scrapy settings for TwitterSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'TwitterSpider'

SPIDER_MODULES = ['TwitterSpider.spiders']
NEWSPIDER_MODULE = 'TwitterSpider.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'TwitterSpider (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False #不遵守

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 3  #三个线程同时抓取

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1  # 隔一秒
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 3
CONCURRENT_REQUESTS_PER_IP = 3 #没有也可以

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'TwitterSpider.middlewares.TwitterspiderSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'TwitterSpider.middlewares.ProxyMiddleware': 243,
 }

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'TwitterSpider.pipelines.TwitterspiderPipeline': 300,
}#保存文件，保存位置，'路径（文件名），类名，参数越低越优先'
RETRY_ENABLED = True #重试
RETRY_TIMES = 3
RETRY_HTTP_CODES = [429,404,403] #遇到这些重试
HTTPERROR_ALLOWED_CODES = [429,404,403] #允许错误的验证码
# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

SEARCH_URL_TEMPLATE = 'https://twitter.com/i/search/timeline?q={keyword}&src=typed&include_entities=1{max_position}' #配置的，具体变了
MAX_POSITION_URL = 'https://twitter.com/search?q={keyword}&src=typed_query'

# COMMENT_LATTER_URL = 'https://twitter.com/i/iamdevloper/conversation/1194562654284787712?include_available_features=1&include_entities=1&max_position=DAACDwABCgAAAAcQlAsvvFeQABCT8fVuFpABEJP8Z5DXsAAQlA2NjleQARCT8NRCl9AIEJSadJAWsAMQk_MdEZbgAQgAAwAAAAECAAQAAAA&reset_error_state=false'
COMMENT_LATTER_URL = '{prefix}/conversation/{tweet_id}?include_available_features=1&include_entities=1&max_position={max_position}&reset_error_state=false'

SEARCH_HEADERS = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cache-control': 'no-cache',
    'dnt': '1',
    'pragma': 'no-cache',
    'referer': 'https://twitter.com/search?q={keyword}&src=typed_query',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    'x-twitter-active-user': 'yes'
}

MAX_POSITION_HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cache-control': 'no-cache',
    'dnt': '1',
    'pragma': 'no-cache',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
}

COMMENT_LATTER_HEADERS = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cache-control': 'no-cache',
    'dnt': '1',
    'pragma': 'no-cache',
    'referer': 'https://twitter.com/iamdevloper/status/1194562654284787712',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36',
    'x-overlay-request': 'true',
    'x-previous-page-name': 'permalink',
    'x-requested-with': 'XMLHttpRequest',
    'x-twitter-active-user': 'yes'
}


TWITTER_HEADERS = {
"Host":'twitter.com',
"Connection":'keep-alive',
"Sec-Fetch-Mode":'cors',
"x-twitter-client-language":'zh-cn',
"User-Agent":'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36',
"authorization":'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
"Accept":'*/*',
"Sec-Fetch-Site":'same-origin',
"Accept-Language":'zh-CN,zh;q=0.9,en;q=0.8',
"x-guest-token":"1330337443585822720"
}

    
TWITTER_API_URL = 'https://api.twitter.com/1.1/search/tweets.json?q={keyword}&result_type=recent&count=100'
BEAR_TOKEN = 'Bearer AAAAAAAAAAAAAAAAAAAAAMBTBgEAAAAA2ujLLoyW9VAzhdc012jFHa97i%2BU%3D2Fw1ksB2m2xIqb1EPQRZQHx0IYg54a39vP3SNGG2vezqjE2ev9'



