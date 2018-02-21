# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join
class mailItem(Item):
    email=Field()
    url=Field()
    crawled = Field()
    spider = Field()
class shespiderItem(Item):
    title=Field()
    author=Field()
    reply=Field()
    crawled = Field()
    spider = Field()
class CaijinghexunItem(Item):
    href = Field()
    crawled = Field()
    spider = Field()
class yicheItem(Item):
    carname = Field()
    cardtime = Field()
    miliage = Field()
    volume = Field()
    salecity = Field()
    # href = Field()
    crawled = Field()
    spider=Field()

class ExampleItem(Item):
    name = Field()
    description = Field()
    link = Field()
    crawled = Field()
    spider = Field()
    url = Field()


class ExampleLoader(ItemLoader):
    default_item_class = ExampleItem
    default_input_processor = MapCompose(lambda s: s.strip())
    default_output_processor = TakeFirst()
    description_out = Join()
 