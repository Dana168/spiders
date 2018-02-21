import requests
import lxml 
import lxml.etree
import re
url = 'http://shenzhen.taoche.com/all/?page='
response = requests.get(url).content
mytree = lxml.etree.HTML(response)
# myres = mytree.xpath('//div[@id="container_base"]//div[@data-state="1"]')
# for m in myres:
#     mhref = m.xpath('//div[@class="item_details"]/h3/a/@href')
# print(mhref)
myres = mytree.xpath('//div[@id="container_base"]//div[@data-state="1"]')
print(len(myres))
for m in myres:
    mhref = m.xpath('//div[@class="item_details"]/h3/a/@href')
    for i in range(len(mhref)):
        print(mhref[i])
        print(type(mhref[i]))
