import selenium
import selenium.webdriver
import time
import lxml
import lxml.etree
import requests

#selenium 访问京东登录页面
url = "https://passport.jd.com/new/login.aspx"
driver = selenium.webdriver.Chrome()
driver.get(url)
time.sleep(5)

#跳转到账户登录界面
zhanghu = driver.find_element_by_xpath("//*[@class=\"login-tab login-tab-r\"]/a")
zhanghu.click()
time.sleep(3)

#模拟获取用户名，密码和登录节点
user = driver.find_element_by_id("loginname")
password = driver.find_element_by_id("nloginpwd")
submit = driver.find_element_by_id("loginsubmit")
user.clear()
password.clear()
time.sleep(3)

#
user.send_keys(u"用你的账号和密码")
time.sleep(1)
password.send_keys("用你的账号和密码")
time.sleep(5)
submit.click()
time.sleep(15)
cookies = driver.get_cookies()  #抓取全部到cookie
# driver.close()


print("开始会话")
req = requests.session()
# cookies = driver.get_cookies()  #抓取全部到cookie
for cookie in cookies:
    req.cookies.set(cookie['name'],cookie["value"])
req.headers.clear()#清空头
newpage = req.get("https://cart.jd.com/cart.action")
print("会话完成")
# print newpage.text

# 抓取价格
# mytree=lxml.etree.HTML(newpage.text  )
# gwclist = mytree.xpath("//*[@class=\"cell p-price\"]/strong/text()")
# print gwclist
# for hw in gwclist:
#     print hw


mytree=lxml.etree.HTML(newpage.text  )
gwclist = mytree.xpath("//*[@id=\"vender_8888\"]//div[@class=\"p-name\"]/a//text()")
# print gwclist
count=0
file = open("jidong.txt","wb")
# print gwclist
for hw in gwclist:
    if hw.strip():
        count+=1
        print(hw.strip())
        text = hw.strip()
        file.write(text.encode("utf-8"))
print (count)



file.close()

print("访问完成")
time.sleep(20)
#
# time.sleep(20)
driver.close()