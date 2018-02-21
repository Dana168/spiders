from scrapy_redis.spiders import RedisSpider
import example.items
import redis
import scrapy
import selenium
import selenium.webdriver
import time
import lxml
import lxml.etree
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

class StockSpider(RedisSpider):

    name = 'stocknewsurl'
    redis_key = 'stock:start_urls2'

    def __init__(self, *args, **kwargs):

        domain = kwargs.pop('https://gupiao.baidu.com/stock/', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(StockSpider, self).__init__(*args, **kwargs)


    def parse(self,response):
        url = "https://gupiao.baidu.com"
        driver = selenium.webdriver.Chrome()
        driver.get(response.url)
        time.sleep(3)

        newsTitleList=[]
        newsUrlList=[]
        # 实现【新闻】【公告】【研报】三栏翻页
        for i in range(1, 4):
            rule = "//*[@id=\"app-wrap\"]/div[4]/div[4]/ul/li[" + str(i) + "]"
            elem = driver.find_element(By.XPATH, rule)
            print(elem, "开始抓取第",i,"栏")
            elem.click()
            time.sleep(3)

            # 实现每一栏翻页：
            # 1、抓取lastPageNumber
            webdata = driver.page_source
            mytree = lxml.etree.HTML(webdata)
            num=mytree.xpath("//*[@id=\"app-wrap\"]/div[4]/div[5]/div//a[last()-2]/text()")[0]
            # num = mytree.xpath("//*[@id=\"app-wrap\"]/div[4]/div[5]/div//a[8]/text()")[0]
            print(num,"共",num,"页")
            # 2、翻页
            for k in range(0, eval(num) - 1):
                nextRule = "//*[@id=\"app-wrap\"]/div[4]/div[5]/div/a[last()-1]"
                next = driver.find_element(By.XPATH, nextRule)
                print(next, "下一页")
                next.click()
                time.sleep(5)

                # 爬取每一栏每一页的【标题】和【url】
                for j in range(0, 10):
                    pagedata = driver.page_source
                    soup = BeautifulSoup(pagedata, "xml")
                    try:
                        newsTitle = soup.find_all('h4', {'class': 'text-ellipsis'})[j].string
                        newsUrl = soup.find_all('h4', {'class': 'text-ellipsis'})[j].a['href']
                        newsUrl = url + newsUrl
                        print("元素",newsTitle, newsUrl)
                        newsTitleList.append(newsTitle)
                        newsUrlList.append(newsUrl)
                        print("列表",newsTitleList,newsUrlList)

                    except:
                        pass
        driver.close()
        time.sleep(5)
        for i in range(len(newsTitleList)):
            stockitem = example.items.StockItem()
            stockitem["newsTitle"] = newsTitle
            stockitem["newsUrl"] = newsUrl
        print("结束66666666666666666666666666666666666666666666666")
        yield stockitem


