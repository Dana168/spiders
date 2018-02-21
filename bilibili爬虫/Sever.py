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

task_queue = Queue() #任务
result_queue = Queue() #结果

def  return_task(): #返回任务队列
    return task_queue
def return_result(): #返回结果队列
    return   result_queue

class  QueueManger(multiprocessing.managers.BaseManager):#继承，进程管理共享数据
    pass
def geturlnumbers(url):
    content = requests.get(url).text
    mytree = lxml.etree.HTML(content)
    linelist1 = mytree.xpath("//div[@id='primary_menu']")
    urllist1 = []
    urllist4 = []
    urllist5 = []
    for line in linelist1:
        urllist2 = line.xpath("./ul//li[@class='nav-item']/a/@href")
        for url2 in urllist2:
            url = "https:" + url2
            urllist1.append(url)

    for url in urllist1:
        content = requests.get(url).text
        mytree = lxml.etree.HTML(content)
        linelist = mytree.xpath("//div[@class='sub-nav-m']")

        for line in linelist:
            urllist3 = line.xpath("./ul/li/a/@href")

            for url3 in urllist3[1:]:
                url = "https:" + url3
                urllist4.append(url)
    for url in urllist4:

        # driver = selenium.webdriver.PhantomJS(r"D:\爬虫项目\phantomjs-2.1.1-windows\bin\phantomjs.exe")
        # # driver=selenium.webdriver.Chrome()
        # driver.get(url)
        # pagedata = driver.page_source  # 抓取渲染的网页源码代码
        # driver.close()
        # mytree = lxml.etree.HTML(pagedata)  # 解析代码
        # page = mytree.xpath("//a[@class='p endPage']/text()")[0]
        # page = eval(page)
        for i in range(1, 30):
            url = url + "#!page=" + str(i)
            urllist5.append(url)
    return urllist5





if __name__=="__main__":
    urllist = geturlnumbers("https://www.bilibili.com/")

    multiprocessing.freeze_support()#开启分布式支持
    QueueManger.register("get_task", callable=return_task)#注册函数给客户端调用
    QueueManger.register("get_result", callable=return_result)
    manger=QueueManger(address=("127.0.0.1",8848),authkey=123456) #创建一个管理器，设置地址与密码
    manger.start() #开启
    task, result = manger.get_task(), manger.get_result() #任务，结果
    for  url  in  urllist:
        print ("task add data",url)
        # 传入url到客户端
        task.put(url)
    print ("waitting for------")
    savefile = open("bilibili.txt","wb")
    while True:
        # 从客户端得到结果
        res=result.get(timeout=1000)
        print ("get data",res)
        savefile.write(res.encode("utf-8","ignore"))
        savefile.flush()

    savefile.close()
    manger.shutdown()#关闭服务器

