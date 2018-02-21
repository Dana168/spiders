'''
进程嵌套线程，线程嵌套协程，完成对开源中国网站 -----开源项目的分类、项目资源、项目信息的提取
'''
import re
import json
import jsonpath as jsonpath
import threading
import multiprocessing
import requests
import lxml
import lxml.etree
import os
import gevent
import gevent.monkey

gevent.monkey.patch_all()  # 自动切换


# 实现项目的分类信息
def getAlltype(url, headers):
    content = requests.get(url, headers=headers).text

    jsonstr = re.findall("param=\"([\s\S]*)</project-sort>", content)
    jsonstr = jsonstr[0].replace("\n", '').replace('\t', '')[:-2]  # 去掉数据中的\n\t和“ "> ”

    datadict = eval(jsonstr, type("Dummy", (dict,), {'__getitem__': lambda s, n: n})())
    datastr = re.sub("\'", "\"", str(datadict))

    jsontree = json.loads(datastr)  # 转化为json对象
    linelist = jsonpath.jsonpath(jsontree, "$..menu.items") 
    baseurl = "https://www.oschina.net/"
    print(len(linelist[0]))  

    for line in linelist[0][1:]:
        name = line["name"]
        print(name)
        childurllist = []
        threadlist = []
        for child in line["childs"]:  
            # 每个大类下的小类
            childname = child["name"]
            childurl = baseurl + child["href"]
            print("------", childname, childurl)

            # 对每个小类开个线程
            mythread = threading.Thread(target=getProjectUrl, args=((name, childname), (childurl, headers)))
            mythread.start()
            threadlist.append(mythread)
        for mythread in threadlist:
            mythread.join()


# 翻页、提取每个项目的链接
def getProjectUrl(args1, args2):
    name, childname = args1
    childurl, headers = args2
    data = requests.get(childurl, headers=headers).text
    mytree = lxml.etree.HTML(data)
    # 总的项目个数num
    total = mytree.xpath("//section[@class='box-aw box main']/div/div[1]/div[1]/text()")[0]
    num = eval(re.findall("\d+", total)[0])
    print(num)
    # 每页20个项目，计算总的页数
    if num % 20 == 0:
        pages = num // 20
    else:
        pages = num // 20 + 1
    # 存储每类下所有项目的url
    urllist = []  
    for i in range(1, pages + 1):
        s = requests.session()
        s.keep_alive = False
        temp = re.findall("\d+", childurl)[0]
        # 翻页
        url = childurl + "?company=0&sort=score&lang=" + temp + "&recommend=false&p=" + str(i)

        # 提取每页所有项目
        data = requests.get(url, headers=headers).text
        mytree = lxml.etree.HTML(data)
        # 每个项目的信息
        linelist = mytree.xpath("//div[@class='lists news-list']//div[@class='box item']//div[@class='box-aw']")
        tasklist = []
        for line in linelist:
            title1 = line.xpath("./a/div[@class='title']/text()")[0].strip()
            title2 = line.xpath("./a/div[@class='title']//span[1]/text()")[0]
            title = title1 + title2
            title = title.replace("/", "").replace(".", "")
            attrproject = line.xpath("./a/div[@class='title']//span[2]/text()")
            suburl = line.xpath("./a/@href")[0]
            urllist.append(suburl)
            print("------------", title, attrproject, suburl)
            # 开启协程，爬取每个项目的详细信息
            tasklist.append(gevent.spawn(getcontent, (name, childname, headers, title, attrproject, urllist)))
        gevent.joinall(tasklist)


# 提取每个项目的详细信息
def getcontent(args):
    name, childname, headers, title, attrproject, urllist = args

    for suburl in urllist:
        s = requests.session()
        s.keep_alive = False
        data = requests.get(suburl, headers=headers).text
        mytree = lxml.etree.HTML(data)

        score = mytree.xpath("//*[@id='v-header']/div/div[1]/div[1]/div/span/text()")  # 得分
        num = mytree.xpath("//*[@id='v-header']/div/div[1]/div[2]/div[1]/span/text()")  # 本类中的排名
        collect = mytree.xpath("//*[@id='v-basic']/footer/div[3]/span/text()")  # 收藏人数
        date = mytree.xpath("//section[@class='sc-container']/div/div/div[4]/header/span/text()")  # 上传日期
        info = mytree.xpath("//div[@class='detail editor-viewer all']")[0]  # 详细介绍
        info = info.xpath("string(.)")  # info为<class 'lxml.etree._ElementUnicodeResult'>，需要转为字符
        info = str(info)
        info = " ".join(info.split())
        date = date[0]
        score = "Score:" + score[0].strip()
        collect = "The number of collection:" + collect[0]
        # attrproject="Type:"+str(attrproject)
        if len(num) == 0:
            num = "In this class ranking：None"
        else:
            num = "In this class ranking：" + num[0]
        print("------------------", score, num, collect, date, info)

        content = title + "\r\n" + suburl + "\r\n" + str(
            attrproject) + "\r\n" + score + "\r\n" + num + "\r\n" + collect + "\r\n" + date + "\r\n" + info
        saveAllData(name, childname, title, content)


# 保存数据
def saveAllData(name, childname, title, content):
    basepath = r"C:\Users\asa_h\Desktop\贺自彩_开源中国爬虫_Python1701\data"
    filename = basepath + "\\" + name + "\\" + childname
    if not os.path.exists(filename):
        os.makedirs(filename)
    else:
        pass
    filename += "\\"
    file = open(filename + title + ".txt", "wb")
    file.write(content.encode("utf-8", "ignore"))
    file.flush()
    file.close()


if __name__ == '__main__':
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'  # 模拟浏览器
    headers = {'User-Agent': user_agent}
    url = "http://www.oschina.net/project"
    process = multiprocessing.Process(target=getAlltype, args=(url, headers))
    process.start()

