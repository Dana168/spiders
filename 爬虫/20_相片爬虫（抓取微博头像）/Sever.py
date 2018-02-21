# coding:utf-8
'''
由于微博系统默认设置，无法查看超过5页的非互相关注人的关注列表
→→→→→→→→本程序用分布式链接，程序启动前请先修改本机地址ip(第45行代码）←←←←←←←
→→→→→→→→请在60行和63行输入微博用户名和密码←←←←←←←
'''
import multiprocessing  # 分布式进程
import multiprocessing.managers  # 分布式进程管理器
import queue  # 队列
import threading
import selenium
import selenium.webdriver
import time
import lxml
import lxml.etree
import requests
import re

task_queue = queue.Queue()  # 任务
result_queue = queue.Queue()  # 结果img
url_queue = queue.Queue()  # 结果url


def return_task():  # 返回任务队列
    return task_queue


def return_result():  # 返回结果队列
    return result_queue


def return_resulturl():  # 返回结果队列
    return url_queue


class QueueManger(multiprocessing.managers.BaseManager):  # 继承，进程管理共享数据
    pass


if __name__ == "__main__":
    multiprocessing.freeze_support()  # 开启分布式支持
    QueueManger.register("get_task", callable=return_task)  # 注册函数给客户端调用
    QueueManger.register("get_result", callable=return_result)
    QueueManger.register("get_resultURL", callable=return_resulturl)

    manger = QueueManger(address=("10.36.132.10", 8848), authkey=123456)  # 创建一个管理器，设置地址与密码
    manger.start()  # 开启
    task, result = manger.get_task(), manger.get_result()  # 任务，结果
    resultURL = manger.get_resultURL()  # 接收url
    visitedlist = ['1699637153', '5562309247', '5750600479', '6327679940', '5346093632',
                   '1878905274', '1829348151', '1732464917', '1225419417', '1391954182']  # 初始id

    driver = selenium.webdriver.Firefox()
    driver.get("https://weibo.com/login")
    print("正在打开微博")
    time.sleep(10)
    # 登录
    print("正在登录")
    username = driver.find_element_by_id("loginname")
    username.send_keys("1733776802@qq.com")  # 请在此输入用户名
    time.sleep(2)
    password = driver.find_element_by_name("password")
    password.send_keys("zhs314159265")  # 请在此输入密码
    time.sleep(5)
    elem = driver.find_element_by_xpath(
        "/html/body/div[1]/div[1]/div/div[2]/div[1]/div[2]/div/div[2]/div[1]/div[2]/div[1]/div/div/div/div[3]/div[6]/a")
    elem.click()
    time.sleep(3)
    print("登录成功")

    # 跳转我的主页
    # driver.get("https://weibo.com/u/3714235945/home")
    print("正在跳转到主页")
    time.sleep(5)
    for myid in visitedlist:
        task.put(myid)
        print("put data :", myid)
    print("初始化完成--------")
    print("请打开客户端下载图片--------")
    print("请打开客户端下载图片--------")
    print("请打开客户端下载图片--------")

    imgnum = 0  # 标记当前已put多少图片
    while True:
        try:
            id = task.get()
            print("get id:",id)

            for i in range(1, 6):
                theurl = "https://weibo.com/p/100505" + id + "/follow?page=" + str(i) + "#Pl_Official_HisRelation__61"
                driver.get(theurl)
                print("正在打开", theurl)
                time.sleep(10)
                data = driver.page_source
                print("抓取网页源码")
                mytree = lxml.etree.HTML(data)
                # //*[@id="Pl_Official_HisRelation__60"]/div/div/div/div[2]/div[1]/ul/li[1]/dl/dt/a/img
                # //*[@id="Pl_Official_HisRelation__60"]/div/div/div/div[2]/div[1]/ul/li[2]/dl/dt/a/img
                imgurl = mytree.xpath("//*[@id=\"Pl_Official_HisRelation__60\"]/div/div/div/div[2]/div[1]/ul/li")  # 主页关注列表
                imgurl = imgurl[0]
                print("获得关注列表")
                usercardlist = imgurl.xpath("//dl/dd[1]/div[1]/a[1]/@usercard")  # 获得id
                imglist = imgurl.xpath("//dl/dt/a/img/@src")  # 图片链接
                rexs = re.compile("id=(\d+)")
                print("获得图片链接")
                for usercard in usercardlist:
                    theid = re.findall(rexs, usercard)
                    myid = theid[0]  # id
                    #去重
                    if myid in visitedlist:
                        pass
                    else:
                        task.put(myid)
                        print("put id:",myid)

                for theimgurl in imglist:
                    theimgurl = theimgurl.replace(".50/",".690/")  # 替换成高清图片的链接
                    result.put(theimgurl)
                    imgnum += 1
                    print("put imgurl:",imgnum,"---",theimgurl)
        except Exception as e:
            print("解析网页出错：",e)