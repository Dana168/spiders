﻿# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BaidubaikeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # 标题
    title = scrapy.Field()
    # 内容
    content = scrapy.Field()
    # 链接
    url = scrapy.Field()
