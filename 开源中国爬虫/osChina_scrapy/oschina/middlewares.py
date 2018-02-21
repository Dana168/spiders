# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#aaa
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import selenium
from scrapy import signals
from selenium import webdriver
from  scrapy.http import HtmlResponse
from selenium.webdriver import DesiredCapabilities


# class LoginMiddleware(object):
#     def process_request(self,request,spider):
#         dcap = dict(DesiredCapabilities.PHANTOMJS)  # 处理无界面浏览器
#         dcap["phantomjs.page.settings.userAgent"] = (
#             "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0"
#         )
#         spider.browser = selenium.webdriver.PhantomJS(
#             executable_path=r"F:\qianfeng\codeAll\level3_python\Webpro\phantomjs-2.1.1-windows\bin\phantomjs.exe",
#             desired_capabilities=dcap)
#         spider.browser.get(request.url)
#         return HtmlResponse(url=spider.browser.current_url,  # 当前连接
#                             body=spider.browser.page_source,  # 源代码
#                             encoding="utf-8")
class OschinaSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
