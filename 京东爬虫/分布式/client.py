import multiprocessing  #分布式进程
import multiprocessing.managers #分布式进程管理器
import random,time  #随机数，时间
import queue #队列
import os

import re
import threading
import gevent
import gevent.monkey
import selenium
import selenium.webdriver
import pyquery
import requests
import json
#gevent.monkey.patch_all()#自动切换
mlist = []
ylist=[]


def download(yson):#爬取商品评论
    html=requests.get(yson).text

    jsondata=html[26:-2]
    #print(jsondata)
    data=json.loads(jsondata)#获取为json 格式
    #print(data)
    for i in data['comments']:
        content = i['content']
        print(content)

        result.put(content)



#yson="http://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv2941&productId=11712592910&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1"


def jsonurl(numb,url):#爬取评价页数

    for i in range(0,numb):
        hturl=url+'&score=0&sortType=5&page='+str(i)+"&pageSize=10&isShadowSku=0&fold=1"

        download(hturl)
        hturl=""


def produID(url):

     rester = "\d+"
     id = re.findall(rester, url)[0]
    #print(id)
     url = "http://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv2941&productId=" + id
     # 返回构建的json 链接
     return url


class QueueManager(multiprocessing.managers.BaseManager):
    pass


if __name__ == '__main__':
    
    QueueManager.register("get_task")  # 注册函数调用服务器
    QueueManager.register("get_result")

    manger = QueueManager(address=("10.36.132.69", 8888),authkey=4444)
    manger.connect()  # 链接服务器
    task = manger.get_task()
    result = manger.get_result()  # 任务，结果
    talist=[]
    print(3)
    time.sleep(20)
    while True:
        if(not  task.empty()):

           starturl=task.get()
           idurl=produID(starturl)
           talist.append(gevent.spawn(jsonurl,10,idurl))
        else:
            break


    gevent.joinall(talist)






