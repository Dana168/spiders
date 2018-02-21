# coding:utf-8
'''
由于微博系统默认设置，无法查看超过5页的非互相关注人的关注列表
→→→→→→→→本程序用分布式链接，程序启动前请先修改本机地址ip(第23行代码）←←←←←←←
'''
import multiprocessing  # 分布式进程
import multiprocessing.managers  # 分布式进程管理器
import queue  # 队列
import requests
import gevent
import gevent.monkey
import threading


class QueueManger(multiprocessing.managers.BaseManager):  # 继承，进程管理共享数据
    pass


if __name__ == "__main__":
    QueueManger.register("get_task")  # 注册函数调用服务器
    QueueManger.register("get_result")
    QueueManger.register("get_resultURL")
    manger = QueueManger(address=("10.36.132.10", 8848), authkey=123456)
    manger.connect()  # 链接服务器
    task = manger.get_task()
    result = manger.get_result()  # 任务，结果
    resultURL = manger.get_resultURL()  # 抓取url
    imgnum = 0
    visitlist = []


    def loadimg():
        global imgnum
        while True:
            try:
                imgurl = result.get()
                if imgurl in visitlist:
                    print("图片已存在")
                else:
                    imgnum += 1
                    visitlist.append(imgurl)
                    imgurl = "http:" + imgurl
                    print("下载图片：", imgnum, "----", imgurl)
                    req = requests.get(imgurl).content
                    with open("爬虫下载图片/%s.png" % imgnum, "wb") as file:
                        file.write(req)
            except Exception as e:
                print("图片%d下载失败："%imgnum,e)

    # 开三条线程持续接收链接下载图片
    threadlist = []
    for i in range(5):
        mythd = threading.Thread(target=loadimg)
        mythd.start()
        threadlist.append(mythd)
    print("线程开启完毕，等待url...")

    # 永不关闭
    while True:
        pass
