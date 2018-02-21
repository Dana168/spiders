import selenium
import selenium.webdriver
import time
from selenium.webdriver.common.keys import Keys


#使用谷歌浏览器
driver=selenium.webdriver.Chrome()


#获取12306登录页面
driver.get("http://kyfw.12306.cn/otn/login/init")


#获取用户名的,输入用户名
driver.find_element_by_id("username").send_keys("用户名")

#输入密码
driver.find_element_by_id("password").send_keys("密码")
time.sleep(5)


while True:
    time.sleep(5)
    print(driver.page_source.find("先生"))
    if driver.page_source.find("先生")!=-1:
        break
    pass


#跳转到订票的页面
selectYuding=driver.find_element_by_id("selectYuding")
selectYuding.click()
print("跳转到订票页面成功")


#始发站
startaddress=driver.find_element_by_id("fromStationText")
startaddress.click()
startaddress.clear()


# startaddress.send_keys("北京")
startaddress.send_keys("深圳")
startaddress.send_keys(Keys.ENTER)


#终点站
endaddress=driver.find_element_by_id("toStationText")
endaddress.click()
endaddress.clear()

endaddress.send_keys("北京")
# endaddress.send_keys("深圳")
endaddress.send_keys(Keys.ENTER)

#点击查询
print("延时30s,如果地址与开始时间有异请进行手动修改。。。")
check=driver.find_element_by_id("query_ticket")
check.click()
time.sleep(20)

#只显示可预订的班次id="avail_ticket"id="avail_ticket"
avail_ticket=driver.find_element_by_id("avail_ticket")
avail_ticket.click()

count=0

while True:
    count+=1

     # 点击查询
    check = driver.find_element_by_id("query_ticket")
    check.click()
    time.sleep(5)

    #班次的表id="queryLeftTable"
    queryLeftTable=driver.find_element_by_id("queryLeftTable")
    print("driver.find_element_by_id(trainu).text",driver.find_element_by_id("trainum").text)
    if driver.find_element_by_id("trainum").text!="0":
        #预定车次
        book=driver.find_element_by_xpath("//*[@id='queryLeftTable']/tr[1]/td[last()]/a")
        book.click()
        time.sleep(3)
    #当跳转到订单详情时不含“备注”这个词
    if driver.page_source.find("备注")==-1:

        #选择乘车的人
        normal_passenger_id=driver.find_element_by_xpath("//*[@id=\"normalPassenger_0\"]")
        normal_passenger_id.click()

        #提交订单
        submitOrder_id=driver.find_element_by_id("submitOrder_id")
        submitOrder_id.click()

        #返回修改
        time.sleep(5)
        break
    print("第%s次查询"%(str(count)))

print("完成")

