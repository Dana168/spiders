#! C:\Python36\python.exe
# coding=utf-8
'''
about what
'''
import multiprocessing
from queue import Queue
# 得到记录数量,,,进程管理共享数据
from multiprocessing.managers import BaseManager
import urllib.request
import json
import os
import time
import requests
from selenium import webdriver

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive'}
# 实现登陆获取cookies
def getcookies(username, password):
    driver = webdriver.Chrome()
    driver.get(
        "https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=http%3A%2F%2Fm.weibo.cn%2F%3F%26jumpfrom%3Dweibocom")
    driver.set_page_load_timeout(10)  # 设置超时
    time.sleep(5)
    driver.find_element_by_id("loginName").send_keys(username)
    driver.find_element_by_id("loginPassword").send_keys(password)
    driver.find_element_by_id("loginAction").click()
    time.sleep(10)
    cookies = driver.get_cookies()
    cookieResult = {}
    for item in cookies:
        try:
            cookieResult[item['name']] = item['value']
        except:
            continue
    file = open('cookies', 'w')
    file.write(str(cookieResult))
    file.close()
    return cookieResult

def login(usename, password):
    if os.path.isfile('cookies'):
        cookies = eval(open("cookies", "r").read())
        # print("cookie存在")
    else:
        cookies = getcookies(usename, password)
    session = requests.session()
    session.cookies = requests.utils.cookiejar_from_dict(cookies)
    return session

def getinfo(data):
    # 我的js
    # if str(data).find("card_group")==-1:
    #     datadict = data["cards"]
    # #别人的js
    # else:
    #     data = data["cards"][0]
    #     datadict = data['card_group']
    datadict = data["cards"]
    i=0
    idlist=[]
    for mydata in datadict:
        i+=1
        #我的js有verified_reason，别人的没有
        try:
            id = mydata["user"]['id']
            idlist.append(id)
            name = mydata["user"]["screen_name"]
            image = mydata['user']['profile_image_url']
            intro = mydata["user"]["description"]
            indexurl = mydata["user"]["profile_url"]

            # 下载图片
            imagehref = str(image)
            path = "../image/" + name + ".jpg"
            urllib.request.urlretrieve(imagehref, path)  # 保存图片
            mystr = ""
            mystr += "id：" + str(id) + "\r\n"
            mystr += "昵称：" + str(name) + "\r\n"
            mystr += "头像：" + str(image) + "\r\n"
            mystr += "简介：" + str(intro) + "\n\n"
            mystr += "主页链接：" + str(indexurl) + "\n\n"
            print(mystr)

            file.write(mystr.encode("utf-8", "ignore"))
            file.flush()

            taskapi = "https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_" + str(id)
            task.put(taskapi)
            print("==============================================")
            print("增加任务", taskapi)
            print("==============================================\n")
        except:
            continue
    return idlist

def gettaskapi(usename, password,url):
    session=login(usename,password)
    i = 0
    # 翻页
    while True:
        try:
            i += 1
            html = session.get(url+"&page=" + str(i)).text
            data = json.loads(html)
            getinfo(data)
         # 结束翻页
        except KeyError:
            print("此人粉丝爬完============================")
            break


task_queue=Queue() #任务
result_queue=Queue() #结果

def  return_task(): #返回任务队列
    return task_queue
def return_result(): #返回结果队列
    return   result_queue


if __name__ == '__main__':
    multiprocessing.freeze_support()
    BaseManager.register("get_task", callable=return_task)
    BaseManager.register("get_result", callable=return_result)
    manger = BaseManager(address=("127.0.0.1", 8888), authkey="123456".encode())
    manger.start()
    task, result = manger.get_task(), manger.get_result()

    file = open("info.txt", "wb")

    url = "https://m.weibo.cn/api/container/getSecond?containerid=1005055303733126_-_FANS"
    gettaskapi("18879091455", "asdw09065991", url)

    print("等待数据处理：----------------------")

    while True:
        try:
            reslist = result.get(timeout=50)
            print("得到数据：",reslist[0])
            task.put(reslist[1])
            print("==============================================")
            print("增加任务", reslist[1])
            print("==============================================\n")
            file.write(reslist[0].encode("utf-8", "ignore"))
            file.write("\n".encode("utf-8", "ignore"))
            file.flush()
        except Exception as e:
            print(e)
            break

    file.close()
    manger.shutdown()  # 关闭服务器