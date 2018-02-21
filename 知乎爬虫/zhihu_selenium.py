#! C:\Python36\python.exe
# coding:utf-8

from selenium import webdriver
import time
from bs4 import BeautifulSoup


driver=webdriver.Chrome()                #用chrome浏览器打开
driver.get("http://www.zhihu.com")       #打开知乎我们要登录
time.sleep(2)                            #让操作稍微停一下
driver.find_element_by_link_text('登录').click() #找到‘登录’按钮并点击
time.sleep(2)
#找到输入账号的框，并自动输入账号 这里要替换为你的登录账号
driver.find_element_by_name('account').send_keys('13232929610')
time.sleep(2)
#密码，这里要替换为你的密码
driver.find_element_by_name('password').send_keys('13232929610')
time.sleep(2)
#输入浏览器中显示的验证码，这里如果知乎让你找烦人的倒立汉字，手动登录一下，再停止程序，退出#浏览器，然后重新启动程序，直到让你输入验证码
yanzhengma=input('验证码:')
driver.find_element_by_name('captcha').send_keys(yanzhengma)
#找到登录按钮，并点击
driver.find_element_by_css_selector('div.button-wrapper.command > button').click()

# 获得cookies
cookie=driver.get_cookies()
time.sleep(3)
driver.get('https://www.zhihu.com/topic/19551137/hot')
time.sleep(5)

# 每5秒下移一次，一共下移10次
def execute_times(times):
    for i in range(times + 1):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
execute_times(10)

# 页面解析
html=driver.page_source
soup1=BeautifulSoup(html,'lxml')
authors=soup1.select('a.author-link')
authors_alls=[]
authors_hrefs=[]
for author in authors:
    authors_alls.append(author.get_text())
    authors_hrefs.append('http://www.zhihu.com'+author.get('href'))
authors_intros_urls=soup1.select('span.bio')
authors_intros=[]
for authors_intros_url in authors_intros_urls:
    authors_intros.append(authors_intros_url.get_text())

for authors_all,authors_href,authors_intro in zip(authors_alls,authors_hrefs,authors_intros):
    data={
        'author':authors_all,
        'href':authors_href,
        'intro':authors_intro
    }
    print(data)