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

#登录京东
user.send_keys(u"用你的账号和密码")
time.sleep(1)
password.send_keys("用你的账号和密码")
time.sleep(5)
submit.click()
time.sleep(15)
# cookies = driver.get_cookies()  #抓取全部到cookie
# driver.close()
# print "开始会话"
# req = requests.session()
# # cookies = driver.get_cookies()  #抓取全部到cookie
# for cookie in cookies:
#     req.cookies.set(cookie['name'],cookie["value"])
# req.headers.clear()#清空头
# newpage = req.get("https://cart.jd.com/cart.action")
# print "会话完成"
# print newpage.text

# 抓取价格
# mytree=lxml.etree.HTML(newpage.text  )
# gwclist = mytree.xpath("//*[@class=\"cell p-price\"]/strong/text()")

intputsp = driver.find_element_by_id("key")
intputsp.clear()
intputsp.send_keys(u"小米手机")
time.sleep(2)

sosou = driver.find_element_by_xpath("//*[@id=\"search\"]/div/div[2]/button/i")
sosou.click()
time.sleep(5)

xiaoliang = driver.find_element_by_xpath("//*[@id=\"J_filter\"]/div[1]/div[1]/a[2]")
xiaoliang.click()
time.sleep(3)

url = "https://search.jd.com/Search?keyword=%E5%B0%8F%E7%B1%B3%E6%89%8B%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&bs=1&wq=%E5%B0%8F%E7%B1%B3%E6%89%8B%E6%9C%BA&ev=exbrand_%E5%B0%8F%E7%B1%B3%EF%BC%88MI%EF%BC%89%5E&psort=3&click=0"
newpage = requests.get(url)
# print(newpage.content.decode("utf-8"))

mytree=lxml.etree.HTML(newpage.content.decode("utf-8"))
# namelist = mytree.xpath("//*[@id=\"J_goodsList\"]/ul//li/div/div[5]/strong/a/@href")
#
namelist = mytree.xpath("//*[@id=\"J_goodsList\"]/ul//li/div/div[4]/a/em/text()")
for name in namelist:
    if name.strip():
        print(name.strip())




print("访问完成")
time.sleep(10)
#
# time.sleep(20)
driver.close()