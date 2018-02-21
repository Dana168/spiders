#coding:utf-8
import multiprocessing.managers #�ֲ�ʽ���̹�����
import random,time  #�������ʱ��
import gevent.monkey
import json
import re
import jsonpath as jsonpath
import requests

class  QueueManger(multiprocessing.managers.BaseManager):#�̳У����̹���������
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
        jsontree = json.loads(req)  # ������json
        title = jsonpath.jsonpath(jsontree, "$..title")  # ����json,�������ڵ��������е�title,..��ʾ��ǰ�ڵ�
        tname = jsonpath.jsonpath(jsontree, "$..tname")  # ����
        pattern = re.compile('"aid":(\d+),"vie')  # ��Ϊaid�ظ���������Ҫ����
        aid = pattern.findall(req)
        view = jsonpath.jsonpath(jsontree, "$..view")
        danmaku = jsonpath.jsonpath(jsontree, "$..danmaku")
        clist=[]
        for b in range(len(aid)):
            # print('���⣺%s��ID��%s�����ͣ�%s,�ۿ�����%s����Ļ����%s' % (title[b], aid[b], tname[b], view[b], danmaku[b]))
            clist.append([title[b], aid[b], tname[b], view[b], danmaku[b]])
            print("���ݣ�",[title[b], aid[b], tname[b], view[b], danmaku[b]])

        result.put(clist)
    except:
        print('���س���')

if __name__=="__main__":
    QueueManger.register("get_task")  # ע�ắ�����÷�����
    QueueManger.register("get_result")
    manger=QueueManger(address=("192.168.0.107",8888),authkey="123456".encode('utf-8'))
    manger.connect()  #���ӷ�����
    task= manger.get_task()
    result =manger.get_result()  # ���񣬽��
    for i  in range(1000):
        time.sleep(1)
        geturllist = []  # url�б�
        tasklist = []  # �����б�
        try:
            url = task.get(timeout=1)  # ������ץȡһ��url
            geturllist.append(url)
        except Exception as e:
            print('���ճ�ʱ��',e)
        print('urllist>>>>>>>>>>>>>>>>>',geturllist)
        for url in geturllist:  # ����urllist,�½�һ��Э���飬�Զ��л�
            tasklist.append(gevent.spawn(getinfo, url))
        gevent.joinall(tasklist)
