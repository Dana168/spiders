# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Scrapy58Item(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    titleurl = scrapy.Field()
    room = scrapy.Field()
    add = scrapy.Field()
    money = scrapy.Field()


