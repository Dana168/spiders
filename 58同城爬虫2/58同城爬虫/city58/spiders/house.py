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






class ShenzhenhouseMongoSpider(CrawlSpider):
    name = 'house_mongo'
    allowed_domains = ['sz.58.com']
    custom_settings = {
        'ITEM_PIPELINES': {'city58.pipelines1.ShenzhenhousePipeline': 300}
    }
    # start_urls = ['http://newhouse.sz.fang.com/house/s/b9%s'%(i) for i in range(1,25)]
    start_urls = ["http://sz.58.com/chuzu/pn1/","http://sz.58.com/ershoufang/pn1/","http://sz.58.com/shangpucz/pn1/"]
    rules=(Rule(LinkExtractor(allow=r"http://sz.58.com/chuzu/pn\d+/"),follow=True,callback="parse_request1"),
           Rule(LinkExtractor(allow=r"http://sz.58.com/ershoufang/pn\d+/"), follow=True, callback="parse_request2"),
           Rule(LinkExtractor(allow=r"http://sz.58.com/shangpucz/pn\d+/"), follow=True, callback="parse_request3"),)

    def parse_request1(self,response):
        res = response.text
        res = lxml.etree.HTML(res)
        reslist=res.xpath("//div[@class= \"content\"]/div[@class=\"listBox\"]/ul[@class=\"listUl\"]//li")
        for res in reslist:
                zufangItems=items.zufangItem()
                zufangItems["housename1"]=res.xpath(".//div[@class=\"des\"]/h2/a//text()")
                zufangItems["housetype1"]=res.xpath(".//div[@class=\"des\"]/p[@class=\"room\"]//text()")
                zufangItems["housearea1"]=res.xpath(".//div[@class=\"des\"]/p[@class=\"add\"]//text()")
                zufangItems["infos1"]=res.xpath(".//div[@class=\"des\"]/div[@class=\"jjr\"]//text()")
                zufangItems["housemoney1"]=res.xpath(".//div[@class=\"listliright\"]/div[@class=\"money\"]//text()")
                # houseitems["pricestatus"]=res.xpath(".//div[@class=\"listliright\"]///text()")
                yield zufangItems

    def parse_request2(self,response):
        res = response.text
        res = lxml.etree.HTML(res)
        reslist=res.xpath("//div[@class= \"content-wrap\"]/div[@class=\"content-side-left\"]/ul[@class=\"house-list-wrap\"]//li")
        for res in reslist:
                ershoufangItems=items.ershoufangItem()
                ershoufangItems["housename2"]=res.xpath(".//div[@class=\"list-info\"]/h2[@class=\"title\"]/a//text()")
                ershoufangItems["housetype2"]=res.xpath(".//div[@class=\"list-info\"]/p[@class=\"baseinfo\"][1]//text()")
                ershoufangItems["housearea2"]=res.xpath(".//div[@class=\"list-info\"]/p[@class=\"baseinfo\"][2]//text()")
                ershoufangItems["infos2"]=res.xpath(".//div[@class=\"list-info\"]/div[@class=\"jjrinfo\"]//text()")
                ershoufangItems["housemoney2"]=res.xpath(".//div[@class=\"price\"]/p[@class=\"sum\"]//text()")
                ershoufangItems["pricestatus2"]=res.xpath(".//div[@class=\"price\"]/p[@class=\"unit\"]//text()")
                yield  ershoufangItems

    def parse_request3(self,response):
        res = response.text
        res = lxml.etree.HTML(res)
        reslist=res.xpath("//div[@class= \"content-wrap\"]/div[@class=\"content-side-left\"]/ul[@class=\"house-list-wrap\"]//li")
        for res in reslist:
                shangyefangItems=items.shangyefangItem()
                shangyefangItems["housename3"]=res.xpath(".//div[@class=\"list-info\"]/h2[@class=\"title\"]/a/span[@class=\"title_des\"]//text()")
                shangyefangItems["housetype3"]=res.xpath(".//div[@class=\"list-info\"]/p[@class=\"baseinfo\"][1]/span//text()")
                shangyefangItems["housearea3"]=res.xpath(".//div[@class=\"list-info\"]/p[@class=\"baseinfo\"][2]/span//text()")
                shangyefangItems["housemoney3"]=res.xpath(".//div[@class=\"price\"]/p[@class=\"sum\"]//text()")
                shangyefangItems["pricestatus3"]=res.xpath(".//div[@class=\"price\"]/p[@class=\"unit\"]//text()")
                yield shangyefangItems





