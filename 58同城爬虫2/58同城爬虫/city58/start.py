#
import  scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from  city58.spiders.house import ShenzhenhouseMongoSpider
from  city58.spiders.twocars import chinatwocarsMongoSpider
settings = get_project_settings()
process = CrawlerProcess(settings=settings)
process.crawl(ShenzhenhouseMongoSpider)
process.crawl(chinatwocarsMongoSpider)
process.start()
