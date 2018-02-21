# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES settings
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

class chinatwocarsPipeline(object):
    def __init__(self):
        self.client = pymongo.MongoClient(host="10.36.132.60", port=27017)
        self.user= self.client["china58twocars"]
    def process_item(self, item, spider):
        img = "".join(item["carimg"]).strip().replace("\n", "").replace("\t", "")
        type = "".join(item["cartype"]).strip().replace("\n", "").replace("\t", "")
        status = "".join(item["carstatus"]).strip().replace("\n", "").replace("\t", "")
        money= "".join(item["carmoney"]).strip().replace("\n", "").replace("\t", "")
        self.user["chinatwocars"].insert({"img":img,"type":type,"status":status,"money":money})
        return item
    def __del__(self):
        self.client.close()

