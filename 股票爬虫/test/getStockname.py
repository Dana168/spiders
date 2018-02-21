# -*- coding: utf-8 -*-
import requests
import lxml
import lxml.etree
import re
import redis

# 东方财富网（http://quote.eastmoney.com/stocklist.html#sz）抓取股票的名称和代码
def getStockName(url):
    pagedata=requests.get(url).content.decode("gbk")
    # print(pagedata)
    mytree=lxml.etree.HTML(pagedata)
    namelist=mytree.xpath("//*[@id=\"quotesearch\"]/ul//li/a/text()")
    # print(namelist)
    newNameList=[]
    stockNums=[]
    regex = re.compile(r'(\S)+\((6|3|0)\d{5}\)',re.IGNORECASE)
    for name in namelist:
        hasMached = regex.match(name)
        if hasMached:
            stockNum=re.split(r'[(,)]',name)[1]
            newNameList.append(name)
            stockNums.append(stockNum)
            print(stockNums)
    # print(newNameList)
    return stockNums

'''
URL类型：
    # “0”开头
    "https://gupiao.baidu.com/stock/sz002156.html"
    # “3”开头
    "https://gupiao.baidu.com/stock/sz300676.html"
    # “6”开头
    "https://gupiao.baidu.com/stock/sh601989.html"
'''

# 根据规律拼接待爬去的个股的url
def stockUrls(stockNums):
    url="https://gupiao.baidu.com/stock/"
    stockUrls=[]
    for num in stockNums:
        if num.startswith("6"):
            stockUrl=url+"sh"+num+".html"
            stockUrls.append(stockUrl)
        else:
            stockUrl=url+"sz"+num+".html"
            stockUrls.append(stockUrl)
    print(stockUrls,"______________________________________")
    return stockUrls

# 存入redis
def saveStockUrls(stockUrls):
    StockRedis = redis.Redis(host="127.0.0.1", port=6379,db=0)
    for stockUrl in stockUrls:
        print(stockUrl)
        StockRedis.lpush("stock:start_urls",stockUrl)

# 抓取个股首页的【资助流向url】
def getFundFlowUrls(stockUrls):
    fundFlowUrls=[]
    for each in stockUrls:
        pagedata=requests.get(each).content.decode("utf-8")
        mytree=lxml.etree.HTML(pagedata)
        # fundFlow=mytree.xpath("//*[@class=\"f10-menu m-t\"]//a[4]/text()")
        fundHref=mytree.xpath("//*[@class=\"f10-menu m-t\"]//a[4]/@href")
        fundFlowUrl="https://gupiao.baidu.com"+str(fundHref[0])
        fundFlowUrls.append(fundFlowUrl)
    print(fundFlowUrls)
    return fundFlowUrls




if __name__ == '__main__':
    url = "http://quote.eastmoney.com/stocklist.html#sz"
    stockNums=getStockName(url)
    stockUrls=stockUrls(getStockName(url))
    saveStockUrls(stockUrls)
    getFundFlowUrls(stockUrls)

