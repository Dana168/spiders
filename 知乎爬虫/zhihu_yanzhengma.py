#! C:\Python36\python.exe
# coding:utf-8
import time

import requests
from selenium import webdriver
import lxml
import lxml.etree


def getPageText(url):
    driver=webdriver.Chrome()
    driver.get(url)
    time.sleep(2)
    elem=driver.find_element_by_class_name("signin-switch-password")
    elem.click()
    time.sleep(2)
    user=driver.find_element_by_name("account")
    pwd=driver.find_element_by_name("password")
    btn=driver.find_element_by_xpath("//div[@class='button-wrapper command']/button")
    user.clear()
    pwd.clear()
    user.send_keys("13232929610")
    pwd.send_keys("13232929610")
    time.sleep(10)
    text=driver.page_source
    mtree=lxml.etree.HTML(text)
    mstr=mtree.xpath("//img[@class='Captcha-image']/@src")[0]
    print(type(mstr),mstr)
    purl="https://www.zhihu.com"+str(mstr)
    # btn.submit()
    # time.sleep(15)
    # text=driver.page_source
    # print(text)
    # # time.sleep(60)
    cookies=driver.get_cookies()
    print(cookies)
    driver.close()
    # return text
    return cookies,purl

def getUrl(text):
    mtree=lxml.etree.HTML(text)
    mlist=mtree.xpath("//div[@class='TopstoryMain']/div//div[1]/div//div[2]//div[1]//div[2]/h2/a/text()")
    print(mlist[0])

def download(url,cookies):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/51.0.2704.63 Safari/537.36'}
    req = requests.session()
    for cookie in cookies:
        req.cookies.set(cookie['name'], cookie["value"])
    req.headers.clear()  # 清空头
    newpage = req.get(url,headers=headers,verify=False)
    # content=requests.get(url,cookies=cookies).content
    file=open("1.jpg","wb")
    pic=file.write(newpage.content)
    print("下载完成")


if __name__ == '__main__':
    url="https://www.zhihu.com/#signin" # 知乎登陆页面
    # yzmUrl="https://www.zhihu.com/captcha.gif?r=1509961862004&type=login&lang=cn"
    cookies,yzmUrl=getPageText(url)
    download(yzmUrl,cookies)