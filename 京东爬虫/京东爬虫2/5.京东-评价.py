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
time.sleep(5)

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

# 抓取评论的链接
mytree=lxml.etree.HTML(newpage.content.decode("utf-8"))
pinglunlist = mytree.xpath("//*[@id=\"J_goodsList\"]/ul/li[1]/div/div[5]/strong/a/@href")
print(pinglunlist[0])
newurl = pinglunlist[0]
newurl = "http:"+ newurl

# 抓取评论的页面
plpage = requests.get(newurl)
# print(plpage.content.decode("gbk"))

wangpingtree = lxml.etree.HTML(plpage.content.decode("gbk"))
wplist = wangpingtree.xpath("//*[@id=\"comment-0\"]/div[@class=\"comment-item\"]/text()")
print(wplist)


print("访问完成")
time.sleep(10)
#
# time.sleep(20)
driver.close()