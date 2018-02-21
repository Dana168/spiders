# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SinachinaItem(scrapy.Item):
    # define the fields for your item here like:
    url=scrapy.Field()
    level1=scrapy.Field()
    level2 = scrapy.Field()
    level3 = scrapy.Field() #文件夹的层级

    title = scrapy.Field() #标题，内容
    content=scrapy.Field()
    pass
