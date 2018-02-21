#python3
#分布式爬取51job职位

import multiprocessing
import multiprocessing.managers
import threading

import lxml
import requests
import re
from queue import  Queue
import  lxml.etree
import time

def geturllist(url):
    headers = {"User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0);"}
    response = requests.get(url, headers=headers).content.decode("gbk")
    # print response
    mytree = lxml.etree.HTML(response)
    number = mytree.xpath("//div[@class=\"rt\"]/text()")[0].strip()
    restr = re.compile("(\d+)",re.IGNORECASE)
    num = restr.findall(number)[0]
    num = eval(num)

    urllist=[]
    pages=0
    if num % 50 == 0:
        pages = num // 50
    else:
        pages = num // 50 + 1
    for i in range(1, pages + 1):
        urllist.append("http://search.51job.com/list/040000,000000,0000,00,9,99,python,2,"+str(i)+".html")
    print (urllist)
    return urllist

task_queue=Queue() #任务
result_queue=Queue() #结果

def  return_task(): #返回任务队列
    return task_queue
def return_result(): #返回结果队列
    return   result_queue


class  QueueManger(multiprocessing.managers.BaseManager):#继承，进程管理共享数据
    pass


def  getmsgfromclient(result):
    savefile=open("msg.txt","wb") #保存邮件，
    while True:
        time.sleep(1)
        res = result.get(timeout=100)
        print ("get data", res)
        # print res
        savefile.write((res+"\r\n").encode("utf-8"))
        savefile.flush()
    savefile.close()

if __name__ == '__main__':
    multiprocessing.freeze_support()  # 开启分布式支持
    QueueManger.register("get_task", callable=return_task)  # 注册函数给客户端调用
    QueueManger.register("get_result", callable=return_result)
    manger = QueueManger(address=("127.0.0.1",8888), authkey=b"100000")  # 创建一个管理器，设置地址与密码
    manger.start()  # 开启
    task, result = manger.get_task(), manger.get_result()  # 任务，结果
    url = "http://search.51job.com/list/040000,000000,0000,00,9,99,python,2,3.html"
    urllist = geturllist(url)

    for url in urllist:
        print ("task add data", url)
        task.put(url)
    for i in range(50):
        thd = threading.Thread(target= getmsgfromclient,args=(result,))#开启接收的线程
        thd.start()

    print ("waitting for------")


    time.sleep(10000)
    print ("over")
    manger.shutdown()  # 关闭服务器


    pass