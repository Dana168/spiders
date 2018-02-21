import selenium.webdriver
import lxml
import lxml.etree
import requests
import pymongo 
# url = 'http://shenzhen.taoche.com/all/'
import selenium
import selenium.webdriver
import time
import urllib
def getinfo(url):
    response = requests.get(url).text
    # print(response)
    mytree = lxml.etree.HTML(response)
    myres = mytree.xpath('//div[@id="container_base"]//div[@data-state="1"]')
    for m in myres:
        mlist = m.xpath('//div[@class="item_details"]/h3/a/text()')
        mhref = m.xpath('//div[@class="item_details"]/h3/a/@href')
    # print(mlist)
    # print(mhref)
    # print(len(myres))
    return mhref

def geturllist():
    urllist = []
    for i in range(1,51):
        url = 'http://shenzhen.taoche.com/all/?page='+str(i)
        urllist.append(url)
    return urllist
# http://shenzhen.taoche.com/all/?page=50#pagetag

def getCarinfo(url):
    response = requests.get(url).text
    # print(response)
    mytree = lxml.etree.HTML(response)
    myname = mytree.xpath('//div[@class="summary-title"]/h1/text()')[0]
    print(myname)
    myres = mytree.xpath('//div[@class="summary-attrs"]//dt')
    for data in myres:
        alist = data.xpath('//dt/text()')[0:4]
        blist = data.xpath('//dd/text()')[0:4]
    # print(len(myres))

    print(alist,blist)
    return myname,alist,blist

if __name__ == '__main__':
    client = pymongo.MongoClient(host='127.0.0.1', port=27017)
    db = client['yiche']
    user = db['carinfo']

    urllist = geturllist()
    print(urllist)
    mhrefdata = []
    for url in urllist:
        mhref = getinfo(url)
        mhrefdata.append(mhref)
    # url = 'http://www.taoche.com/buycar/b-dealer17102111748.html'
    for i in range(len(mhrefdata)):
        for j in range(len(mhrefdata[0])):
            myname, alist, blist=getCarinfo(mhrefdata[i][j])
            user.insert({'carname':myname,alist[0]:blist[0],alist[1]:blist[1],alist[2]:blist[2],alist[3]:blist[3]})

    client.close()


    # url = 'https://home.taoche.com/'
    # cookies = {}
    # driver = selenium.webdriver.Chrome()
    # driver.get(url)
    # time.sleep(10)
    # login = driver.find_element_by_id('1')
    # login.click()
    # time.sleep(3)
    # username = driver.find_element_by_id('mobile1')
    # password = driver.find_element_by_id('password')
    # time.sleep(3)
    # username.send_keys('17150304377')
    # password.send_keys('210342866@qq')
    # time.sleep(3)
    #
    #
    # page_source = driver.page_source
    # mytree = lxml.etree.HTML(page_source)
    # img = mytree.xpath('//div[@id="GetImgValidateCode1"]/img/@src')[0]
    # print(img)
    # img = 'https://home.taoche.com'+str(img)
    # print(img)
    # urllib.request.urlretrieve(img,'b.jpg')
    #
    # loginbtn = driver.find_element_by_id('user-btn1')
    # loginbtn.click()
    # time.sleep(10)
    # driver.get('https://home.taoche.com/')
    # time.sleep(3)
    # page_source = driver.page_source
    # print(page_source)
    # driver.close()