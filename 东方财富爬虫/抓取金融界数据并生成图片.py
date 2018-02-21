import threading
import  urllib
import time
import requests,re,json,time,os
import lxml
import lxml.etree
from matplotlib import pyplot
import matplotlib
import  matplotlib.pyplot as plt #数据可视化
from aip import AipNlp

#页码，当不翻页时，bug,

pyplot.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
pyplot.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

#得到最大页码的数值
def getallpage(url):
    pagedata = requests.get(url).content.decode("gbk")
    # print(pagedata)
    mytree = lxml.etree.HTML(pagedata)
    #取所有的页码数
    #如果有翻页
    if  pagedata.find("page_newslib"):
        data = mytree.xpath("//*[@class=\"page_newslib\"]//a[last()-1]/text()")
        return data  #['11']

    else:
        return ['1']

#得到页面的内容并保存
def everypagecontent(url,number):
    #解决服务器延时的问题try
    try:
        pagedata = requests.get(url).content.decode("gbk")
        mytree = lxml.etree.HTML(pagedata)
        # print(pagedata)
        # 取所有的内容
        datas = mytree.xpath("//*[@class = \"newlist\"]//li/span/a/text()")
        for data in datas:
            data= data+"\r\n"
            with open(number+".txt","a") as file:
                file.write(data)
                file.flush()
        return datas
    except:
        print("服务器超时")

#调用接口，情感分析
def analyze(number):
    """ 你的 APPID AK SK """
    APP_ID = '10254109'
    API_KEY = 'vnOAq33nhaWqcoTmjfxOOgKI'
    SECRET_KEY = 'praR1key1GSpmZu5P9mzeVHXwDKnjoLO  '

    pos = 0
    nav = 0
    i = 0

    aipNlp = AipNlp(APP_ID, API_KEY, SECRET_KEY)
    for line in open(number+".txt","r",encoding="gbk"):
        aline = line.replace("\r\n","").strip()
        # if len(aline) != 0:
        try:
            result = aipNlp.sentimentClassify(aline) #调用百度接口，情感分析
            positive = result['items'][0]['positive_prob']
            nagative = result['items'][0]['negative_prob']

            i += 1
            if positive >= nagative:
                pos += 1
            else:
                nav += 1
            avgpos = pos / i
            navavg = nav/i
            print(i, format(avgpos,".4f"),format(navavg,".4f"))
        except:
            pass
            # else:
            #     pass
    plt.bar([1], [avgpos], label=number + u"积极的", color="g")
    plt.bar([2], [navavg], label=number + u"消极的", color="b")

    plt.legend()  # 绘制
    plt.savefig(number + ".jpg")
    plt.show()  # 显示
    # return number, format(avgpos, ".4f"), format(navavg, ".4f")

def picture():
    number, postive, navtive = analyze()
    print(number,postive,navtive)
    plt.bar([1], [navtive], label=number+u"积极的", color="g")
    plt.bar([2], [postive], label=number+u"消极的", color="b")
    # matplotlib.use("Agg")
    plt.legend()  # 绘制
    plt.savefig(number+".jpg")
    plt.show() #显示

def getpageurl(url):
    pagenumber = getallpage(url)[0]
    # print(pagenumber)
    for i in range(1, int(pagenumber) + 1):
        try:
            if i == 1:
                url = "http://stock.jrj.com.cn/share," + number + ",ggxw.shtml"
            else:
                url = "http://stock.jrj.com.cn/share," + number + ",ggxw_" + str(i) + ".shtml"
        except:
            pass
        print(everypagecontent(url, number))


numbers = ['300256','600006',"600028","600000"]

#得到股票名称，获取新闻信息生成文件
# for number in numbers:
#     # print(number)
#     url = "http://stock.jrj.com.cn/share,"+number+",ggxw.shtml"
    # getpageurl(url)


#读取文件
for number in numbers:
    print(number)
    analyze(number)
    # thlist=[]
    # for i in range(len(numbers)):
    #     print(len(numbers))
    #     print(numbers[i])
    #     threading.Thread(target=analyze(),args=(number,)).start()

