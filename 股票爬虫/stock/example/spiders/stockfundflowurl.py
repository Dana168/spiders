from scrapy_redis.spiders import RedisSpider
import example.items
import re
import redis
import scrapy
import selenium
import selenium.webdriver
import lxml
import lxml.etree
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup



class StockSpider(RedisSpider):

    name = 'stockfundflowurl'
    # redis_key = 'stock:start_urlscopy'
    redis_key = 'stock:start_urls2'
    def __init__(self, *args, **kwargs):

        domain = kwargs.pop('https://gupiao.baidu.com/stock/', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(StockSpider, self).__init__(*args, **kwargs)


    def parse(self,response):
        self.fundHrefs = response.xpath("//*[@class=\"f10-menu m-t\"]//a[4]/@href").extract()
        print(self.fundHrefs)
        # StockRedis = redis.Redis(host="127.0.0.1", port=6379, db=0)
        self.fundFlowUrl="https://gupiao.baidu.com" +self.fundHrefs[0]
        # StockRedis.lpush("stock:fundFlowUrl", fundFlowUrl)
        print(self.fundFlowUrl,"资金流动url")
        stockitem = example.items.StockItem()
        stockitem["fundFlowUrl"] = self.fundFlowUrl
        print("结束66666666666666666666666666666666666666666666666")
        yield stockitem

