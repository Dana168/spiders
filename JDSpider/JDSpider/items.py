# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JdspiderItem(scrapy.Item):
    # define the fields for your item here like:
    #排名
    number = scrapy.Field()
    #图书名字
    bookName = scrapy.Field()
    #作者
    author = scrapy.Field()
    #出版社
    press = scrapy.Field()
    #图书id
    BookID = scrapy.Field()
    #正价
    price = scrapy.Field()
    #折扣价
    PreferentialPrice = scrapy.Field()







