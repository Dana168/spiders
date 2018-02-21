#coding:utf-8
import multiprocessing
import multiprocessing.managers #分布式进程管理器
import random,time  #随机数，时间
import Queue #队列

task_queue=Queue.Queue() #任务
result_queue=Queue.Queue() #结果
title_queue=Queue.Queue() #结果

def  return_task(): #返回任务队列
    return task_queue
def return_result(): #返回结果队列
    return   result_queue
def return_title(): #返回结果队列
    return   title_queue

class  QueueManger(multiprocessing.managers.BaseManager):#继承，进程管理共享数据
    pass

if __name__=="__main__":
    multiprocessing.freeze_support()#开启分布式支持
    QueueManger.register("get_task",callable=return_task)#注册函数给客户端调用
    QueueManger.register("get_result", callable=return_result)
    QueueManger.register("get_title", callable=return_title)
    manger=QueueManger(address=("10.36.132.204",8848),authkey="123456") #创建一个管理器，设置地址与密码
    manger.start() #开启
    task,result=manger.get_task(),manger.get_result() #任务，结果
    title = manger.get_title()
    urlList = ["https://baike.baidu.com/item/Python/407313",
                'https://baike.baidu.com/item/web/150564',
                'https://baike.baidu.com/item/php/9337'
               ]
    for  url  in urlList:
        task.put(url)
    while True:
        myUrl = result.get()
        mytitle = title.get()
        if myUrl not in urlList:
            print mytitle
            task.put(myUrl)
            urlList.append(myUrl)


    manger.shutdown()#关闭服务器

