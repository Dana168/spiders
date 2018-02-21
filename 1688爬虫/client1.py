"""
登陆1688，输入关键字查询,评价数量前100的评论，评论情感分析打分
"""
#coding:utf-8
import multiprocessing
import multiprocessing.managers
import os

import re
import requests
import threading

import time
from aip import AipNlp

class  QueueManger(multiprocessing.managers.BaseManager):
    pass
#一级货品页面的商品名，商品价格信息，offerid，memberid，为了之后拼接评论页面json，因为不是标准json这里用正则提取
pattern1 = "Num\"[\s\S]*?title=\"(.*?)\"[\s\S]*?offer-stat=\"title\"[\s\S]*?title=\"([\s\S]*?)\"[\s\S]*?offerid=\"(\d+)\" memberid=\"(.*?)\""
regex1 = re.compile(pattern1, re.IGNORECASE)
#评论页面json评论内容
pattern2 = "\"remarkContent\":\"([\s\S]*?)\""
regex2 = re.compile(pattern2, re.IGNORECASE)

def getID(url):
    try:
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0"}
        html = requests.get(url,headers = headers,timeout=15).text
        html = html.replace("\\", "")#去掉转义字符
        s = regex1.findall(html)#拿到一级货品页面的商品名，商品价格信息，offerid，member
        return s
    except:
        pass

def getDealNum(url):
    try:
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0"}
        data = requests.get(url,headers = headers,timeout=20).text
        return regex2.findall(data)#拿到评论页面的评论
    except Exception as e:
        print(e)

def threadWork(tup):#线程任务
    u,resultQueue = tup
    commentList = getDealNum(u[0])
    try:
        if len(commentList) > 0:
            resultQueue.put([len(commentList),commentList, u[1]])#评论数量，评论内容，物品信息
            print(u[1])
    except Exception as e:
        print (e)

def processWork(url,resultQueue):#进程任务
    taskList = []
    pageList = getID(url)
    print("处理", url)
    try:
        for i in pageList:
            infor = i[1] + " " + i[0]#物品信息和价格
            #物品二级页面的json网址，通过改变offerid，memberid定位每个物品，通过改变里面的pageSize参数控制单页评论数量，这样可以一页显示所有评论
            u = ["https://rate.1688.com/remark/offerDetail/rates.json?tbpm=3&_input_charset=GBK&offerId=" + i[
                2] + "&page=1&pageSize=20&starLevel=&orderBy=date&semanticId=&showStat=0&content=null&t=1509587863630&memberId=" +
                 i[3] + "&callback=jQuery17207534614175265777_1509587818416", infor]
            th = threading.Thread(target=threadWork, args=((u, resultQueue),))
            th.start()
            taskList.append(th)
        for thr in taskList:
            thr.join()
    except Exception as e:
        print(e)

if __name__ == '__main__':
    sem = threading.Semaphore(10)
    resultQueue = multiprocessing.Manager().Queue()
    QueueManger.register("getTask")
    QueueManger.register("getResult")
    manager = QueueManger(address=("192.168.1.103", 8000), authkey="123456".encode("utf-8"))
    manager.connect()
    task = manager.getTask()
    result = manager.getResult()
    urlList = []
    while not task.empty():
        url = task.get()
        urlList.append(url)
    with sem:
        pool = multiprocessing.Pool(processes=1)#开启进程池
        for u in urlList:
            pool.apply_async(func=processWork, args=(u, resultQueue))#异步处理，不会阻塞后面的任务
    while True:
        if not resultQueue.empty():
            result.put(resultQueue.get())
        else:
            time.sleep(5)#5秒仍为空视为任务结束
            if resultQueue.empty():
                break
    pool.close()
    pool.join()
