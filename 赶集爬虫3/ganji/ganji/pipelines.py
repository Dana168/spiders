# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
class GanjiPipeline(object):
    def __init__(self):
        self.mfile=open(r"result.txt","w")
        # self.conn=pymongo.MongoClient()
        # print(1111111111111111111111111111111111111)
        pass
    def __del__(self):
        self.mfile.close()
        # self.conn.close()
        # print(33333333333333333333333333333333333333)
        pass
    def process_item(self, item, spider):
        # self.conn.ganji.phone.insert({"title":item["title"],"money":item["money"],"content":item["content"]})
        mstr=item["title"]+" ---- "+item["money"]+" ---- "+item["content"]+"\n"
        self.mfile.write(mstr)
        # print(22222222222222222222222222222222222222)
        return item
