from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider,Rule
from bs4 import BeautifulSoup
from scrapy_redis.spiders import RedisCrawlSpider,RedisMixin
from example import items


from aip import AipNlp

""" 你的 APPID AK SK """
APP_ID = '10254125'
API_KEY = 'kLAAVDQnkFuIkAlAAPZFLNr6'
SECRET_KEY = 'f9AvFUbG6wVYF5PVvuSCmluwjVIN1ZKo'

aipNlp = AipNlp(APP_ID, API_KEY, SECRET_KEY)

class MyCrawler(RedisCrawlSpider):
    """Spider that reads urls from redis queue (myspider:start_urls)."""
    name = 'baike_redis'
    redis_key = 'baike_redis:start_urls'

    pagelinks = LinkExtractor(allow=("/item/.*"))
    rules = [Rule(pagelinks, callback="parse_item", follow=True)]

    def set_crawler(self, crawer):
        CrawlSpider.set_crawler(self, crawer)
        RedisMixin.setup_redis(self)

    def gettitle(self, pagedata):
        soup = BeautifulSoup(pagedata, "html.parser")
        list1 = soup.find_all("h1")
        list2 = soup.find_all("h2")
        if len(list1) != 0 and len(list2) != 0:
            return (list1[0].text, list2[0].text)
        elif len(list1) != 0 and len(list2) == 0:
            return list1[0].text
        else:
            return None

    def getcontent(self, pagedata):
        soup = BeautifulSoup(pagedata, "html.parser")
        summary = soup.find_all("div", class_="lemma-summary")
        if len(summary) != 0:
            return summary[0].get_text()
        else:
            return None

    def parse_item(self, response):
        pagedata = response.body
        # url = response.url
        baikeitem = items.BaidubaikeItem()
        baikeitem["name"] = str(self.gettitle(pagedata))
        baikeitem["content"] = str(self.getcontent(pagedata))
        baikeitem["url"] = response.url
        result = aipNlp.sentimentClassify(baikeitem["content"])
        sentiment = result['items'][0]['sentiment']
        confidence = result['items'][0]['confidence']
        positive_prob = result['items'][0]['positive_prob']
        negative_prob = result['items'][0]['negative_prob']
        baikeitem['sentiment'] = sentiment
        baikeitem['confidence'] = confidence
        baikeitem['positive_prob'] = positive_prob
        baikeitem['negative_prob'] = negative_prob
        yield baikeitem