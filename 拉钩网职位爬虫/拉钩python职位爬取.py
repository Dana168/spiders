import urllib.request
import urllib
import lxml
import lxml.etree
import selenium
import selenium.webdriver
import time
from selenium.webdriver.common.keys import  Keys

driver = selenium.webdriver.Chrome()
driver.get("https://passport.lagou.com/login/login.html?")
time.sleep(2)
user=driver.find_element_by_xpath("//input[@placeholder=\"请输入常用手机号/邮箱\"]")
password=driver.find_element_by_xpath("//input[@placeholder=\"请输入密码\"]")
user.clear()
password.clear()
time.sleep(1)
user.send_keys("18370880100")
password.send_keys("629828lei")
time.sleep(2)
password.send_keys(Keys.ENTER)
time.sleep(2)

input=driver.find_element_by_xpath("//input[@placeholder=\"搜索职位、公司或地点\"]")
input.send_keys("python")
input.send_keys(Keys.ENTER)
time.sleep(5)


file=open("拉钩python职位分析.txt","wb")
def getdata(data):
    mytree=lxml.etree.HTML(data)
    mydata=mytree.xpath("//*[@id=\"s_position_list\"]//ul[@class=\"item_con_list\"]")
    pythonlist=[]
    idlist=[]
    conpanylist=[]
    moneylist=[]
    yearlist=[]

    for line in mydata:
        pythonlist=line.xpath("//a[@class=\"position_link\"]/h3/text()")
        idlist=line.xpath("//a[@class=\"position_link\"]/span/em/text()")
        conpanylist=line.xpath("//div[@class=\"company_name\"]/a/text()")
        moneylist=line.xpath("//span[@class=\"money\"]/text()")
        yearlist=line.xpath("//div[@class=\"li_b_r\"]/text()")
        mystr = ""
        for i in range(len(pythonlist)):
            print(pythonlist[i],idlist[i],conpanylist[i],moneylist[i],yearlist[i])
            mystr+=pythonlist[i]
            mystr+="#"
            mystr += idlist[i]
            mystr += "#"
            mystr += conpanylist[i]
            mystr += "#"
            mystr += moneylist[i]
            mystr += "#"
            mystr+=yearlist[i]
            mystr+="\r\n"
        return mystr

i=0
while True:
    i+=1
    js = "document .body .scrollTop =10000"
    driver.execute_script(js)
    time.sleep(3)
    page = driver.find_element_by_class_name("pager_next")
    page.click()
    time.sleep(2)
    getdata(driver.page_source)
    file.write(getdata(driver.page_source).encode("utf-8"))
    if    i>=30:
        break
file.close()