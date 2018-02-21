# - * - coding: utf-8 - * -

from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector
from DouBanSpider.items import DoubanspiderItem

class DouBan(CrawlSpider):
    name = 'DouBan'
    redis_key = 'douban:start_urls'
    start_urls = ['https://movie.douban.com/top250']

    url = 'https://movie.douban.com/top250'

    def parse(self, response):
        item = DoubanspiderItem()
        selector = Selector(response)
        Movies = selector.xpath('//div[@class="info"]')
        for eachMovie in Movies:
            title = eachMovie.xpath('div[@class="hd"]/a/span[@class="title"]/text()').extract()
            movieInfo = eachMovie.xpath('div[@class="bd"]/p/text()').extract()
            star = eachMovie.xpath('div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()').extract()
            quote = eachMovie.xpath('div[@class="bd"]/p[@class="quote"]/span/text()').extract()

            item['title'] = title
            item['movieInfo'] = ';'.join(movieInfo)
            item['star'] = star
            item['quote'] = quote
            # 提交item
            yield item
        nextLink = selector.xpath('//span[@class="next"]/link/@href').extract()
        if nextLink:
            nextLink = nextLink[0]
            print(nextLink)
            yield Request(self.url + nextLink,callback=self.parse)
