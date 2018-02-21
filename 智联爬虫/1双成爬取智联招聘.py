# encoding:utf-8
import  urllib2
import urllib
import lxml
import lxml.etree
import re

import requests
import selenium  #测试框架
import selenium.webdriver #模拟浏览器
import time

def  geturllist(searchname):
    url="http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E6%B7%B1%E5%9C%B3&kw="+searchname+"&p=1&isadv=0"
    headers = {"User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0);"}
    pagetxt = requests.get(url, headers=headers).content
    myxml = lxml.etree.HTML(pagetxt.decode("utf-8", errors="ignore"))
    #number = eval(myxml.xpath("//*[@class=\"seach_yx\"]//span[@class=\"search_yx_tj\"]/em/text()")[0])
    number = eval(myxml.xpath("//*[@class=\"seach_yx\"]//span[@class=\"search_yx_tj\"]/em/text()")[0])
    urllist=[]
    if number % 60 == 0:
        pnumber=number % 60
        for i in range(1, pnumber):
            urllist.append("http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E6%B7%B1%E5%9C%B3&kw="+searchname+"&p="+str(i)+"&isadv=0")
    else:
        pnumber = number // 60 + 1
        for i in range(1,pnumber+1):
            urllist.append("http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E6%B7%B1%E5%9C%B3&kw="+searchname+"&p="+str(i)+"&isadv=0")

    for line in urllist:
        print line
    #driver.close()  # 关闭
    return urllist

def getinformation(url):
    headers = {"User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0);"}
    pagetxt = requests.get(url, headers=headers).content
    time.sleep(5)

    restr = "<div class=\"newlist_list_content\" id=\"newlist_list_content_table\">([\s\S]*?)<p class=\"newlist_list_top clearfix\">"  # 正则表达式，（）只要括号内的数据
    regex = re.compile(restr, re.IGNORECASE)
    mylist = regex.findall(pagetxt)

    restr = "<table([\s\S]*?)</table>"  # 正则表达式，（）只要括号内的数据
    regex = re.compile(restr, re.IGNORECASE)
    mylist = regex.findall(mylist[0])

    for line in mylist:
        # print line
        restr = "<td class=\"zwyx\">([\s\S]*?)</td>"  # 正则表达式，（）只要括号内的数据
        regex = re.compile(restr, re.IGNORECASE)
        getvaluelist = regex.findall(line)  # 价格

        restr = "<td class=\"gzdd\">([\s\S]*?)</td>"  # 正则表达式，（）只要括号内的数据
        regex = re.compile(restr, re.IGNORECASE)
        getaddrlist = regex.findall(line)  # 价格

        restr = " <td class=\"gsmc\">([\s\S]*?)</td>"  # 正则表达式，（）只要括号内的数据
        regex = re.compile(restr, re.IGNORECASE)
        getcomlist = regex.findall(line)  # 价格
        if len(getcomlist) > 0:
            restr = " target=\"_blank\">([\s\S]*?)</a>"  # 正则表达式，（）只要括号内的数据
            regex = re.compile(restr, re.IGNORECASE)
            getlastcomlist = regex.findall(getcomlist[0])  # 价格

        restr = "<td class=\"zwmc\"([\s\S]*?)</td>"  # 正则表达式，（）只要括号内的数据
        regex = re.compile(restr, re.IGNORECASE)
        getnamelist = regex.findall(line)  # 价格
        if len(getnamelist) > 0:
            restr = " target=\"_blank\">([\s\S]*?)</a>"  # 正则表达式，（）只要括号内的数据
            regex = re.compile(restr, re.IGNORECASE)
            getlastnamelist = regex.findall(getnamelist[0])  # 价格

            restr = "href=\"([\s\S]*?)\""  # 正则表达式，（）只要括号内的数据
            regex = re.compile(restr, re.IGNORECASE)
            getlasturllist = regex.findall(getnamelist[0])  # 价格

        if len(getaddrlist) > 0 and len(getvaluelist) > 0 and len(getlastcomlist) > 0 and len(getlastnamelist) > 0:
            print getlastnamelist[0], getlastcomlist[0], getvaluelist[0], getaddrlist[0], getlasturllist[0]
            print "------------------------------------------------------------------"

            lastlist=[]
            lastlist.append(getlastnamelist[0])
            lastlist.append(getlastcomlist[0])
            lastlist.append(getvaluelist[0])
            lastlist.append(getaddrlist[0])
            lastlist.append(getlasturllist[0])
            savefilepath = "workinfo4.txt"
            savefile = open(savefilepath, "ab")
            for line in lastlist:
                savefile.write((line + "\r\n"))
            savefile.close()

    #driver.close()
searchname="Java"
for line in geturllist(searchname):
    getinformation(line)