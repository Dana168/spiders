import multiprocessing
import multiprocessing.managers

import requests
import re
import lxml
import lxml.etree
import time

def pagexpath(url):
    response = requests.get(
        url,
        headers={"User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0);"}
    ).content.decode("utf-8")

    # print(response)

    mytree = lxml.etree.HTML(response)
    homelist = mytree.xpath("//*[@class=\"f-list-item ershoufang-list\"]")

    datalist = []
    for line in homelist:

        home = line.xpath("./dl/dd[1]/a/text()")[0].strip()

        pattern = ""
        patternlist = line.xpath("./dl/dd[2]//span/text()")
        # print(len(addrlist))
        for  i in range(len(patternlist)) :
            pattern += patternlist[i].strip()
            pattern.strip()
            # print(add)

        addr = ""
        addr1 = line.xpath("./dl/dd[3]/span//a/text()")
        for i in range(len(addr1)):
            addr += addr1[i].strip()

        money = ""
        moneylist = line.xpath("./dl/dd[5]/div[1]//span/text()")
        for i in range(len(moneylist)):
            money += moneylist[i]
        datetime = line.xpath("./dl/dd[5]/div[2]/text()")[0]

        mystr =""
        mystr += home
        mystr += " # "
        mystr += pattern
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
    manger=QueueManger(address=("127.0.0.1",8848),authkey=b"111111")
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
