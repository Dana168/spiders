# -*- coding: utf-8 -*-
'''
Scrapy 框架爬取当当网 书籍信息  挖掘热门书籍标题 链接 及评论数
'''

import scrapy
from dangdang.items import  DangdangItem
from scrapy import Request
from scrapy.http import  request
class DdSpider(scrapy.Spider):
    name = 'dd'
    allowed_domains = ['dangdang.com']
    start_urls = ['http://dangdang.com/']

    def parse(self, response):
        item = DangdangItem()
        item['title'] = response.xpath("//a[@class ='pic']/@title").extract()
        item['link'] = response.xpath("//a[@class ='pic']/@href").extract()
        item['comment'] = response.xpath("//a[@class ='search_comment_num']/text()").extract()
        yield item
        for i in  range(2,101):
            url = "http://category.dangdang.com/pg"+str(i)+"-cp01.54.06.00.00.00.html"
            yield  Request(url,callback=self.parse)