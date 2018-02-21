# Define here the models for your scraped items
#

from scrapy.item import Item, Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join
import scrapy
class StockItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    fundFlowUrl=scrapy.Field()
    name=scrapy.Field()
    changeRate=scrapy.Field()
    totalFundNum=scrapy.Field()
    flowRate=scrapy.Field()
    maniFundNum=scrapy.Field()
    retailFundNum=scrapy.Field()
    mainParticipationRate=scrapy.Field()
    newsTitle=scrapy.Field()
    newsUrl=scrapy.Field()
    news=scrapy.Field()
    crawled=scrapy.Field()
    spider=scrapy.Field()


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
