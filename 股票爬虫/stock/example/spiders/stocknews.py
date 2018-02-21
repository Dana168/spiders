from scrapy_redis.spiders import RedisSpider
import example.items
import re
import redis
import scrapy
import requests
import lxml
import lxml.etree
class StockSpider(RedisSpider):

    name = 'stocknews'
    # redis_key = 'stock:testnews_url'
    redis_key = 'stock:newsUrl2'

    def __init__(self, *args, **kwargs):

        domain = kwargs.pop('https://gupiao.baidu.com/stock/', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(StockSpider, self).__init__(*args, **kwargs)

    def parse(self,response):
        pagedata=requests.get(response.url).content.decode("utf8")
        # print(pagedata)
        mytree=lxml.etree.HTML(pagedata)
        self.news=mytree.xpath("//*[@id=\"app-wrap\"]/div[1]/div[1]/div[2]//p[@class=\"t-indent\"]/text()")
        stockitem = example.items.StockItem()
        stockitem["news"]=self.news
        yield stockitem