# -*- coding: utf-8 -*-
import re

import scrapy
import selenium.webdriver
from selenium.webdriver import DesiredCapabilities
import lxml
import lxml.etree
from  oschina import items


class OschinaSpider(scrapy.Spider):
    name = 'osChina'
    allowed_domains = ['oschina.net']

    # start_urls = ['http://www.oschina.net/project/zh']
    def start_requests(self):
        url = "https://www.oschina.net/project/zh"
        dcap = dict(DesiredCapabilities.PHANTOMJS)  # 处理无界面浏览器
        dcap["phantomjs.page.settings.userAgent"] = (
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0")
        driver = selenium.webdriver.PhantomJS(
            executable_path=r"D:\phantomjs-2.1.1-windows\bin\phantomjs.exe",
            desired_capabilities=dcap)
        driver.get(url)
        html = driver.page_source
        mytree = lxml.etree.HTML(html)
        myitem = items.OschinaItem()
        titleList = mytree.xpath("//div[@id=\"v-so\"]//a[@class=\"box menu vertical\"]//@title")
        urlList = mytree.xpath("//div[@id=\"v-sort\"]//a[@class=\"box menu vertical\"]//@href")
        # myitem["alltitle"] = titleList
        for a in urlList:
            newURL = "https://www.oschina.net" + a
            yield scrapy.Request(newURL, meta={"meta": myitem},  # 传递数据
                                 callback=self.parse,  # 进入下一级页面
                                 headers={
                                     'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0"})

    def parse(self, response):
        myitem = response.meta['meta']
        mytree = lxml.etree.HTML(response.body.decode("utf-8"))
        number = mytree.xpath("//div[@class=\"panel-list news-list\"]//footer//li[7]//text()")

        for i in range(1, int(number[0]) + 1):
            pageurl = response.url + "?p=" + str(i) + "#project-list"
            # print(newurl)
            yield scrapy.Request(pageurl, meta={"meta": myitem}, callback=self.get_content,
                                 headers={
                                     'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0"})

    def get_content(self, response):
        myitem = response.meta['meta']
        mytree = lxml.etree.HTML(response.body.decode("utf-8"))
        content = mytree.xpath("//div[@class = \"panel-list news-list\"]//a[@class=\"item\"]")
        for text in content:
            url = text.xpath("./@href")
            title = text.xpath(".//div[@class=\"title\"]//text()")
            summary = text.xpath(".//div[@class=\"summary\"]//text()")
            # time = text.xpath(".//footer//text()")
            myitem["url"] = url[0]
            myitem["title"] = title[0].strip() + title[1].strip()
            myitem["summary"] = summary[0].strip()
            # myitem["time"]=time[0].strip()+time[1].strip()+time[2].strip()+time[3].strip()
        yield myitem
