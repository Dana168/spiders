'''
分布式客户端
抓取各类每一页的电视剧或电影
抓取电影的详细信息

思路：
    服务器通过抓取优酷 视频 的所有分类，进而 将这些 类别里面的所有页面 发给客户端，
    客户端 则 开线程（限制并发量）抓取每一个页面的所有 视频链接 并获取部分信息，
    （碰到的问题：优酷为了 反扒 设置了两套页面结构， 爆破：通过 if 判断选择哪一套，解决方案）
    然后开 协程 将这些信息 传入协程，
    协程处理这些页面时， 由于视频的类别繁多， 固 不管是否抓到（电影等，是没有选集的） 视频选集信息，都应该将所有的信息
    传回 服务端

    对于线程和协程 打开错误的 链接 ，将其分别传入连个专门的列表，在单独开两条 线程 处理
'''


import multiprocessing.managers
import multiprocessing
import multiprocessing
import queue
import lxml,lxml.etree
import random
import urllib,urllib.request
import time,gevent,gevent.pool
import threading
import selenium.webdriver
import selenium


class Quemanager(multiprocessing.managers.BaseManager):
    pass


def getpagedata(url):
    try:
        header = [{"User-Agent": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"},
                  {"User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)"},
                  {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"},
                  {"User-Agent": "Opera/9.80(WindowsNT6.1;U;en)Presto/2.8.131Version/11.11"},
                  {"User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)"}]
        # random.randint(0,4)  包含0和4
        respon = urllib.request.Request(url,headers=header[random.randint(0,4)])
        pagespurce = urllib.request.urlopen(respon,timeout=8)
        time.sleep(5)
        if pagespurce.code!=200:
            print('---网页开启错误----',pagespurce.code)
            return -1
        else:
            return pagespurce.read().decode('utf-8', 'ignore')
    except Exception as e:
        print('-- Error - url->--%s --- %s '%(e,url))
        return -1



def mvthread(purl,sem,result):
    global errthread
    with sem:
        source = getpagedata(purl)
        if type(source)==str:
            mytree = lxml.etree.HTML(source)
            # 网页存在两种状态
            list = mytree.xpath('//ul[@class=\"panel\"]//li[@class=\"yk-col4 mr1\"]')
            if len(list)<=5:
                list = mytree.xpath('//div[@class=\"yk-row\"]//div[@class=\"yk-col4 \"]')
            kind = mytree.xpath('//div[@class=\"item noborder\"]/ul/li[@class=\"current\"]/span/text()')
            if len(kind)<=5:
                kind = mytree.xpath('//div[@class=\"item border\"]/ul/li[@class=\"current\"]/span/text()')
            print('---kind.type--->>>--%s'%kind)
            # 使用协程池控制协程开启数量
            pool= gevent.pool.Pool(15)
            urlist = []
            for li in list:
                cover = li.xpath('.//div[@class=\"p-thumb\"]/img/@src')[0]
                num = li.xpath('.//ul[@class=\"p-info pos-bottom\"]//span[@class=\"p-time \"]/span/text()')
                if len(num)==0:
                    num = li.xpath('.//ul[@class=\"p-info pos-bottom\"]//span[@class=\"p-time hover-hide\"]/span/text()')[0]
                else:
                    num = num[0]
                title = li.xpath('.//ul[@class=\"info-list\"]/li[@class=\"title\"]/a/text()')[0]
                link = 'http:' + li.xpath('.//ul[@class=\"info-list\"]/li[@class=\"title\"]/a/@href')[0]
                aclist = li.xpath('.//ul[@class=\"info-list\"]/li[@class=\"actor\"]/a/text()')
                if len(aclist)==0:
                    aclist = li.xpath('.//ul[@class=\"info-list\"]/li[@class=\"actor\"]/text()')
                actor = li.xpath('.//ul[@class=\"info-list\"]/li[@class=\"actor\"]/em/text()')
                if len(actor)!=0:
                    actor = actor[0]
                else:
                    actor = 'None'
                for i in range(len(aclist)):
                    if i !=len(aclist)-1:
                        actor += aclist[i]
                        actor += '、'
                    else:
                        actor += aclist[i]
                doc = [kind[0], title,cover, actor, num , link,'']
                urlist.append((link,doc,result))
            print('------>>>--解析-->>-----',urlist)
            # 协程池
            pool.map(getdetail,urlist)
        else:
            errthread.append(purl,sem,result)

def pageinfor(url,doce):
    page = getpagedata(url)
    if type(page)==str:
        tvtree = lxml.etree.HTML(page)
        show = tvtree.xpath('//div[@id=\"module_basic_title\"]/div[@class=\"base_info\"]')[0]
        # gr = show.xpath('//span[@id=\"videoTotalPV\"]/em/text()')[0]
        kd = show.xpath('./h1/a/text()')[0]
        td = show.xpath('./h1//span')
        des =  kd
        if len(td)!=0:
            for li in td:
                if len(li.xpath('./text()'))!=0:
                    des += li.xpath('./text()')[0]
                    des += ' '
        info=doce[1]
        # info.append(des)   会一直叠加
        info[6]=des
        info[5]=url
        result = doce[2]
        result.put(info)
        print('----<<--已发往服务器---<<-----%s' % info)


def getdetail(doc):
    global errorurl
    infor = doc[1]
    source = getpagedata(doc[0])
    if type(source) == str:
        mytree = lxml.etree.HTML(source)
        # 因为每一个栏目里面的页面够着不一样因此要分成 26 类来单独判断
        # 由于视频存储空间不够 固获取视频连接 和播放视频是的一些信息 作为判断是否成功获取页面
        if doc[1][0] == '剧集':
            tvlist = mytree.xpath('//div[@class=\"items clearfix\"]//div[@name=\"tvlist\"]/a[@class=\"sn\"]/@href')
            for tv in tvlist:
                url = 'http:'+tv
                pageinfor(url,doc)

        elif doc[1][0] in ['电影','资讯','广告','游戏','自拍','创意视频','搞笑','生活','汽车','科技','时尚','旅游','微电影','网剧','拍客']:
            show = mytree.xpath('//div[@id=\"module_basic_title\"]/div[@class=\"base_info\"]')[0]
            # gr = show.xpath('.//span[@id=\"videoTotalPV\"]/em/text()')[0]  # Js数据
            kd = show.xpath('./h1/a/text()')
            td = show.xpath('./h1//span')
            des =  kd
            for li in td:
                des += li.xpath('./text()')[0]
                des += ' '
            infor = doc[1]
            infor[6] = des
            # infor.append(des)
            result = doc[2]
            result.put(infor)
            print('----<<--已发往服务器---<<-----%s' % infor)

        elif doc[1][0] in['综艺','音乐','娱乐']:
            try:
                showlist = mytree.xpath('//div[@id=\"Dramalist_wrap\"]//div[@class=\"showlists\"]//[@class=\"item\"]//a[@class=\"A\"]/@href')
                for show in showlist:
                    show = 'http:'+show
                    pageinfor(show, doc)
            except:pass

        elif doc[1][0] in ['动漫','教育','少儿','纪实','体育']:
            aclist = mytree.xpath('//div[@id=\"Dramalist_wrap\"]//div[@class=\"items\"]//li/a[@class=\"A\"]/@href')
            for ac in aclist:
                ac = 'http:'+ ac
                pageinfor(ac, doc)

    else:
        # 页面获取失败是 把链接放入一个列表重新打开
        print('++++++++-------+++++++',doc[0])
        errorurl.append(doc)


def gettask(sem, result):
    while True:
        try:
            if not task.empty():
                purl = task.get(timeout=60)
                threading.Thread(target=mvthread,args=(purl,sem,result)).start()
                # 阻塞线程 完成5条任务时 才开始下5条任务
                print('--->>---收到任务-----',purl)
                time.sleep(120)
            else:
                time.sleep(2)
        except:
            break

def redetail(errorurl):
    while True:
        if len(errorurl)!=0:
            print('>>>>>>>> Error url ++++',len(errorurl))
            doc = errorurl.pop(0)
            errt = threading.Thread(target=getdetail, args=(doc,))
            errt.start()
            errt.join()
        else:
            time.sleep(20)


if __name__ == '__main__':
    errorurl = []
    errthread = []
    Quemanager.register('get_task')
    Quemanager.register('get_result')
    manager = Quemanager(address=('10.36.132.54',6558), authkey=123456)
    manager.connect()
    task,result=manager.get_task(),manager.get_result()
    # 电脑性能原因（8G内存不够） 只能并发6条
    sem = threading.Semaphore(6)
    # 由于下方有while阻塞主线程，就不必阻塞线程
    threading.Thread(target=gettask, args=(sem, result)).start()
    # 处理打开错误的 url
    threading.Thread(target=redetail,args=(errorurl,)).start()
    while True:
        print('-------- Re url -------%s'%len(errthread))
        if len(errthread)!=0:
            purl = errthread.pop(0)
            tr=threading.Thread(target=mvthread, args=(purl, sem, result))
            tr.start()
            tr.join()
        else:
            time.sleep(20)
