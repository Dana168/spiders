# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES settings
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from city58.items import zufangItem,ershoufangItem,shangyefangItem

class ShenzhenhousePipeline(object):
    def __init__(self):
        self.client = pymongo.MongoClient(host="10.36.132.60", port=27017)
        self.user1 = self.client["shenzhen58house"]
        self.user2 = self.client["shenzhen58house"]
        self.user3= self.client["shenzhen58house"]
    def process_item(self, item, spider):
        if zufangItem == item.__class__:
            name="".join(item["housename1"]).strip().replace("\n","").replace("\t","")
            type="".join(item["housetype1"]).strip().replace("\n","").replace("\t","")
            area="".join(item["housearea1"]).strip().replace("\n","").replace("\t","")
            info="".join(item["infos1"]).strip().replace("\n","").replace("\t","")
            money = "".join(item["housemoney1"]).strip().replace("\n", "").replace("\t", "")
            self.user1["shenzhenzufang"].insert({"name":name,"type":type,"area":area,"info":info,"money":money})

        if ershoufangItem == item.__class__:
            name = "".join(item["housename2"]).strip().replace("\n", "").replace("\t", "")
            type = "".join(item["housetype2"]).strip().replace("\n", "").replace("\t", "")
            area = "".join(item["housearea2"]).strip().replace("\n", "").replace("\t", "")
            info = "".join(item["infos2"]).strip().replace("\n", "").replace("\t", "")
            money = "".join(item["housemoney2"]).strip().replace("\n", "").replace("\t", "")
            price= "".join(item["pricestatus2"]).strip().replace("\n", "").replace("\t", "")
            self.user2["shenzhenershoufang"].insert({"name":name,"type":type,"area":area,"info":info,"money":money,"price":price})

        if shangyefangItem==item.__class__:
            name="".join(item["housename3"]).strip().replace("\n","").replace("\t","")
            type="".join(item["housetype3"]).strip().replace("\n","").replace("\t","")
            area="".join(item["housearea3"]).strip().replace("\n","").replace("\t","")
            money = "".join(item["housemoney3"]).strip().replace("\n", "").replace("\t", "")
            price = "".join(item["pricestatus3"]).strip().replace("\n", "").replace("\t", "")
            self.user3["shenzhenshangyefang"].insert({"name":name,"type":type,"area":area,"money":money,"price":price})
        return item
    def __del__(self):
        self.client.close()

