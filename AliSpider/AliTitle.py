# -*- coding: utf-8 -*-

import requests
import re,json,simplejson
import time
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import jieba

def getData():
    url="http://job.alibaba.com/zhaopin/socialPositionList/doList.json"
    payload={"pageIndex":1,"pageSize":10}
    r=requests.post(url,payload)
    title=file("title.data",'w')
    print>>title,str(r.text.encode('utf-8'))

def parse():   
    js=json.loads(open("title.json").read())
    print js.get('returnValue','').get('totalRecord','')
    jobs=js.get('returnValue','').get('datas','')
    job=file("job.data",'w')
    for item in jobs:
        id=item.get('id','')
        name=item.get('name','').encode('utf-8')
        status=item.get('status','')
        des=item.get('description','').encode('utf-8')
        code=item.get('item','')
        dept=item.get('departmentName','').encode('utf-8')
        wl=item.get('workLocation','').encode('utf-8')
        we=item.get('workExperience','').encode('utf-8')
        rn=item.get('recruitNumber','')
        isOpen=item.get('isOpen','')
        dptId=item.get('departmentId','')
        fc=item.get('firstCategory','').encode('utf-8')
        sc=item.get('secondCategory','').encode('utf-8')
        dg=item.get('degree','').encode('utf-8')
        rq=item.get('requirement','').encode('utf-8')
        isNew=item.get('isNew','')
        gmtCreate=item.get('gmtCreate',1)
        tm=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(gmtCreate/1000))
        gmtModified=item.get('gmtModified',1)
        gm=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(gmtModified/1000))
        print >>job,str(rq)
       # print>>job,str(id)+'\t'+str(name)+'\t'+str(status)+'\t'+str(des)+'\t'+str(dept)+'\t'+str(wl)+'\t'+str(we)+'\t'+str(rn)+'\t'+str(fc)+'\t'+str(sc)+'\t'+str(dg)+'\t'+str(rq)+'\t'+str(isNew)+'\t'+str(tm)+'\t'+str(gm)

def draw():
    t=open('job.txt').read()
    w=jieba.cut(t)
    wl=' '.join(w)
    font=r'DroidSansFallbackFull.ttf'
    my_wordcloud = WordCloud(font_path=font).generate(wl)
    plt.imshow(my_wordcloud)
    plt.axis("off")
    plt.show()

if __name__=="__main__":
   # getData()
   # parse()
   draw()
