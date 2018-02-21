# -*- coding: utf-8 -*-

import scrapy
import scrapy58.items
from scrapy.spiders import CrawlSpider


class ZufangSpider(CrawlSpider):
    name = 'zufang'
    allowed_domains = ['sz.58.com']
    start_urls = ['http://sz.58.com/chuzu/pn1']

    def parse(self, response):
        print(response.url)
        datalist = response.xpath("//*[@class=\"listUl\"]/li")

        for data in datalist:
            zfitem = scrapy58.items.Scrapy58Item()
            zfitem["title"] = data.xpath("./div[2]/h2/a/text()").extract()
            zfitem["titleurl"] = data.xpath("./div[2]/h2/a/@href").extract()
            zfitem["room"] = data.xpath("./div[2]/p[1]/text()").extract()
            zfitem["add"] = data.xpath("./div[2]/p[2]/a[1]/text()").extract()
            zfitem["money"] = data.xpath("./div[3]/div[2]/b/text()").extract()
            yield zfitem