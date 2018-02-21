# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join


class TudouItem(Item):
    cover_page = Field()
    movie_name = Field()
    movie_url = Field()
    movie_about =Field()
    crawled = Field()
    spider = Field()


