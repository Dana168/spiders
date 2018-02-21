# -*- coding: utf-8 -*-
import scrapy


class ZhihuspiderSpider(scrapy.Spider):
    name = 'zhihuspider'
    allowed_domains = ['zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    def parse(self, response):
        pass
