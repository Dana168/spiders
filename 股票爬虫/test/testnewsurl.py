# -*- coding: utf-8 -*-
import selenium
import selenium.webdriver
import time
import lxml
import lxml.etree
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

# 拼接要抓取的个股【url】
def getUrl(stockNums):
    url = "https://gupiao.baidu.com/stock/"
    stockUrls = []
    for num in stockNums:
        if num.startswith("6"):
            stockUrl=url+"sh"+num+".html"
            stockUrls.append(stockUrl)
        else:
            stockUrl=url+"sz"+num+".html"
            stockUrls.append(stockUrl)
    return stockUrls

# 抓取个股的【新闻】【公告】【研报】三个页面的【标题】和【超链接】
def getEveryPage(stockNums):
    driver=selenium.webdriver.Chrome()
    stockUrls=getUrl(stockNums)
    url="https://gupiao.baidu.com"
    titleList=[]
    urlList=[]
    for each in stockUrls:
        driver.get(each)
        time.sleep(3)


        # 实现【新闻】【公告】【研报】三栏翻页
        for i in range(1,4):
            rule = "//*[@id=\"app-wrap\"]/div[4]/div[4]/ul/li[" + str(i) + "]"
            elem = driver.find_element(By.XPATH,rule)
            print(elem,"____________________________")
            elem.click()
            time.sleep(3)


            # 实现每一栏翻页：
            # 1、抓取lastPageNumber
            webdata = driver.page_source
            mytree=lxml.etree.HTML(webdata)
            num=mytree.xpath("//*[@id=\"app-wrap\"]/div[4]/div[5]/div//a[8]/text()")[0]
            # print(num)
            # 2、翻页
            for k in range(0,eval(num)-1):
                nextRule="//*[@id=\"app-wrap\"]/div[4]/div[5]/div/a[last()-1]"
                next = driver.find_element(By.XPATH, nextRule)
                # print(next,"****************************")
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
                        print(newsTitle, newsUrl)
                    except:
                        pass
                    titleList.append(newsTitle)
                    urlList.append(newsUrl)

    driver.close()
    return titleList,urlList


time.sleep(10)
stockNums=["601989"]
getEveryPage(stockNums)




