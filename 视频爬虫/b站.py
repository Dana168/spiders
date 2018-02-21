# -*- coding: utf-8 -*-
'''
add your question
'''
import json
import re
import jsonpath as jsonpath
import requests
import pymysql as pymysql

def func():
    headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.9',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        'Cookie':'finger=edc6ecda; fts=1508944686; sid=62s63tfl; buvid3=B374C37F-D452-494B-B343-FAC4AE0661DB26591infoc; pgv_pvi=586080256; rpdid=ipoxmoqsxdoswqlppxqw; DedeUserID=29961182; DedeUserID__ckMd5=ce47392e967d94c9; LIVE_BUVID=AUTO2115089450714838; _cnt_pm=0; _cnt_notify=0; pgv_si=s764438528; purl_token=bilibili_1509904889; SESSDATA=8db08fb0%2C1512497031%2C9dcac2ed; bili_jct=f00df99cb2906de16ca7e4a4f4a2d19b',
        'Host':'comment.bilibili.com',
        'Upgrade-Insecure-Requests':'1',
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3236.0 Safari/537.36"}
    for i in range(1000000):
        url="https://comment.bilibili.com/recommendnew,{}".format(i)
        print(url)
        try:
            req = requests.get(url,headers, timeout=6).content
            # req.encoding = 'utf-8'
            # req=req.text
            req=req.decode("utf-8", "ignore")
            jsontree=json.loads(req)    #������json
            title=jsonpath.jsonpath(jsontree,"$..title")  #����json,�������ڵ��������е�title,..��ʾ��ǰ�ڵ�
            tname=jsonpath.jsonpath(jsontree,"$..tname")  #����
            pattern = re.compile('"aid":(\d+),"vie')     #��Ϊaid�ظ���������Ҫ����
            aid = pattern.findall(req)
            view =jsonpath.jsonpath(jsontree,"$..view")
            danmaku = jsonpath.jsonpath(jsontree,"$..danmaku")
            for b in range(len(aid)):
                print('���⣺%s��ID��%s�����ͣ�%s,�ۿ�����%s����Ļ����%s'%(title[b],aid[b],tname[b],view[b],danmaku[b]))
                # ��ȡ��ѯsql�α�
                cursor.execute(
                    "insert into bilibili(title,aid,tname,view,danmaku) values('%s','%s','%s','%s',%s)" %
                    (str(title[b]), str(aid[b]),str(tname[b]),str(view[b]),str(danmaku[b])))
                # �ύ
                conn.commit()
        except:
            print("ҳ�涪��")
    conn.close()

if __name__ == '__main__':
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='314251612', db='b_station', charset='utf8')
    cursor = conn.cursor()
    cursor.execute(
        "create table bilibili(id INT PRIMARY KEY AUTO_INCREMENT,title varchar(100),aid int (20),tname varchar(50),view int (20),danmaku int (20))")
    func()


