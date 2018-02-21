#python3
#分布式爬取 赶集租房信息

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
    response = requests.get(url, headers=headers).content.decode("utf-8")
    # print response
    mytree = lxml.etree.HTML(response)
    restr = re.compile("<span class=\"num\">(\d+)套</span>",re.IGNORECASE)
    num = restr.findall(response)[0]
    num = eval(num)

    # print(num)

    urllist=[]
    pages=0
    if num % 70 == 0:
        pages = num // 70
    else:
        pages = num // 70 + 1
    for i in range(1, pages + 1):
        if i >150:
            break
        urllist.append("http://sz.ganji.com/fang1/o"+str(i)+"p1/")
    # print (urllist)
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
    savefile=open("ganjimsg00.txt","ab+") #保存邮件，
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
    #authkey = b"123"
    manger = QueueManger(address=("127.0.0.1",8848), authkey=b"111111")  # 创建一个管理器，设置地址与密码
    manger.start()  # 开启
    task, result = manger.get_task(), manger.get_result()  # 任务，结果
    url = "http://sz.ganji.com/fang1/o1p1/"
    urllist = geturllist(url)

    for url in urllist:
        print ("task add data", url)
        task.put(url)

    #开启100条线程
    for i in range(40):
        thd = threading.Thread(target= getmsgfromclient,args=(result,))#开启接收的线程
        thd.start()

    print ("waitting for------")



    time.sleep(10000)
    print("over")
    manger.shutdown()  # 关闭服务器


    pass