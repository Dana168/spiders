from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy_redis.spiders import RedisCrawlSpider
import lxml.etree
import scrapy
import re
from bs4 import BeautifulSoup
from example import items
from scrapy_redis.spiders import RedisMixin
from scrapy.spiders import CrawlSpider


class MyCrawler(RedisCrawlSpider):
    """Spider that reads urls from redis queue (myspider:start_urls)."""
    name = 'tudou_redis'
    redis_key = 'tudou_redis:start_urls'

    rules = (Rule(LinkExtractor(allow=r"/category/c_\d+_p_\d+\.html?"),
                  callback="parse_videolist", follow=True),)

    def set_crawler(self, crawer):
        CrawlSpider.set_crawler(self, crawer)  # 设置默认爬去
        RedisMixin.setup_redis(self)  # url由redis

    def parse_videolist(self, response):
        data = response.body
        # print(data)
        mytree = lxml.etree.HTML(data)
        linelist = mytree.xpath("//div[@class=\"td-col\"]")
        # movie_url =""
        for line in linelist:
            myitem = items.TudouItem()
            myitem["cover_page"]=line.xpath("./div[1]/div/img/@src")[0]
            movie_url= "http:"+line.xpath("./div[1]/div/div/a/@href")[0]
            # print(movie_url)
            myitem["movie_name"] =line.xpath("./div[1]/div/div/a/@title")[0]
        # yield scrapy.Request(movie_url, callback=self.parse_dsj)
            yield scrapy.Request(movie_url, callback=self.parse_video,meta={"meta": myitem})

    def parse_video(self, response):
        myitem = response.meta['meta']
        data = response.body
        mytree = lxml.etree.HTML(data)
        if mytree.xpath("//div[@class=\"td-play__videoinfo__details-box__desc\"]/text()"):
            content = response.xpath("//div[@class=\"td-play__videoinfo__details-box__desc\"]/text()")[0].extract()
        else:
            content =""
        myitem["movie_about"] =content
        linelist = mytree.xpath("//div[@class=\"td-listbox__list__item--show\"]")
        movie_utllist = []
        for line in linelist:
            nurl = "http:" + line.xpath("./a/@href")[0]
            title = line.xpath("./a/@title")[0]
            movie_utllist.append((nurl, title))

        myitem["movie_url"] = movie_utllist
        yield myitem
        pass


