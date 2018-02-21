import multiprocessing.managers
import multiprocessing
import queue
import threading
import urllib

import selenium
import time
from selenium import webdriver
import lxml
from lxml import etree
from multiprocessing import Queue
import urllib.request
task_queue=queue.Queue() #任务
result_queue=queue.Queue()  #结果mail
resulturl_queue = queue.Queue()
def  return_task(): #返回任务队列
    return task_queue
def return_result(): #返回结果队列
    return   result_queue
def return_resulturl(): #返回结果队列
    return   resulturl_queue
class  QueueManger(multiprocessing.managers.BaseManager):#继承，进程管理共享数据
    pass
y = 0
def download(url):
    global y
    y += 1
    try:
        name = url.split("/")
        urllib.request.urlretrieve(url,r"F:\\picture"+"\\"+str(y)+".jpg")
    except:
        pass
def getdatafromclient(result):
    while True:
        time.sleep(2)
        res = resulturl.get(timeout=50)
        download(res)
        print("get data",res)
def getstrfromclient(result):
    with open("世纪佳缘.txt","wb")as file:
        try:
            while True:
                time.sleep(2)
                mystr = result.get(timeout=50)
                file.write((mystr+'\r\n').encode("utf-8"))
                file.flush()
        except:
            pass

if __name__ == "__main__":
    multiprocessing.freeze_support()  # 开启分布式支持
    QueueManger.register("get_task", callable=return_task)  # 注册函数给客户端调用
    QueueManger.register("get_result", callable=return_result)
    QueueManger.register("get_resulturl", callable=return_resulturl)
    manger = QueueManger(address=("192.168.0.107", 8868), authkey=123456)  # 创建一个管理器，设置地址与密码
    manger.start()  # 开启
    task, result = manger.get_task(), manger.get_result()  # 任务，结果
    resulturl = manger.get_resulturl()#结果url队列
    sem = threading.Semaphore(15)
    print("服务端开启")
    driver = selenium.webdriver.PhantomJS()
    driver.get("http://login.jiayuan.com/?channel=200&position=102")
    username = driver.find_element_by_id("login_email")
    password = driver.find_element_by_id("login_password")
    isenter = driver.find_element_by_id("login_btn")
    username.send_keys("18370808967")
    password.send_keys("123456")
    isenter.click()
    time.sleep(3)
    driver.get("http://search.jiayuan.com/v2/index.php?")
    time.sleep(2)
    data = driver.page_source
    i = 0
    def geturllist(driver,data):
        global i
        i += 1
        mytree = lxml.etree.HTML(data)
        urllist = mytree.xpath("//div[@class = 'user_name']/a/@href")
        for url in urllist[1:]:
            task.put(url)      #往任务队列里添加任务
        js = "getSearchResult('next')"#执行js自动翻页
        driver.execute_script(js)
        time.sleep(3)
        driver.implicitly_wait(10)
        data = driver.page_source
        url = resulturl.get()
        th = threading.Thread(target=getdatafromclient, args=(resulturl,)).start()#开启一条线程来接受数据
        otherth = threading.Thread(target=getstrfromclient,args=(result,)).start()#开启另外一条线程来保存图片
        print(url)
        if data.find("第" + str(i) + "页") != -1:  # 判断是不是最后一页
            geturllist(driver,data)  # 递归翻页
    geturllist(driver,data)
    manger.shutdown()  # 关闭服务器