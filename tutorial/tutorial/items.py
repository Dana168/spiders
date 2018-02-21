# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    votes=scrapy.Field()
    title=scrapy.Field()
    answers=scrapy.Field()
    views=scrapy.Field()
    tags=scrapy.Field()
    pass
