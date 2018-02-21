# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from ganji import items

class PhoneSpider(CrawlSpider):
    count=0
    name = 'phone'
    allowed_domains = ['ganji.com']
    start_urls = ['http://sz.ganji.com/shouji/o1/']
    # start_urls = ['http://zhuanzhuan.ganji.com/detail/919855528017510406z.shtml']
    rules = (
        Rule(LinkExtractor(allow=r"http://sz.ganji.com/shouji/o\d+/")),
        Rule(LinkExtractor(allow=r"http://zhuanzhuan.ganji.com/detail/\d+z.shtml"),callback="parse_content_one"),
        Rule(LinkExtractor(allow=r"http://sz.ganji.com/shouji/\d+x.htm"),callback="parse_content_two"),
        # Rule(LinkExtractor(allow=r"http://sz.ganji.com/shouji/31752303704124x.htm"),callback="parse_content_two"),
        # Rule(LinkExtractor(allow=r"http://zhuanzhuan.ganji.com/detail/919855528017510406z.shtml"),callback="parse_content_one"),
    )
    # def start_requests(self):
    #     headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"}
    #     for i in range(1,56):
    #         url="http://sz.ganji.com/shouji/o"+str(i)+"/"
    #         request=scrapy.Request(url,headers=headers)
    #         yield request

    def parse_content_one(self, response):
        items_list=items.GanjiItem()
        self.count+=1
        print("+++++++++++++",response)
        title=response.css(".info_titile::text")
        money=response.css(".price_now > i::text")
        content=response.css(".baby_kuang > p::text")
        print(title.extract()[0])
        print(money.extract()[0])
        content = "#".join(content.extract())
        print(content)
        items_list["title"]=title.extract()[0]
        items_list["money"]=money.extract()[0]
        items_list["content"]=content
        yield items_list
        print("--------------------",self.count)
        pass
    def parse_content_two(self, response):
        items_list = items.GanjiItem()
        self.count+=1
        print("===========",response)
        title=response.css(".col-cont h1::text")
        money=response.css(".det-infor > li > i::text")
        content=response.css(".second-sum-cont span::text")
        print(title.extract()[0])
        print(money.extract()[0])
        content="#".join(content.extract())
        print(content)
        items_list["title"] = title.extract()[0]
        items_list["money"] = money.extract()[0]
        items_list["content"] = content
        yield items_list
        print("--------------------",self.count)

        pass

