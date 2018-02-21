'''
分布式服务端
负责收集分类连接和每一种的所有页面
'''
import multiprocessing.managers
import multiprocessing
import multiprocessing
import queue,pymongo
import lxml,lxml.etree
import random
import urllib,urllib.request
import time
import threading

task_queue = queue.Queue()
result_queue = queue.Queue()


def task_return():
    return task_queue
def result_return():
    return result_queue


class QueManager(multiprocessing.managers.BaseManager):
    pass

recount = 0
def getpagedata(url):
    global recount
    try:
        header = [{"User-Agent": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"},
                  {"User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)"},
                  {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"},
                  {"User-Agent": "Opera/9.80(WindowsNT6.1;U;en)Presto/2.8.131Version/11.11"},
                  {"User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)"}]
        # random.randint(0,4)  包含0和4
        respon = urllib.request.Request(url, headers=header[random.randint(0, 4)])
        pagespurce = urllib.request.urlopen(respon, timeout=8)
        time.sleep(3)
        #检测是否成功打开网页
        if pagespurce.code!=200:
            print('-------',pagespurce.code)
            time.sleep(2)
            getpagedata(url)
        else:
            return pagespurce.read().decode('utf-8','ignore')
    #如果连接超时，迭代打开网页
    except Exception as e:
        print(e)
        time.sleep(3)
        recount += 1
        # 限制迭代的次数  （3次）
        if recount<4:
            getpagedata(url)
        else:
            recount = 0
            return 0

def kinds(urlbank):
    ur2 = 'http://list.youku.com/category/video/c_0.html'
    source = getpagedata(ur2)
    # 判断页面数据是否可用
    if type(source)==str:
        mytree = lxml.etree.HTML(source)
        kindlist = mytree.xpath('//div[@id=\"filterPanel\"]/div[@class=\"item noborder\"]/ul//li')
        for i in range(1, len(kindlist)):
            kurl = 'http://list.youku.com' + kindlist[i].xpath('./a/@href')[0]
            urlbank.append(kurl)
        return urlbank
    else:
        kinds(urlbank)

def pages(url,task):
    source = getpagedata(url)
    if type(source)==str:
        mytree = lxml.etree.HTML(source)
        num = mytree.xpath('//ul[@class=\"yk-pages\"]//li[last()-1]/a/text()')
        newurl =url.replace('.html','')
        if len(num)!=0:
            for i in range(1, eval(num[0])+1):
                purl = newurl+'_s_1_d_1_p_' + str(i) + '.html'
                task.put(purl)
                print(purl,'---------已放入任务附列----------')
    else:
        Errorbank.append(url)

def mongosave(result):
    # client = pymongo.MongoClient(host='10.36.132.235',port=27017)
    file = open(r'./mvinfor.txt','w')
    while True:
        try:
            # result_queque.empty() 永远为空
            #正确的方法是用 result.empty()
            if result.empty():
                time.sleep(5)
            else:
                doc = result.get()
                print('------获取数据------', doc)
                # 列表无法写入 txt
                for line in doc:
                    file.write(str(line).encode('utf-8','ignore').decode('utf-8','ignore')+' , ')
                file.write('\n')
                file.flush()
        except Exception as e:
            print('>>>>>>>>>----- 写入错误 --%s--<<<<<<<<'%e)
    file.close()
    # client.close()


if __name__ == "__main__":
    Errorbank = []
    multiprocessing.freeze_support()
    QueManager.register('get_task',callable=task_return)
    QueManager.register('get_result',callable=result_return)
    manager = QueManager(address=('10.36.132.54',6558),authkey=123456)
    manager.start()
    task,result=manager.get_task(),manager.get_result()
    urlbank = []
    urlbanks = kinds(urlbank)
    for url in urlbank:
        threading.Thread(target=pages,args=(url,task)).start()
    # 单独开启一条线程存储数据
    threading.Thread(target=mongosave,args=(result,)).start()
    # 有下面的while
    while True:
        if len(Errorbank)!=0:
            url = Errorbank.pop()
            t = threading.Thread(target=pages, args=(url, task))
            t.start()
        else:
            time.sleep(10)
