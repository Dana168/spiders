#! C:\Python36\python.exe
# coding:utf-8
import time
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
    btn.submit()
    time.sleep(5)
    text=driver.page_source
    print(text)
    # time.sleep(60)
    driver.close()
    return text

def getUrl(text):
    mtree=lxml.etree.HTML(text)
    mlist=mtree.xpath("//div[@class='TopstoryMain']/div//div[1]/div//div[2]//div[1]//div[2]/h2/a/text()")
    print(mlist[0])



if __name__ == '__main__':
    url="https://www.zhihu.com/#signin" # 知乎登陆页面
    text=getPageText(url)
    getUrl(text)