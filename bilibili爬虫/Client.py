#coding:utf-8
import multiprocessing  #分布式进程
import multiprocessing.managers #分布式进程管理器
import random,time  #随机数，时间
from queue import Queue
import requests
import lxml
import re
import lxml.etree
import os
import selenium
import selenium.webdriver

class  QueueManger(multiprocessing.managers.BaseManager):#继承，进程管理共享数据
    pass


#  输入url,返回一个数据集合list
def  download(url):
    datalist = []
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0"}
    driver = selenium.webdriver.PhantomJS(r"D:\爬虫项目\phantomjs-2.1.1-windows\bin\phantomjs.exe")
    # driver=selenium.webdriver.Chrome()
    driver.get(url)
    pagedata = driver.page_source  # 抓取渲染的网页源码代码
    driver.close()
    mytree = lxml.etree.HTML(pagedata)  # 解析代码

    linelist = mytree.xpath("//div[@class='l-item']")
    url = "https://www.bilibili.com"
    for line in linelist:
        mystr = ""
        mystr += url + line.xpath("./div/a[2]/@href")[0] + " # " + "\r\n"
        mystr += line.xpath("./div/a[2]/text()")[0] + " # " + "\r\n"
        mystr += line.xpath("./div/div[@class='v-desc']/text()")[0] + " # " + "\r\n"
        mystr += line.xpath("./div/div[@class='up-info']/a/text()")[0] + " # " + "\r\n"
        mystr += line.xpath("./div/div[@class='up-info']/span/text()")[0] + " # " + "\r\n"
        mystr += line.xpath("./div/div[@class='v-info']/span[1]/span/text()")[0] + " # " + "\r\n"
        mystr += line.xpath("./div/div[@class='v-info']/span[2]/span/text()")[0] + " # " + "\r\n"
        mystr += line.xpath("./div/div[@class='v-info']/span[3]/span/text()")[0] + " # " + "\r\n"
        datalist.append(mystr)
    return  datalist


if __name__=="__main__":
    QueueManger.register("get_task")  # 注册函数调用服务器
    QueueManger.register("get_result")
    manger = QueueManger(address=("127.0.0.1",8848),authkey=123456)

    manger.connect()  #链接服务器
    task= manger.get_task()
    result =manger.get_result()  # 任务，结果

    for i  in range(1000):

        try:
            # 从服务端得到url
            url=task.get()
            print ("client get",url)
            datalist= download(url)
            for  line  in  datalist: #结果队列
                # 传入结果到服务端
                result.put(line)
        except:
            pass

