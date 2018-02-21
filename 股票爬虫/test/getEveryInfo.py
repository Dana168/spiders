# -*- coding: utf-8 -*-
import requests
import lxml
import lxml.etree

# 抓取【新闻】【公告】【研报】中每条新闻超链接页面的信息
def getEveryInfo(urlList):
    for url in urlList:
        pagedata=requests.get(url).content.decode("utf8")
        mytree=lxml.etree.HTML(pagedata)
        infos=mytree.xpath("//*[@id=\"app-wrap\"]/div[1]/div[1]/div[2]//p[@class=\"t-indent\"]/text()")
        for each in infos:
            info=each.strip()
            print(info)

if __name__ == '__main__':
    urlList = ["https://gupiao.baidu.com/article/report/gaotime_notice_601989_3535970",
               "https://gupiao.baidu.com/article/abbfe6f5af5c49db57ee269a154c6991",
               "https://gupiao.baidu.com/article/SPDR330404",
               "https://gupiao.baidu.com/article/report/gaotime_notice_601989_3247110"]
    getEveryInfo(urlList)