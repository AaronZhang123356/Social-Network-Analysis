#encoding:utf-8
#time:2020/11/17 20:28
import pymongo
import json
mongo_client1 = pymongo.MongoClient(host="127.0.0.1",port=27017).twitter.tweet
mongo_client2 = pymongo.MongoClient(host="127.0.0.1",port=27017).twitter.comments

keyword = "world of warcraft"
datas1 = mongo_client1.find({"keyword":keyword},{"_id":0})
with open(f"{keyword}.json","w",encoding="utf-8") as f:
    for data in datas1:
        id_str = data['id_str']
        datas2 = mongo_client2.find({"tweet_id":id_str},{"_id":0})
        comment_list = []
        for data2 in datas2:
            item = {}
            item['name'] = data2['user']
            item['time'] = data2['reply_time_dt']
            item['comment'] = data2['content']
            comment_list.append(item)
        item2 = {}
        item2['keyword'] = keyword
        item2['name'] = data['user']
        item2['time'] = data['post_time']
        item2['post'] = data['content']
        item2['comment_num'] = data['comment_num']
        item2['like_num'] = data['like_num']
        item2['repost_num'] = data['repost_num']
        f.write(json.dumps(item2,ensure_ascii=False)+"\n")





