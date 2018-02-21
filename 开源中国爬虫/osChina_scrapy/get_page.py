# coding:utf-8
import requests
import lxml
from lxml import etree
#shit
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0"}
req = requests.get("https://www.oschina.net/project/zhlist/331/mobile-dev", headers=headers)
html = req.content.decode("utf-8")
mytree = lxml.etree.HTML(html)
content = mytree.xpath("//div[@class = \"panel-list news-list\"]//a[@class=\"item\"]")
for text in content:
    url = text.xpath("./@href")
    title = text.xpath(".//div[@class=\"title\"]//text()")
    summary = text.xpath(".//div[@class=\"summary\"]//text()")
    time = text.xpath(".//footer//text()")
    # print(url)
    # print(title[0].strip()+title[1].strip())
    # print("---")
    print(time[0].strip()+time[1].strip()+time[2].strip()+time[3].strip()+time[4].strip())
    # for i in time:
    #     print(i.strip())
    # print(summary[0].strip())

