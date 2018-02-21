# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo


class OschinaPipeline(object):
    def  __init__(self):
        self.file = open('data.txt','w')
        # self.client = pymongo.MongoClient(host="127.0.0.1",port=27017)
        # self.db = self.client.osChina
        # self.site = self.db.text
    # def __del__(self):
    #     # self.db.close()
    def process_item(self, item, spider):
        self.file.write(item["url"]+" # "+item["title"]+item["summary"]+'\n')
        # self.site.insert({"url":item["url"],"titile":item["title"],"summary":item["summary"]})
        return item
