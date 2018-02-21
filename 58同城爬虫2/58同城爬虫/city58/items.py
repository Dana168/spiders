# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class zufangItem(scrapy.Item):
    # define the fields for your item here like:
    housename1= scrapy.Field()
    housetype1=scrapy.Field()
    housearea1=scrapy.Field()
    infos1= scrapy.Field()
    housemoney1=scrapy.Field()


class ershoufangItem(scrapy.Item):
    # define the fields for your item here like:
    housename2= scrapy.Field()
    housetype2=scrapy.Field()
    housearea2=scrapy.Field()
    infos2= scrapy.Field()
    housemoney2=scrapy.Field()
    pricestatus2=scrapy.Field()
    pass

class shangyefangItem(scrapy.Item):
    # define the fields for your item here like:
    housename3= scrapy.Field()
    housetype3=scrapy.Field()
    housearea3=scrapy.Field()
    housemoney3=scrapy.Field()
    pricestatus3=scrapy.Field()
    pass

class carsItem(scrapy.Item):
    # define the fields for your item here like:
    carimg=scrapy.Field()
    cartype=scrapy.Field()
    carstatus=scrapy.Field()
    carmoney=scrapy.Field()



