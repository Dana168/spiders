# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BaikeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    content = scrapy.Field()
    sentiment_minute = scrapy.Field()
    confidence_minute = scrapy.Field()
    positive_prob_minute = scrapy.Field()
    negative_prob_minute = scrapy.Field()
    url = scrapy.Field()
    pass
