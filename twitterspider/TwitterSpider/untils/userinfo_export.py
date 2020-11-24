#encoding:utf-8
#time:2020/11/17 20:23
import pymongo
import json
#根据你爬取的twitter修改这个名字
name = "RyanCampbell89"
mongo_client = pymongo.MongoClient(host="127.0.0.1",port=27017).twitter.userinfo
datas1 = mongo_client.find({},{"_id":0})
with open(f"{name}.json","w",encoding="utf-8") as f:
    for data in datas1:
        item = {}
        item['twitter_name'] = data['user_name']
        item[data['type']] = data['user']
        item['description'] = data['description']
        f.write(json.dumps(item,ensure_ascii=False)+"\n")
