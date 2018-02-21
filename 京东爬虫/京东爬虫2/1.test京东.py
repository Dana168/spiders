import requests
import lxml
import lxml.etree
import time


url = "https://search.jd.com/Search?keyword=%E5%B0%8F%E7%B1%B3%E6%89%8B%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&bs=1&wq=%E5%B0%8F%E7%B1%B3%E6%89%8B%E6%9C%BA&ev=exbrand_%E5%B0%8F%E7%B1%B3%EF%BC%88MI%EF%BC%89%5E&psort=3&click=0"
newpage = requests.get(url)
# newpage = newpage.encoding("utf-8")#发现了什么


# print(newpage.content.decode("utf-8"))


mytree=lxml.etree.HTML(newpage.content.decode("utf-8"))
# namelist = mytree.xpath("//*[@id=\"J_goodsList\"]/ul//li[@class=\"gl-item\"]/text()")
pinglunlist = mytree.xpath("//*[@id=\"J_goodsList\"]/ul/li[1]/div/div[5]/strong/a/@href")

# namelist = mytree.xpath("//*[@id=\"J_goodsList\"]/ul//li/div/div[4]/a/@href")
# print(namelist[0])
newurl = pinglunlist[0]
newurl = "http:"+ newurl

plpage = requests.get(newurl)
time.sleep(5)
# print(plpage.content.decode("gbk"))
# namelist = mytree.xpath("//*[@id=\"J_goodsList\"]/ul//li/div/div[5]/strong/a/@href")
#
# for name in namelist:
#     if name.strip():
#         print(name.strip())

wangpingtree = lxml.etree.HTML(plpage.content.decode("gbk"))
# print(wangpingtree)

# wplist = wangpingtree.xpath("//*[@id=\"comment-0\"]//div[@class=\"comment-item\"]/div[@class=\"user-info\"]/text()")

# wplist = wangpingtree.xpath("//*div[@class=\"tab-con\"]/[@id=\"comment-0\"]//div[@class=\"comment-item\"]/div[@class=\"user-info\"]//text()")
# for i in wplist:
#     print(i)

# print(wplist)
