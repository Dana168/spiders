import multiprocessing  #分布式进程
import multiprocessing.managers #分布式进程管理器
import random,time  #随机数，时间
import queue #队列
import threading
task_queue=queue.Queue() #任务
result_queue=queue.Queue() #结果mail
url_queue=queue.Queue()#结果url
import selenium
import selenium.webdriver
mlist=[]
import pymongo
import pyquery

def  return_task(): #返回任务队列
    return task_queue
def return_result(): #返回结果队列
    return   result_queue
def mongdb():#存入数据库
    import pymongo
    conn = pymongo.MongoClient()  # 连接本机数据库
    # conn = pymongo.MongoClient(host="192.168.1.202")


class  QueueManger(multiprocessing.managers.BaseManager):#继承，进程管理共享数据
    pass
def geturl(name):#获取初始链接
    jsl='https://search.jd.com/Search?keyword='+ name+ '&enc=utf-8&'
    return jsl

def productlist(starturl,numb):#爬取函数
    if (numb<2):#当商品数量小于2页时
       url=starturl+"&pag="+str(2)
       driver=selenium.webdriver.PhantomJS()
       driver.get(url)
       text = driver.find_element_by_xpath('//*[@class="filter"]//a[2]')
       text.click()
       html = driver.page_source
       # print(html)
       content = pyquery.PyQuery(html)
       Rmbs = content(".gl-i-wrap")


       for xes in Rmbs.items():
           name = xes("em").eq(1).text()  # 商品名称
           newurl=xes('a').attr('href')
           print(name,newurl)
           mlist.append(newurl)
       return mlist
    else:
        url = starturl + "&pag=" + str(3)
        driver = selenium.webdriver.PhantomJS()
        driver.get(url)
        text = driver.find_element_by_xpath('//*[@class="filter"]//a[2]')
        text.click()
        html = driver.page_source
        # print(html)
        content = pyquery.PyQuery(html)
        Rmbs = content(".gl-i-wrap")
        for xes in Rmbs.items():
            name = xes("em").eq(1).text()  # 商品名称
            newurl = xes('a').attr('href')#输出跳转链接productID
            mlist.append(newurl)
        return mlist#返回新链接列表
if __name__=="__main__":
    multiprocessing.freeze_support()
    QueueManger.register("get_task",callable=return_task)#注册函数给客户端调用
    QueueManger.register("get_result", callable=return_result)

    manger=QueueManger(address=("10.36.132.69",8888),authkey=4444)
    #manger=QueueManger(address=("10.36.132.77",8888)) #创建一个管理器，设置地址与密码
    manger.start() #开启
    time.sleep(10)
    task,result=manger.get_task(),manger.get_result() #任务，结果
    name=input("请输入你要爬取的商品")
    jsl=geturl(name)
    print(jsl)
    jslist=productlist(jsl,2)
    for list in jslist:
        task.put(list)
    time.sleep(30)
    while True:
        try:
           r=result.get()
           print(r)
        except:
            break
    manger.shutdown()  # 关闭服务器

