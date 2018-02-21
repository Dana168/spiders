import time

import re
import lxml.etree
import bs4
import lxml
import requests
import selenium
import selenium.webdriver

#使用模拟浏览器
# driver=selenium.webdriver.Firefox()
driver=selenium.webdriver.Chrome()
# driver=selenium.webdriver.PhantomJS(r"E:\software\21_python2.7\phantomjs-2.1.1-windows\bin\phantomjs.exe")
#获取微博的登录页面
driver.get("https://weibo.com/")
#延时加载页面
time.sleep(10)
#查找账号
loginname=driver.find_element_by_id("loginname")
#出入账号
loginname.send_keys("1120567103@qq.com")
#查找密码
password=driver.find_element_by_name("password")
#输入密码
password.send_keys("*")

#当页面不含登录，即已经登录时，才跳出循环
#需要输入验证码时
while True:
    #页面不含登录时
    if driver.page_source.find("登录")==-1:
        break
# driver.get("https://weibo.com/"+str(idnumber)+"/profile?rightmod=1&wvr=6&mod=personinfo&is_all=1")
time.sleep(5)



#点击登录
# sub=driver.find_element_by_xpath("//*[@id=\"pl_login_form\"]/div/div[3]/div[6]/a")
# sub.click()


#个人的微博id
idnumber=re.findall("https:\/\/weibo.com\/u\/(\d+)\/home",driver.current_url,re.IGNORECASE)[0]
time.sleep(10)

file=open("1.txt","wb")

#获取所有的朋友的名字和链接
def getAllFriends(allnumber):

    #使用微博id跳转
    driver.get("https://weibo.com/p/100505"+str(idnumber)+"/myfollow?is_friends=1&cfs=&Pl_Official_RelationMyfollow__94_page="+str(allnumber)+"#Pl_Official_RelationMyfollow__94")
    time.sleep(10)
    data1=driver.page_source
    soup=lxml.etree.HTML(data1)
    #抓取链接
    content1=soup.xpath("//*[@class='title W_fb W_autocut ']/a[1]/@href")
    #抓取好友名字
    content2=soup.xpath("//*[@class='title W_fb W_autocut ']/a[1]/text()")

    for a in range(len(content1)):
            #微博信息
            #好友微博名字
            print (content2[a])
            file.write(content2[a].encode("gbk","ignore"))

            file.flush()
            #匹配微博id
            numnerId=re.findall(".*/(.*?)\?",content1[a])[0]
            #打印内容
            getContent(numnerId)

#https://weibo.com/p/1005052056350722/myfollow?is_friends=1&cfs=&Pl_Official_RelationMyfollow__94_page=2#Pl_Official_RelationMyfollow__94
#https://weibo.com/iampaulwong?from=myfollow_friends&is_all=1
#https://weibo.com/u/iampaulwong?from=myfollow_friends&is_all=1
#获取个人的简单基本信息介绍,微博信息
def getContent(number):
    if number.isdigit():
        url="https://weibo.com/u/" + str(number) + "?from=myfollow_friends&is_all=1"
    else:
        url = "https://weibo.com/" + str(number) + "?from=myfollow_friends&is_all=1"
    driver.get(url)
    print(url)

    time.sleep(5)
    # 获取个人的简单基本信息介绍
    ul_detail = driver.find_element_by_class_name("ul_detail")
    # 打印信息
    print(ul_detail.text.strip().replace("\t", "").replace("\n", "").replace(" ", ""))
    file.write("\n".encode("gbk", "ignore"))
    file.write(ul_detail.text.strip().replace("\t", "").replace("\n", "").replace(" ", "").encode("gbk", "ignore"))
    file.write("\n".encode("gbk", "ignore"))
    file.write("--------------------------------------------------------------------------------\n".encode("gbk", "ignore"))
    file.flush()
    count=0
    print("--" * 100)
    while True:

        js = "window.scrollTo(200,55000);"  # 调用js
        driver.execute_script(js)
        time.sleep(5)
        js = "window.scrollTo(200,55000);"  # 调用js
        driver.execute_script(js)
        time.sleep(5)
        js = "window.scrollTo(200,55000);"  # 调用js
        driver.execute_script(js)
        time.sleep(10)
        #获取当前的源码
        data=driver.page_source
        soup=bs4.BeautifulSoup(data,"lxml")
        content=soup.find_all("div",class_="WB_detail")
        for a in content:
            #微博信息
            count+=1
            print (a.get_text().strip().replace("\t","").replace("\n","").replace(" ",""))
            file.write((str(count)+"  "+a.get_text().strip().replace("\t","").replace("\n","").replace(" ","")).encode("gbk", "ignore"))
            file.write("\n".encode("gbk", "ignore"))
            file.flush()

        if driver.page_source.find("page next S_txt1 S_line1")!=-1:
            getNext=driver.find_element_by_xpath("//*[@class='page next S_txt1 S_line1']")
            getNext.click()
        else:
            break
    file.write(("共%d条微博"%(count)).encode("gbk", "ignore"))
    file.write("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n".encode("gbk", "ignore"))
    file.flush()
    print("+" * 100)

for a in range(1,3):
    # try:
        getAllFriends(a)
    # except:
    #     pass

