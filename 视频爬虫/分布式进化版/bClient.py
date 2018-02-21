#coding:utf-8
import multiprocessing.managers #分布式进程管理器
import random,time  #随机数，时间
import gevent.monkey
import json
import re
import jsonpath as jsonpath
import requests

class  QueueManger(multiprocessing.managers.BaseManager):#继承，进程管理共享数据
    pass

def  getinfo(url):
    try:
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': 'finger=edc6ecda; fts=1508944686; sid=62s63tfl; buvid3=B374C37F-D452-494B-B343-FAC4AE0661DB26591infoc; pgv_pvi=586080256; rpdid=ipoxmoqsxdoswqlppxqw; DedeUserID=29961182; DedeUserID__ckMd5=ce47392e967d94c9; LIVE_BUVID=AUTO2115089450714838; _cnt_pm=0; _cnt_notify=0; pgv_si=s764438528; purl_token=bilibili_1509904889; SESSDATA=8db08fb0%2C1512497031%2C9dcac2ed; bili_jct=f00df99cb2906de16ca7e4a4f4a2d19b',
            'Host': 'comment.bilibili.com',
            'Upgrade-Insecure-Requests': '1',
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3236.0 Safari/537.36"}
        req = requests.get(url, headers, timeout=6).content
        req = req.decode("utf-8", "ignore")
        jsontree = json.loads(req)  # 加载至json
        title = jsonpath.jsonpath(jsontree, "$..title")  # 解析json,解析根节点下面所有的title,..表示当前节点
        tname = jsonpath.jsonpath(jsontree, "$..tname")  # 类型
        pattern = re.compile('"aid":(\d+),"vie')  # 因为aid重复，所以需要正则
        aid = pattern.findall(req)
        view = jsonpath.jsonpath(jsontree, "$..view")
        danmaku = jsonpath.jsonpath(jsontree, "$..danmaku")
        clist=[]
        for b in range(len(aid)):
            # print('标题：%s，ID：%s，类型：%s,观看量：%s，弹幕量：%s' % (title[b], aid[b], tname[b], view[b], danmaku[b]))
            clist.append([title[b], aid[b], tname[b], view[b], danmaku[b]])
            print("内容：",[title[b], aid[b], tname[b], view[b], danmaku[b]])

        result.put(clist)
    except:
        print('下载出错')

if __name__=="__main__":
    QueueManger.register("get_task")  # 注册函数调用服务器
    QueueManger.register("get_result")
    manger=QueueManger(address=("192.168.0.107",8888),authkey="123456".encode('utf-8'))
    manger.connect()  #链接服务器
    task= manger.get_task()
    result =manger.get_result()  # 任务，结果
    for i  in range(1000):
        time.sleep(1)
        geturllist = []  # url列表
        tasklist = []  # 任务列表
        try:
            url = task.get(timeout=1)  # 服务器抓取一个url
            geturllist.append(url)
        except Exception as e:
            print('接收超时吧',e)
        print('urllist>>>>>>>>>>>>>>>>>',geturllist)
        for url in geturllist:  # 根据urllist,新建一个协程组，自动切换
            tasklist.append(gevent.spawn(getinfo, url))
        gevent.joinall(tasklist)
