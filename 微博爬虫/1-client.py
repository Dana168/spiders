#! C:\Python36\python.exe
# coding=utf-8
'''
about what
'''
from multiprocessing.managers import BaseManager

import time


import json
import os
import time
import requests
from selenium import webdriver
import urllib.request

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

    data = data["cards"][0]
    datadict = data['card_group']
    i=0
    for mydata in datadict:
        i+=1
        id = mydata["user"]['id']
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
        mystr += "简介：" + str(intro) + "\r\n"
        mystr += "主页链接：" + str(indexurl) + "\n\n"
        print(mystr)
        #增加任务列表
        jsurl = "https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_"+ str(id)
        resultlist = []
        resultlist.append(mystr)
        resultlist.append(jsurl)
        result.put(resultlist)


# 输入api链接得到粉丝信息【昵称，id】
def weiboGetdata(usename, password,starturl):
    session = login(usename, password)
    i = 0
    #翻页
    while True:
        try:
            i += 1
            url=starturl+"&since_id="+str(i)
            time.sleep(5)
            html = session.get(url).text
            data = json.loads(html)
            getinfo(data)
        # 结束翻页
        except KeyError:
            print("此人粉丝爬完===========================================================================")
            break


if __name__ == '__main__':
    BaseManager.register("get_task")
    BaseManager.register("get_result")
    manger = BaseManager(address=("127.0.0.1", 8888), authkey="123456".encode())
    manger.connect()
    task, result = manger.get_task(), manger.get_result()

    while not task.empty():
        time.sleep(5)
        try:
            taskapi=task.get()
            print("客户机得到任务链接：",taskapi)
            weiboGetdata("18879091455", "asdw09065991", taskapi)
        except:
            pass