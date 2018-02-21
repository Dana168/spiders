# -*- coding: utf-8 -*-
import scrapy
from tutorial.items import TutorialItem

class ExampleSpider(scrapy.Spider):
    name = 'example'
    start_urls = ['https://stackoverflow.com/questions?sort=votes']


    def parse(self, response):
        headers= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
 #       for href in response.css('.question-summary h3 a::attr(href)'):
  #          full_url = response.urljoin(href.extract())
   #         yield scrapy.Request(full_url,headers=headers,callback=self.parse_question)
        for url in self.start_urls:
            yield scrapy.Request(url,headers=headers,callback=self.parse_question)

    def parse_question(self, response):
        item=TutorialItem()
        questions = response.css('div.question-summary')
        for question in questions:
            item['votes'] = question.xpath(".//div[@class='votes']//strong/text()").extract_first()
            item['title'] = question.xpath(".//a[@class='question-hyperlink']/text()").extract_first()
            item['answers'] = question.xpath(".//div[ contains(@class, 'answered')]/strong/text()").extract_first()
            item['views'] = question.xpath(".//div[contains(@class, 'views')]/@title").extract_first()
            item['tags'] = question.xpath(".//div[contains(@class, 'tags')]/a/text()").extract()
            yield item  
