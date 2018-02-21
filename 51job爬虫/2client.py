import multiprocessing
import multiprocessing.managers

import requests
import re
import lxml
import lxml.etree
import time



def pagexpath(url):
    headers = {"User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0);"}
    response = requests.get(url,headers=headers).content.decode("gbk")
    # print(response)
    mytree = lxml.etree.HTML(response)

    joblist = mytree.xpath("//*[@id=\"resultList\"]//div[@class=\"el\"]")
    datalist = []
    for line in joblist:
        mystr = ""
        job = line.xpath("./p/span/a/text()")[0].strip()
        company = line.xpath("./span[1]/a/text()")[0].strip()
        addr = line.xpath("./span[2]/text()")[0].strip()
        money = line.xpath("./span[3]/text()")
        if len(money) == 0:
            money = ""
        else:
            money = money[0].strip()
        datetime = line.xpath("./span[4]/text()")[0].strip()

        mystr += job
        mystr += " # "
        mystr += company
        mystr += " # "
        mystr += addr
        mystr += " # "
        mystr += money
        mystr += " # "
        mystr += datetime
        mystr += "\r\n"


        datalist.append(mystr)

    # print datalist

    return  datalist
class  QueueManger(multiprocessing.managers.BaseManager):#继承，进程管理共享数据
    pass
if __name__=="__main__":
    QueueManger.register("get_task")  # 注册函数调用服务器
    QueueManger.register("get_result")
    manger=QueueManger(address=("127.0.0.1",8888),authkey=b"100000")
    manger.connect()  #链接服务器
    task= manger.get_task()
    result =manger.get_result()  # 任务，结果

    for i  in range(1000):
        time.sleep(1)
        try:
            url=task.get()
            print ("client get",url)
            datalist= pagexpath(url)
            for  line  in  datalist: #结果队列
                print (line)
                result.put(line)
        except:
            print ("error")
            pass
