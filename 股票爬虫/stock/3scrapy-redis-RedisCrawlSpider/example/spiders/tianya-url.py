# -*- coding: utf-8 -*-
import scrapy
import  re

import example.items  #引用外部文件
from scrapy.linkextractors import LinkExtractor #链接提取
from scrapy.spiders import CrawlSpider, Rule  #提取网页URL的功能，规则
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy_redis.spiders import RedisMixin

class TianyaSpider(RedisCrawlSpider):
    name = 'tianya_nimei'
    redis_key = 'tianya_nimei:start_urls'
    rules=(
        Rule(LinkExtractor(".*?shtml"),callback="parse_item",follow=True),
        )


    def set_crawler(self,crawer):
        CrawlSpider.set_crawler(self,crawer) #设置默认爬去
        RedisMixin.setup_redis(self) #url由redis



    def parse_item(self, response):
        print(response.url)
        pagedata=response.body.decode("gbk","ignore")
        regex=re.compile(r"([A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4})",re.IGNORECASE) #预编译正则
        emaillist=regex.findall(pagedata) #抓取所有的邮箱
 
     
        for   mail in  emaillist:
            myitem=example.items.mailItem()
            myitem["email"]=mail
            myitem["url"]=response.url
            yield myitem




       

