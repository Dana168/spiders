import gevent.monkey
import re
import requests
import lxml
import lxml.etree

gevent.monkey.patch_all()  # 自动切换


def download(urllist, file):
    try:
        for url in urllist:
            content = requests.get(url).text
            mytree = lxml.etree.HTML(content)
            linelist = mytree.xpath("//div[@class=\"f-list-item ershoufang-list\"]/dl")
            for line in linelist:
                namelist = line.xpath("./dd[@class=\"dd-item title\"]/a/text()")
                arealist = line.xpath("./dd[@class=\"dd-item size\"]/span[5]/text()")
                pricelist = line.xpath("./dd[@class=\"dd-item info\"]/div/span[1]/text()")
                unitlist = line.xpath("./dd[@class=\"dd-item info\"]/div/span[2]/text()")
                restr = "(\d+)"  # 正则表达式，（）只要括号内的数据
                regex = re.compile(restr, re.IGNORECASE)
                arealist = regex.findall(arealist[0])
                try:
                    averprice = int(eval(pricelist[0]) / eval(arealist[0]))
                except IndexError:
                    arealist = line.xpath("./dd[@class=\"dd-item size\"]/span[3]/text()")
                    arealist = regex.findall(arealist[0])
                    averprice = int(eval(pricelist[0]) / eval(arealist[0]))
                print(namelist[0], arealist[0], pricelist[0], unitlist[0], averprice)
                mygetstr = ""
                mygetstr += namelist[0]
                mygetstr += "    "
                mygetstr += arealist[0]
                mygetstr += "    "
                mygetstr += pricelist[0]
                mygetstr += unitlist[0]
                mygetstr += "    "
                mygetstr += str(averprice)
                mygetstr += "元/月/㎡"
                mygetstr += "\r\n"  # 换行
                file.write(mygetstr.encode("utf-8", errors="ignore"))
    except:
        print("error")


urllist = []
for i in range(1, 101):
    url = "http://sz.ganji.com/fang1/o" + str(i) + "/"
    urllist.append(url)
file = open("赶集租房.txt", "wb")
xclist = [[], [], [], [], [], [], [], [], [], []]
N = len(xclist)
for i in range(len(urllist)):
    xclist[i % N].append(urllist[i])  # 求模切割
tasklist = []
for i in range(N):
    tasklist.append(gevent.spawn(download, xclist[i], file))
gevent.joinall(tasklist)

file.close()
filepath = "赶集租房.txt"
readfile = open(filepath, "rb")
mydatalist = readfile.readlines()
mynewlist = []
for line in mydatalist:
    line = line.decode("utf-8", "ignore")
    line = line.replace("元/月/㎡", "    元/月/㎡").replace("\r\n", "")
    linelist = line.split("    ")
    try:
        if linelist[2].find("元/月") != -1:
            linelist[1] += "㎡"
            print(linelist)
            mynewlist.append(linelist)  # 存储列表，每个元素都是列表
    except:
        print("error")
readfile.close()

mynewlist.sort(key=lambda x: eval(x[3]))  # 根据第三个排序，转化为整数

savefile = open("租房均价最低.txt", "w", encoding="utf-8")
for data in mynewlist:
    print(data)
    savefile.write(str(data) + "\r\n")
savefile.close()
