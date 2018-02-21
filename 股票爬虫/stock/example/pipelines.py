# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
from datetime import datetime
import redis

class ExamplePipeline(object):
    def __init__(self):
        self.StockRedis = redis.Redis(host="127.0.0.1", port=6379, db=0)
    def __del__(self):
        pass
    def process_item(self, item, spider):
        if spider.name=='stocknewsurl':
            self.StockRedis.lpush("stock:newsTitle2", item["newsTitle"])
            self.StockRedis.lpush("stock:newsUrl2", item["newsUrl"])
        elif spider.name=='stockfundflowurl':
            self.StockRedis.lpush("stock:fundFlowUrl2", item["fundFlowUrl"])
        elif spider.name=='stockfundflow':
            self.StockRedis.lpush("stock:name2", item["name"])
            self.StockRedis.lpush("stock:totalFundNum2", item["totalFundNum"])
            self.StockRedis.lpush("stock:flowRate2", item["flowRate"])
            self.StockRedis.lpush("stock:maniFundNum2", item["maniFundNum"])
            self.StockRedis.lpush("stock:retailFundNum2", item["retailFundNum"])
            self.StockRedis.lpush("stock:mainParticipationRate2", item["mainParticipationRate"])
        elif spider.name=='stocknews':
            self.StockRedis.lpush("stock:news2", item["news"])

        item["crawled"] = datetime.utcnow()
        item["spider"] = spider.name
        return item
