"""
登陆1688，输入关键字查询,评价数量前100的评论，评论情感分析打分
"""
#coding:utf-8
import multiprocessing
import multiprocessing.managers
import queue
import urllib

import lxml
import lxml.etree
import time
import pymongo

from aip import AipNlp
from selenium import webdriver

""" 你的 APPID AK SK """
APP_ID = ''
API_KEY = ''
SECRET_KEY = ''

aipNlp = AipNlp(APP_ID, API_KEY, SECRET_KEY)

taskQueue = queue.Queue()
resultQueue = queue.Queue()

def getPage(keyword):#1688必须登录才能查看，这个函数的目的是拿到关键字的搜索页数返回任务网址
    driver = webdriver.Firefox()
    #1688用的是从淘宝网链接过来的网页登录，直接操作1688的登录界面会找不到元素
    url = "https://login.taobao.com/member/login.jhtml?style=b2b&css_style=b2b&from=b2b&newMini2=true&full_redirect=true&redirect_url=https%3A%2F%2Flogin.1688.com%2Fmember%2Fjump.htm%3Ftarget%3Dhttps%253A%252F%252Flogin.1688.com%252Fmember%252FmarketSigninJump.htm%253FDone%253Dhttp%25253A%25252F%25252Fmember.1688.com%25252Fmember%25252Foperations%25252Fmember_operations_jump_engine.htm%25253Ftracelog%25253Dlogin%252526operSceneId%25253Dafter_pass_from_taobao_new%252526defaultTarget%25253Dhttp%2525253A%2525252F%2525252Fwork.1688.com%2525252F%2525253Ftracelog%2525253Dlogin_target_is_blank_1688&reg=http%3A%2F%2Fmember.1688.com%2Fmember%2Fjoin%2Fenterprise_join.htm%3Flead%3Dhttp%253A%252F%252Fmember.1688.com%252Fmember%252Foperations%252Fmember_operations_jump_engine.htm%253Ftracelog%253Dlogin%2526operSceneId%253Dafter_pass_from_taobao_new%2526defaultTarget%253Dhttp%25253A%25252F%25252Fwork.1688.com%25252F%25253Ftracelog%25253Dlogin_target_is_blank_1688%26leadUrl%3Dhttp%253A%252F%252Fmember.1688.com%252Fmember%252Foperations%252Fmember_operations_jump_engine.htm%253Ftracelog%253Dlogin%2526operSceneId%253Dafter_pass_from_taobao_new%2526defaultTarget%253Dhttp%25253A%25252F%25252Fwork.1688.com%25252F%25253Ftracelog%25253Dlogin_target_is_blank_1688%26tracelog%3Dlogin_s_reg"
    driver.get(url)
    time.sleep(1)
    driver.find_element_by_class_name("login-switch").click()
    username = ""#你的淘宝账号
    password = ""#你的淘宝密码
    time.sleep(1)
    driver.find_element_by_id("TPL_username_1").send_keys(username)
    time.sleep(1)
    driver.find_element_by_id("TPL_password_1").send_keys(password)
    time.sleep(3)
    driver.find_element_by_id("J_SubmitStatic").click()
    time.sleep(5)
    keyword = urllib.parse.quote(keyword.encode("gbk"))#解决浏览器url对中文的转换
    driver.get(
        "https://s.1688.com/selloffer/offer_search.htm?keywords="+keyword+"&n=y&spm=a260k.635.1998096057.d1#beginPage=1&offset=0")
    time.sleep(3)
    driver.execute_script("window.scrollBy(0,30000)")
    time.sleep(2)
    html = driver.page_source
    mytree = lxml.etree.HTML(html)
    return (mytree.xpath("//em[@class=\"fui-paging-num\"]/text()")[0])

def  returnTask():
    return taskQueue

def returnResult():
    return  resultQueue

class  QueueManger(multiprocessing.managers.BaseManager):
    pass

def getPageUrl(keyword):
    pageList = []
    # pages = eval(getPage(keyword))
    keyword = urllib.parse.quote(keyword.encode("gbk"))
    # for i in range(1,pages+1):
    for i in range(3):
        #1688为瀑布流ajax，一次显示20个，除了selenium可以拿到json修改参数让60个信息全部显示
        page = "https://s.1688.com/selloffer/rpc_async_render.jsonp?keywords="+keyword+"&qrwRedirectEnabled=false&n=y&uniqfield=pic_tag_id&beginPage="+str(i)+"&_=1509585224574&templateConfigName=marketOfferresult&offset=0&pageSize=60&asyncCount=60&startIndex=0&async=true&enableAsync=true&rpcflag=new&_pageName_=market&callback=jQuery18306540157986921664_150"
        pageList.append(page)
    return pageList

if __name__ == '__main__':
    keyword = input("请输入查询关键字:")
    urlList = getPageUrl(keyword)
    multiprocessing.freeze_support()
    QueueManger.register("getTask", callable=returnTask)
    QueueManger.register("getResult", callable=returnResult)
    manager = QueueManger(address=("192.168.1.103", 8000), authkey="123456".encode("utf-8"))
    manager.start()
    task, result = manager.getTask(), manager.getResult()
    for u in urlList:
        task.put(u)#jsonw网址传入队列
        print(u)
    print("压入完毕")
    allList = []
    time.sleep(10)
    while True:
        if not result.empty():
            text = result.get()
            print(text[2])
            allList.append(text)
        else:
            time.sleep(15)#超过15秒为空表示结束
            if result.empty():
                break
    allList.sort()
    allList.reverse()
    rankList = allList[:10]#对评论数量进行排名，取前100名,测试前10名
    print("开始评分")#百度AI不支持并发，所以只能取完数据再分析
    for infor in rankList:
        result = 0
        if infor[0] > 0:
            try:
                for comment in infor[1]:
                    score = aipNlp.sentimentClassify(comment)
                    print(score)
                    result += score["items"][0]['positive_prob']#积极向的分数
                infor.append(result / infor[0])
                infor.reverse()
            except Exception as e:
                print(e)
    print("开始写入")
    client = pymongo.MongoClient(host="127.0.0.1", port=27017)
    db=client["1668"]
    mydb = db["1668"]
    try:
        for text in allList:
            mydb.insert({"物品信息":text[1],"评价数量":round(text[3]*5,1),"评价情感分析":text[0],"评价详情":text[2]})
    except:
        pass
    manager.shutdown()
