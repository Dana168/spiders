# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
from datetime import datetime
import pymongo
class ExamplePipeline(object):

    def __init__(self):
        self.client = pymongo.MongoClient(host='127.0.0.1', port=27017)
        self.db = self.client['yiche1']
        self.user = self.db['carinfo1']
        pass
    def __del__(self):
        self.client.close()

    def process_item(self, item, spider):
        item["crawled"] = datetime.utcnow()
        item["spider"] = spider.name
        self.user.insert({'carname':item['carname'],'cardtime':item['cardtime'],'miliage':item['miliage'],'volume':item['volume'],'salecity':item['salecity']})



        return item
 