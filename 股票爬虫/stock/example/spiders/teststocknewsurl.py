from scrapy_redis.spiders import RedisSpider
import example.items
import selenium
import selenium.webdriver
import time
import lxml
import lxml.etree
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import threading


class StockSpider(RedisSpider):

    name = 'stock'
    redis_key = 'stock:start_urls'

    def __init__(self, *args, **kwargs):
        self.rlock = threading.RLock()
        self.newsTitles=[]
        self.newsUrls=[]
        self.stockitem = example.items.StockItem()
        # self.stockitem["newsTitle"] = []
        # self.stockitem["newsUrl"] = []
        domain = kwargs.pop('https://gupiao.baidu.com/stock/', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(StockSpider, self).__init__(*args, **kwargs)

    def fun(self,rule,response):
        driver = selenium.webdriver.Chrome()
        driver.get(response.url)
        time.sleep(3)
        urlRule = "https://gupiao.baidu.com"
        elem = driver.find_element(By.XPATH, rule)
        print(elem, "222222222222222222222222222222")
        elem.click()
        time.sleep(3)

        # 实现每一栏翻页：
        # 1、抓取lastPageNumber
        webdata = driver.page_source
        mytree = lxml.etree.HTML(webdata)
        num = mytree.xpath("//*[@id=\"app-wrap\"]/div[4]/div[5]/div//a[8]/text()")[0]
        print(num)
        # 2、翻页
        for k in range(0, eval(num) - 1):
            nextRule = "//*[@id=\"app-wrap\"]/div[4]/div[5]/div/a[last()-1]"
            next = driver.find_element(By.XPATH, nextRule)
            print(next, "****************************")
            next.click()
            time.sleep(5)

            # 爬取每一栏每一页的【标题】和【url】
            for j in range(0, 10):

                pagedata = driver.page_source
                soup = BeautifulSoup(pagedata, "xml")
                print("soup")
                try:
                    newsTitle = soup.find_all('h4', {'class': 'text-ellipsis'})[j].string
                    newsUrl = soup.find_all('h4', {'class': 'text-ellipsis'})[j].a['href']
                    print(newsTitle)
                    newsUrl = urlRule + newsUrl
                    print(newsUrl)
                    with self.rlock:
                        self.newsTitles.append(newsTitle)
                        self.newsUrls.append(newsUrl)
                        print(newsTitle, newsUrl,"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
                except:
                    pass
                print(self.newsTitles,"********",self.newsUrls,"***********")

        driver.close()
        time.sleep(10)

    def parse(self,response):

        # 实现【新闻】【公告】【研报】三栏翻页

        for i in range(1, 4):
            ts=[]
            rule = "//*[@id=\"app-wrap\"]/div[4]/div[4]/ul/li[" + str(i) + "]"
            # elem = driver.find_element(By.XPATH, rule)
            t=threading.Thread(target=self.fun, args=(rule,response))
            ts.append(t)
            for t in ts:
                t.start()
                t.join()
        for i in range(len(self.newsTitles)):
            print("开始存入：")
            # stockitem = example.items.StockItem()
            self.stockitem["newsTitle"] = self.newsTitle[i]
            self.stockitem["newsUrl"] = self.newsUrl[i]
            print("结束")
            yield self.stockitem

