# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
from datetime import datetime

class ExamplePipeline(object):
    def __init__(self):
        self.file=open("1.txt","w")
    def __del__(self):
        self.file.close()
    def process_item(self, item, spider):
        item["crawled"] = datetime.utcnow()
        item["spider"] = spider.name
        self.file.write(str(item)) #写入，刷新，实时写入
        self.file.flush()
        print(item)
        return item
