#coding:utf-8
import multiprocessing  #分布式进程
import multiprocessing.managers #分布式进程管理器
import random,time  #随机数，时间
import queue #队列
import os
import urllib
import re
import threading
import  queue

import requests
from requests import request


def  geteveryurl(data):
    alllist=[]
    mylist1=[]
    mylist2=[]

    mylist1=getallhttp(data)
    if len(mylist1) >0:
        mylist2=getabsurl(  mylist1[0],data)

    alllist.extend(mylist1)
    alllist.extend(mylist2)
    return  alllist


#<a class="u-btn pre-btn" href="/m/post-140-393974-4.shtml"></a>
def  getabsurl(url,data):
    try:
        regex=re.compile("href=\"(.*?)\"",re.IGNORECASE)
        httplist=regex.findall(data)
        newhttplist=httplist.copy()#深拷贝
        for data  in  newhttplist:
            if  data.find("http://")!=-1:
                httplist.remove(data)
            if  data.find("javascript")!=-1:
                httplist.remove(data)
        hostname=gethostname(url)
        if hostname!=None:
            for  i  in range(len(httplist)):
                httplist[i]=hostname+httplist[i]

        return httplist
    except:
        return []


#http://bbs.tianya.cn/post-140-393974-1.shtml'
#http://bbs.tianya.cn
def  gethostname(httpstr):
    try:
        mailregex = re.compile(r"(http://\S*?)/", re.IGNORECASE)
        mylist = mailregex.findall(httpstr)
        if  len(mylist)==0:
            return None
        else:
            return mylist[0]
    except:
        return None


def  getallhttp(data):
    try:
        mailregex = re.compile(r"(http://\S*?)[\"|>|)]", re.IGNORECASE)
        mylist = mailregex.findall(data)
        return mylist
    except:
        return []


def  getallemail(data):
    try:
        mailregex = re.compile(r"([A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4})", re.IGNORECASE)
        mylist = mailregex.findall(data)
        return mylist
    except:
        return []

def  getdata(url):
    try:
        # data=requests(url).read().decode("utf-8"
        data=requests.get(url).text
        return data  #没有异常返回字符串
    except:
        return "" #发生异常返回空

class  QueueManger(multiprocessing.managers.BaseManager):#继承，进程管理共享数据
    pass

if __name__=="__main__":
    QueueManger.register("get_task")  # 注册函数调用服务器
    QueueManger.register("get_result")
    QueueManger.register("get_resultURL")
    manger=QueueManger(address=("192.168.30.1",8848),authkey=123456)
    manger.connect()  #链接服务器
    task= manger.get_task()
    result =manger.get_result()  # 任务，结果
    resultURL=manger.get_resultURL()#抓取url
    for i  in range(1000):
        time.sleep(1)
        try:
            url=task.get() #服务器抓取一个url

            print ("抓取", url)
            pagedata = getdata(url)  # 抓取页面数据
            print(pagedata)
            emailist = getallemail(pagedata)  # 抓取页面的邮箱
            if len(emailist) != 0:
                for email in emailist:
                    print (email)
                    result.put(email)#返回结果到服务器的邮件结果队列

            urlist = geteveryurl(pagedata)  # 提取页面的链接，压入队列
            if len(urlist) != 0:
                for myurl in urlist:
                    resultURL.put(myurl)



        except:
            pass

