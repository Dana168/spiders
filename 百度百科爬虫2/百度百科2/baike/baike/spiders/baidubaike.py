# -*- coding: utf-8 -*-
import scrapy
import baike.items
import re
from bs4 import  BeautifulSoup
from  scrapy.spider import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
import os
from aip import AipNlp

""" 你的 APPID AK SK """
APP_ID = '10314238'
API_KEY = 'kMBzbEGokFY3sfc5g3dqldcU'
SECRET_KEY = 'yd7uDNg5040rD7inpOm5mDgtFfeGNGd1 '

class BaidubaikeSpider(CrawlSpider):
    name = 'baidubaike'
    allowed_domains = ['baidu.com']
    start_urls = ['https://baike.baidu.com/item/%E8%9C%97%E9%B8%A2']
    pagelinks =LinkExtractor(allow=("/item/.*"))
    rules =[Rule(pagelinks,callback="parse_item",follow=True)]


    def gettitle(self,pagedata):
        soup = BeautifulSoup(pagedata,"html.parser")
        list1 = soup.find_all("h1")
        list2 = soup.find_all("h2")
        if len(list1) != 0 and len(list2)!=0:
            return (list1[0].text,list2[0].text)
        elif len(list1)!=0 and len(list2)==0:
            return list1[0].text
        else:
            return None

    def getcontent(self,pagedata):
        soup = BeautifulSoup(pagedata,"html.parser")
        summary = soup.find_all("div",class_="lemma-summary")
        if len(summary)!=0:
            return summary[0].get_text()
        else:
            return None

    def parse_item(self, response):
        pagedata = response.body
        url = response.url
        baikeitem = baike.items.BaikeItem()
        baikeitem["name"] = str(self.gettitle(pagedata))
        content=str(self.getcontent(pagedata))

        # content = self.parse_comment(url)
        content = content.replace("\u200b", "")
        content = content.replace("\n", "")
        content = content.replace("\xa0", "")
        content = content.replace("\u4260", "")
        baikeitem["content"] = content
        aipNlp = AipNlp(APP_ID, API_KEY, SECRET_KEY)
        result = aipNlp.sentimentClassify(content)

        sentiment = '情感极性分类：' + str(result['items'][0]['sentiment'])
        confidence = '置信度：' + str(result['items'][0]['confidence'])
        positive_prob = '积极类别的概率：' + str(result['items'][0]['positive_prob'])
        negative_prob = '消极类别的概率：' + str(result['items'][0]['negative_prob'])
        baikeitem["sentiment_minute"]=sentiment
        baikeitem["confidence_minute"]=confidence
        baikeitem["positive_prob_minute"]=positive_prob
        baikeitem["negative_prob_minute"]=negative_prob

        baikeitem["url"] = response.url
        yield baikeitem


