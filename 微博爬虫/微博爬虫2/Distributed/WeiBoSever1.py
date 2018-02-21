#coding:utf-8
import multiprocessing  #分布式进程
import multiprocessing.managers #分布式进程管理器
import random,time  #随机数，时间
import queue #队列
import threading

task_queue=queue.Queue() #任务
result_queue=queue.Queue() #结果mail
url_queue=queue.Queue()#结果url

def  return_task(): #返回任务队列
    return task_queue
def return_result(): #返回结果队列
    return   result_queue
def return_resulturl(): #返回结果队列
    return   url_queue

class  QueueManger(multiprocessing.managers.BaseManager):#继承，进程管理共享数据
    pass

def  getmailfromclient(result):
    savefile=open("email.txt","wb") #保存邮件，
    while True:
        res = result.get(timeout=100)
        print ("get data", res)
        savefile.write((res+"\r\n").encode("utf-8"))
        savefile.flush()
    savefile.close()

if __name__=="__main__":
    multiprocessing.freeze_support()#开启分布式支持
    QueueManger.register("get_task",callable=return_task)#注册函数给客户端调用
    QueueManger.register("get_result", callable=return_result)
    QueueManger.register("get_resultURL", callable=return_resulturl)

    manger=QueueManger(address=("192.168.30.1",8848),authkey=123456) #创建一个管理器，设置地址与密码
    # manger=QueueManger(address=("192.168.30.1",8848),authkey=123456) #创建一个管理器，设置地址与密码
    manger.start() #开启
    task,result=manger.get_task(),manger.get_result() #任务，结果
    result_URL=manger.get_resultURL()#接收url
    visitedlist=["http://bbs.tianya.cn/m/post-140-393974-1.shtml",
                  "http://bbs.tianya.cn/m/post-140-393974-2.shtml",
                  "http://bbs.tianya.cn/m/post-140-393974-3.shtml"]

    for  url  in ["http://bbs.tianya.cn/m/post-140-393974-1.shtml",
                  "http://bbs.tianya.cn/m/post-140-393974-2.shtml",
                  "http://bbs.tianya.cn/m/post-140-393974-3.shtml"]:
        print ("task add data",url)
        task.put(url)
    threading.Thread(target= getmailfromclient,args=(result,)).start()#开启接收的线程

    print ("waitting for------")
    for  i  in range(10000):
        resurl=result_URL.get(timeout=100)
        print ("get data",resurl)
        if  resurl  in  visitedlist:
            pass
        else:
            task.put(resurl )
            visitedlist.append(resurl )

    manger.shutdown()#关闭服务器

