# -*- coding: utf-8 -*-
import scrapy
import urllib
import urllib.request
import lxml
import lxml.etree
from  sinaChina import items

class SinachinaspiderSpider(scrapy.Spider):
    name = 'sinaChinaSpider'
    allowed_domains = ['sina.com.cn']
    start_urls = ['http://news.sina.com.cn/guide/']

    def parse(self, response):
        parenturls = response.xpath("//div[@class=\"clearfix\"]")
        myitems=[]

        for parenturl in parenturls:

            if len(myitems)>10: #缩短测试时间
                break


            level1 = ""
            level2 = ""
            level3 = ""
            if len(parenturl.xpath("./h3/a/text()")) == 0:
                if len(parenturl.xpath("./h3/span/text()")) == 0:
                    level1=parenturl.xpath("./h3/text()").extract()[0]
                else:
                    level1 =parenturl.xpath("./h3/span/text()").extract()[0]
            else:
                level1=parenturl.xpath("./h3/a/text()").extract()[0]
            print(level1)
            lines = parenturl.xpath("./ul//li")
            for line in lines:
                level2=line.xpath("./a/text()").extract()[0]
                print("----",level2)
                baseurl=line.xpath("./a/@href").extract()[0]

                data = urllib.request.urlopen(baseurl).read().decode("utf-8","ignore")
                mytree = lxml.etree.HTML(data)
                links = mytree.xpath("//div[@class=\"second-nav\"]/div/div//a")
                for line in links:
                    level3=line.xpath("./text()")[0]
                    print("--------",level3)

                    myitem = items.SinachinaItem()
                    myitem["url"]=line.xpath("./@href")[0]
                    print(myitem["url"])
                    myitem["level1"] =level1
                    myitem["level2"] =level2
                    myitem["level3"] =level3
                    myitems.append(myitem)
                    #yield scrapy.Request(url=myitem["url"],meta={"meta":myitem},callback=self.parse_level3)
        #print("-----------------------------------------------------------------")
        for  myitem in myitems:
            yield scrapy.Request(url=myitem["url"], meta={"meta": myitem}, callback=self.parse_level3)
            #yield scrapy.Request(myitem["url"],callback=self.parse_url)


    def parse_url(self,response):
        print("####################", response.url)


    def parse_level3(self, response):
        print("####################",response.url)
        myitem =response.meta['meta']
        links = response.xpath("//ul[@class=\"list_009\"]//li")
        for line in links:
            everyurl=line.xpath("./a/@href").extract()[0]
            yield  scrapy.Request(everyurl,meta={"meta2":myitem},callback=self.pargepage)
        #翻页
        url=response.url
        urllist = url.split("/")
        nexturl = response.xpath("//span[@class=\"pagebox_next\"]/a/@href").extract()[0]
        nexturl = nexturl[2:]
        newurl = ""
        for i in range(len(urllist) - 1):
            newurl += urllist[i]
            newurl += "/"
        newurl += nexturl
        print("---------",newurl)

        if len(response.xpath("//ul[@class=\"list_009\"]//li")) == 0:  # 没有数据终止递归
            pass
        else:

            yield scrapy.Request(newurl,meta={"meta":myitem},callback=self.parse)







    def pargepage(self,response):
        myitem=response.meta['meta2']
        title = response.xpath("//h1[@id=\"artibodyTitle\"]/text()").extract()[0]
        #print(title)
        content = response.xpath("//div[@id=\"artibody\"]//p/text()").extract()
        lastcontent=""
        for line in content:
            lastcontent+=line
            #print(line)
        myitem["title"]=title
        myitem["content"]=lastcontent
        return   myitem