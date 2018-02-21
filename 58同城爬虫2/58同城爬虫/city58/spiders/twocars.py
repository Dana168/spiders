# -*- coding: utf-8 -*-
#
import urllib

import re
import requests

import lxml
import lxml.etree
import scrapy
from scrapy.spiders import Rule,CrawlSpider
from scrapy.linkextractors import LinkExtractor
from city58 import items






class chinatwocarsMongoSpider(CrawlSpider):
    name = 'car_mongo'
    allowed_domains = ['quanguo.58.com']
    start_urls = ["http://quanguo.58.com/ershouche/pn1/"]
    rules=(Rule(LinkExtractor(allow=r"http://quanguo.58.com/ershouche/pn\d+/"),follow=True,callback="parse_request"),)
    custom_settings = {
        'ITEM_PIPELINES': {'city58.pipelines2.chinatwocarsPipeline': 400}
    }

    def parse_request(self,response):
        res = response.text
        res = lxml.etree.HTML(res)
        reslist=res.xpath("//div[@id=\"infolist\"]/table[@class=\"tbimg kcc_tsys\"]//tr")
        for res in reslist:
                carItems=items.carsItem()
                carItems["carimg"]=res.xpath(".//td[@class=\"img\"]/a/img//@src")
                carItems["cartype"]=res.xpath(".//td[@class=\"t\"]/a[1]//text()")
                carItems["carstatus"]=res.xpath(".//td[@class=\"t\"]/p//text()")
                carItems["carmoney"]=res.xpath(".//td[@class=\"tc\"]//text()")
                yield carItems





