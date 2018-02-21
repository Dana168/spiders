# coding:utf-8
import multiprocessing  # 分布式进程
import multiprocessing.managers  # 分布式进程管理器
import time  # 随机数，时间
import queue  # 队列
import threading
import pymysql as pymysql

task_queue = queue.Queue()  # 任务
result_queue = queue.Queue()  # 结果mail
url_queue = queue.Queue()  # 结果url


def return_task():  # 返回任务队列
    return task_queue


def return_result():  # 返回结果队列
    return result_queue


class QueueManger(multiprocessing.managers.BaseManager):  # 继承，进程管理共享数据
    pass


def getmailfromclient(result):
    while True:
        time.sleep(5)
        res = result.get(timeout=100)
        print("get data", res)
        for b in range(len(res)):
            title = res[b][0]
            aid = res[b][1]
            tname = res[b][2]
            view1 = res[b][3]
            danmaku = res[b][4]
            print('标题被：%s，ID：%s，类型：%s,观看量：%s，弹幕量：%s' % (title, aid, tname, view1, danmaku))
            # 获取查询sql游标
            cursor.execute(
                "insert into bilibili3(title,aid,tname,view1,danmaku) values('%s','%s','%s','%s',%s)" % (
                str(title), str(aid), str(tname), str(view1), str(danmaku)))
            # 提交
            conn.commit()
    conn.close()


if __name__ == "__main__":
    multiprocessing.freeze_support()  # 开启分布式支持
    QueueManger.register("get_task", callable=return_task)  # 注册函数给客户端调用
    QueueManger.register("get_result", callable=return_result)
    manger = QueueManger(address=("192.168.0.107", 8888), authkey="123456".encode('utf-8'))  # 创建一个管理器，设置地址与密码
    manger.start()  # 开启
    task, result = manger.get_task(), manger.get_result()  # 任务，结果
    # 创建数据库
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='314251612', db='b_station', charset='utf8')
    cursor = conn.cursor()
    cursor.execute(
        "create table bilibili3(id INT PRIMARY KEY AUTO_INCREMENT,title varchar(100),aid int (20),tname varchar(50),view1 int (20),danmaku int (20))")
    for i in range(1000000):
        url = "https://comment.bilibili.com/recommendnew,{}".format(i)  # 拼接网址
        print("task add data", url)
        task.put(url)
        print("waitting for------")
        threading.Thread(target=getmailfromclient, args=(result,)).start()  # 开启接收的线程
        time.sleep(1)

    manger.shutdown()  # 关闭服务器
