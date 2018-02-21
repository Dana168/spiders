# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
import pymongo
from datetime import datetime

class ExamplePipeline(object):
    def __init__(self):
        self.file = open('baike1.txt','wb')
        client = pymongo.MongoClient(host='127.0.0.1',port=27017)
        self.db = client
        self.users = self.db["baidubaike1"]
    def __del__(self):
        self.file.close()
    def process_item(self, item, spider):
        text = str(item) + "\r\n"
        self.file.write(text.encode("utf-8", "ignore"))
        self.file.flush()
        item["crawled"] = datetime.utcnow()
        item["spider"] = spider.name
        self.users["baidu"].insert({"name": item["name"], "content": item["content"], "url": item["url"]})
        return item



