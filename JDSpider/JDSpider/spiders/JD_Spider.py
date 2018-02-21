# - * - coding: utf-8 - * -

__author__ = "Alexan"

from scrapy.spiders import CrawlSpider
from JDSpider.items import JdspiderItem
from scrapy.selector import Selector
from scrapy.http import Request
import requests
import re, json

class JdSpider(CrawlSpider):
    name = "JDSpider"
    redis_key = "JDSpider:start_urls"
    start_urls = ["http://book.jd.com/booktop/0-0-0.html?category=1713-0-0-0-10001-1#comfort"]

    def parse(self, response):
        item = JdspiderItem()
        selector = Selector(response)
        Books = selector.xpath('/html/body/div[8]/div[2]/div[3]/div/ul/li')
        for each in Books:
            num = each.xpath('div[@class="p-num"]/text()').extract()
            bookName = each.xpath('div[@class="p-detail"]/a/text()').extract()
            author = each.xpath('div[@class="p-detail"]/dl[1]/dd/a[1]/text()').extract()
            press = each.xpath('div[@class="p-detail"]/dl[2]/dd/a/text()').extract()

            temphref = each.xpath('div[@class="p-detail"]/a/@href').extract()
            temphref = str(temphref)
            BookID = str(re.search('com/(.*?)\.html',temphref).group(1))

            json_url = 'http://p.3.cn/prices/mgets?skuIds=J_' + BookID
            r = requests.get(json_url).text
            data = json.loads(r)[0]
            price = data['m']
            PreferentialPrice = data['p']

            item['number'] = num
            item['bookName'] = bookName
            item['author'] = author
            item['press'] = press
            item['BookID'] = BookID
            item['price'] = price
            item['PreferentialPrice'] = PreferentialPrice

            yield item

        nextLink = selector.xpath('/html/body/div[8]/div[2]/div[4]/div/div/span/a[7]/@href').extract()
        if nextLink:
            nextLink = nextLink[0]
            import urlparse
            nextLink=urlparse.urljoin(response.url,nextLink)
            print(nextLink)
            yield Request(nextLink,callback=self.parse)
