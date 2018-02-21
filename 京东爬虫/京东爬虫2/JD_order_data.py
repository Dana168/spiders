# -*- coding: utf-8 -*-
# @Author:
# @Date:
# @Last Modified by:
# @Last Modified time:

'''
京东数据爬取
'''
import codecs
# import urllib


# import gevent
# import requests
import re

import selenium
import selenium.webdriver
import time

from bs4 import BeautifulSoup


def login(url,user_name,password):
    # 登录
    # selenium驱动打开浏览器，并获取URL下的内容
    # driver=selenium.webdriver.Chrome()
    driver=selenium.webdriver.PhantomJS(r"C:\Users\l910726\Desktop\杂物\phantomjs-2.1.1-windows\bin\phantomjs.exe")
    driver.get(url)
    time.sleep(2)
    #selenium控制自动化，选定登录方式
    elem=driver.find_element_by_class_name("login-tab-r")
    elem.click()

    # 自动化输入账号密码并登录
    user=driver.find_element_by_id("loginname")
    psw=driver.find_element_by_id("nloginpwd")
    user.send_keys(user_name)
    psw.send_keys(password)
    time.sleep(3)
    loginbtn=driver.find_element_by_id("loginsubmit")
    loginbtn.click()
    time.sleep(5)

    childurllist = ["1", "2", "2016", "2015", "2014", "3"]
    childurllistall=[]
    for i in childurllist:
        url01 = "https://order.jd.com/center/list.action?search=0&d=" + i + "&s=4096"
        # print url
        driver.get(url01)
        time.sleep(3)
        data = driver.page_source
        soup = BeautifulSoup(data, "lxml")
        page1ist = soup.find_all("div", class_="pagin")[0].find_all("a")
        # print page1ist
        if len(page1ist) == 1:
            page = 1
            childurl = url01 + "&page=" + str(page)
            childurllistall.append(childurl)
        else:
            page = len(page1ist)
            for i in range(1, page):
                childurl = url01 + "&page=" + str(i)
                childurllistall.append(childurl)

    print(childurllistall)

    file=codecs.open("JDdata.txt","wb","utf-8")
    getorderdata(childurllistall, driver, file)

    driver.close()


def getorderdata(childurllistall, driver, file):
    sum=0.00
    for url in childurllistall:
        sum+=getchildurlorderlist(driver, file, url)
    print("您的订单总价格是：",sum)
def getchildurlorderlist(driver, file, url):

    driver.get(url)
    time.sleep(5)
    data=driver.page_source
    print(url,'订单页面加载完成')
    soup = BeautifulSoup(data, "lxml")
    # print type(soup)
    orderlist = soup.find_all(class_="order-tb")[0].find_all("tbody")
    sum=0.00
    for i in orderlist:
        if len(i.find_all(class_="p-name")) != 0:
            dealtime = i.find_all(class_="dealtime")[0].text.strip()
            orderNum = i.find_all(class_="number")[0].find_all("a")[0].text.strip()
            goodName = i.find_all(class_="p-name")[0].find_all("a")[0].text.strip()
            goodsNumber = i.find_all(class_="goods-number")[0].text.strip()
            amount = i.find_all(class_="amount")[0].find_all("span")[0].text.strip()
            file.write(goodName + " & " + goodsNumber + " & " + orderNum + " & " + amount + " & " + dealtime + "\n")
            print(goodName + " & ", goodsNumber + " & ", orderNum + " & ", amount + " & ", dealtime)
            price=re.findall("(\d+.\d+)", amount, flags=re.I)[0]
            price=eval(str(price))
            sum+=price
    return sum

if __name__ == '__main__':

    user_name=input("请输入您的京东账号：")
    password=input("请输入您的京东密码")
    # 登录页面
    url = "https://passport.jd.com/new/login.aspx"
    login(url,user_name,password)

    print("mian over")