# -*- coding: utf-8 -*-
import selenium
import selenium.webdriver
import lxml
import lxml.etree
from selenium.webdriver.common.by import By
import re
import requests
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

# 抓取个股首页的【资助流向url】
def getFundFlowUrls(stockUrls):
    fundFlowUrls=[]
    headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}
    for each in stockUrls:
        pagedata = requests.get(each,headers=headers).content.decode("utf-8")
        print(type(pagedata))
        mytree=lxml.etree.HTML(pagedata)
        # fundFlow=mytree.xpath("//*[@class=\"f10-menu m-t\"]//a[4]/text()")
        fundHref=mytree.xpath("//*[@class=\"f10-menu m-t\"]//a[4]/@href")
        print(fundHref,"__________________")
        fundFlowUrl="https://gupiao.baidu.com"+str(fundHref)
        fundFlowUrls.append(fundFlowUrl)
    print(fundFlowUrls)
    return fundFlowUrls


# 抓取个股【资金流向（fundFlowUrl）页面的详细信息】
def getFundFlowInfo(fundFlowUrls):
    # regex=re.compile("\d+",re.IGNORECASE)
    for each in fundFlowUrls:
        pagedata=requests.get(each).content.decode("utf-8")
        mytree=lxml.etree.HTML(pagedata)

        # 单日汇总
        name=mytree.xpath("//*[@class=\"border data-table _dailyFunds\"]/tbody/tr//td[1]/a/text()")
        changeRate=mytree.xpath("//*[@class=\"border data-table _dailyFunds\"]/tbody/tr//td[2]/text()")[0].strip()
        totalFundNum=mytree.xpath("//*[@class=\"border data-table _dailyFunds\"]/tbody/tr//td[3]/text()")[0].strip()
        flowRate=mytree.xpath("//*[@class=\"border data-table _dailyFunds\"]/tbody/tr//td[4]/text()")[0].strip()
        maniFundNum=mytree.xpath("//*[@class=\"border data-table _dailyFunds\"]/tbody/tr//td[5]/text()")[0].strip()
        retailFundNum=mytree.xpath("//*[@class=\"border data-table _dailyFunds\"]/tbody/tr//td[6]/text()")[0].strip()
        mainParticipationRate=mytree.xpath("//*[@class=\"border data-table _dailyFunds\"]/tbody/tr//td[7]/text()")[0].strip()
        print(name,changeRate,totalFundNum,flowRate,maniFundNum,retailFundNum,mainParticipationRate)
    return name,changeRate,totalFundNum,flowRate,maniFundNum,retailFundNum,mainParticipationRate
if __name__ == '__main__':
    url="http://quote.eastmoney.com/stocklist.html#sz"
    stockNums=getStockName(url)
    stockUrls=stockUrls(stockNums)
    fundFlowUrls=getFundFlowUrls(stockUrls)
    getFundFlowInfo(fundFlowUrls)