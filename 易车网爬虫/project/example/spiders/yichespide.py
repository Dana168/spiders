# -*- coding: utf-8 -*-
import scrapy
import example.items
import selenium
import selenium.webdriver
import lxml
import   lxml.etree
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class taocheSpider(scrapy.Spider):
    name = 'yichetesteep14'
    allowed_domains = ['taoche.com']
    def start_requests(self):
        #模拟浏览器，随机浏览器,翻页功能
        for  i  in range(1,51):
            url="http://shenzhen.taoche.com/all/?page="+str(i)
            yield scrapy.Request( url,
            headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0"})

    def parse(self, response):
        #print(response.body)  ajax.动态数据，需要进入静态页面

        mytree = lxml.etree.HTML(response.body)
        # myres = mytree.xpath('//div[@id="container_base"]//div[@data-state="1"]')
        # print(len(myres))
        # for m in myres:
        mhref = mytree.xpath('//div[@class="item_details"]/h3/a/@href')

        print(mhref)
        for  i   in  range(len(mhref)):
            myitem=example.items.CaijinghexunItem()
            myitem["href"]=mhref[i]
            #self.log(myitem["name"] + "   " + myitem["url"])
            yield scrapy.Request(myitem["href"],meta={"meta":myitem}, #传递数据
                                 callback=self.parse_page, #进入下一级页面
                                 headers={
                                     'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0"})

    def  parse_page(self,response):
        print('get: ',response.url) #链接
        mytree = lxml.etree.HTML(response.body.decode('utf-8','ignore'))  # 解析代码
        # print(pagedata)
        #print(response.body) #页面代码
        # myitem = response.meta['meta'] #取出数据

        myname = mytree.xpath('//div[@class="summary-title"]/h1/text()')[0]
        myres = mytree.xpath('//div[@class="summary-attrs"]//dt')
        for data in myres:
            blist = data.xpath('//dd/text()')[0:4]
        yiitem = example.items.yicheItem()
        yiitem['carname']=myname
        yiitem['cardtime']=blist[0]
        yiitem['miliage'] = blist[1]
        yiitem['volume'] = blist[2]
        yiitem['salecity'] = blist[3]
        yield  yiitem

        #
        # dcap = dict(DesiredCapabilities.PHANTOMJS)  # 处理无界面浏览器
        # # dcap["phantomjs.page.settings.userAgent"]=("Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.23 Mobile Safari/537.36")
        # dcap["phantomjs.page.settings.userAgent"] = (
        #     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0"
        # )
        # driver = selenium.webdriver.PhantomJS(
        #     executable_path=r"C:\Users\Tsinghua-yincheng\Desktop\tools\phantomjs-2.1.1-windows\bin\phantomjs.exe",
        #     desired_capabilities=dcap)
        # #driver=selenium.webdriver.PhantomJS(r"C:\Users\Tsinghua-yincheng\Desktop\tools\phantomjs-2.1.1-windows\bin\phantomjs.exe")
        # #driver=selenium.webdriver.Chrome()
        # driver.get(response.url)
        # pagedata=driver.page_source #抓取渲染的网页源码代码
        # driver.close()
        #
        # mytree=lxml.etree.HTML(pagedata) #解析代码
        # print(pagedata)
        #
        # myitem["hits"]=mytree.xpath("//span[@id=\"articleClickCount\"]/text()")[0]
        # myitem["comment"]=mytree.xpath("//span[@id=\"articleCommentCount\"]/text()")[0]
        # self.log( myitem["name"]+"   "+myitem["hits"]+"   "+myitem["comment"])
        # yield  myitem


