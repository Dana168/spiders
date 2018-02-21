# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
from datetime import datetime
import pymongo

class ExamplePipeline(object):
    def  __init__(self):
        client = pymongo.MongoClient("mongodb://Hans:111111@10.36.132.18:27017")
        self.db = client
        self.users = self.db["tudou"]  # 新建一个数据库
    def process_item(self, item, spider):
        item["crawled"] = datetime.utcnow()
        item["spider"] = spider.name
        #插入数据
        self.users["tudou"].insert({"cover_page": item["cover_page"], "movie_name": item["movie_name"], "movie_url": item["movie_url"],
                                    "movie_about": item["movie_about"], "crawled": item["crawled"], "spider": item["spider"]})
        return item
    def __del__(self):
        self.db.close() #关闭数据库

    # def process_item(self, item, spider):
    #     item["crawled"] = datetime.utcnow()
    #     item["spider"] = spider.name
    #     while True:
    #         with open(spider.name +".txt","a+") as self.file:
    #             self.file.write(str(item)+"\r\n")
    #             self.file.flush()
    #             if not str(item):
    #                 break
    #         return item
