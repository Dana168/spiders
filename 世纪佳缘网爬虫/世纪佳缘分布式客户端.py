#! C:\Python36\python.exe
import multiprocessing
import multiprocessing.managers
import queue
import gevent
import requests
import  urllib.request
import selenium
from selenium import webdriver
import time
import gevent.monkey
import lxml
from lxml import etree
import urllib
def getdata(driver,url,result):
    print("开始抓取")
    driver.get(url)
    datas = driver.page_source
    yourtree = lxml.etree.HTML(datas)
    linelist = yourtree.xpath("//div[@class = 'member_info_r yh']")
    for line in linelist:
        name = line.xpath("./h4/text()")
        if len(name)!=0:
            name = line.xpath("./h4/text()")[0]
            result.put(name)
        else:
            name = ""
        print(name)

        userid = line.xpath("./h4/span/text()")
        if len(userid)!=0:
            userid = line.xpath("./h4/span/text()")[0]
            result.put(userid)
        else:
            userid = ""
        print(userid)

        huiyuan = line.xpath(".//p[@class = 'member_ico_box']/span/text()")
        if len(huiyuan)!=0:
             huiyuan = line.xpath(".//p[@class = 'member_ico_box']/span/text()")[0]
             result.put(huiyuan)
        else:
            huiyuan = ""

        info = line.xpath(".//h6[@class = 'member_name']/text()")
        if len(info)!=0:
            info = line.xpath(".//h6[@class = 'member_name']/text()")[0]
            result.put(info)
        else:
            info = ""
        print(info)

        infofirst = line.xpath(".//h6[@class = 'member_name']//a[1]/text()")
        if len(infofirst)!=0:
            infofirst = line.xpath(".//h6[@class = 'member_name']//a[1]/text()")[0]
            result.put(infofirst)
        else:
            infofirst = ""
        print(infofirst)

        infosecond = line.xpath(".//h6[@class = 'member_name']//a[2]/text()")
        if len(infosecond)!=0:
            infosecond = line.xpath(".//h6[@class = 'member_name']//a[2]/text()")[0]
            result.put(infosecond)
        else:
            infosecond = ""
        print(infosecond)
        otherlist = line.xpath("./ul[@class = 'member_info_list fn-clear']//li")
        try:
            for other in otherlist:
                others = other.xpath(".//div[2]/em/text()")
                result.put(others[0])
        except:
            pass
    comment = yourtree.xpath("//div[@class = 'js_text']/text()")
    if len(comment)!=0:
        comment = yourtree.xpath("//div[@class = 'js_text']/text()")[0]
        result.put(comment.strip())
    else:
        comment = "暂无自我介绍"

    imagesrc = yourtree.xpath("//div[@id = 'bigImg']//li[2]/table/tbody/tr/td/a/img/@src")
    if len(imagesrc)!=0:
        imagesrc = yourtree.xpath("//div[@id = 'bigImg']//li[2]/table/tbody/tr/td/a/img/@src")[0]
        resulturl.put(imagesrc)
    else:
        pass
    print(imagesrc)

class  QueueManger(multiprocessing.managers.BaseManager):#继承，进程管理共享数据
    pass


if __name__ == "__main__":
    QueueManger.register("get_task")  # 注册函数调用服务器
    QueueManger.register("get_result")
    QueueManger.register("get_resulturl")
    manger = QueueManger(address=("192.168.0.107", 8868), authkey=123456)
    manger.connect()  # 链接服务器
    task = manger.get_task()
    result = manger.get_result()  # 任务，结果
    resulturl = manger.get_resulturl()
    driver = selenium.webdriver.PhantomJS()
    for i in range(1000):
        time.sleep(1)
        geturllist = []  # url列表
        tasklist = []  # 协程任务列表
        for i in range(100):
            try:
                url = task.get(timeout=1000)  # 服务器抓取一个url
                geturllist.append(url)
            except:
                pass
        for url in geturllist:  # 根据urllist,新建一个协程组，自动切换
            tasklist.append(gevent.spawn(getdata,driver, url,result))
        gevent.joinall(tasklist)