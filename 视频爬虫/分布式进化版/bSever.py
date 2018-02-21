# coding:utf-8
import multiprocessing  # �ֲ�ʽ����
import multiprocessing.managers  # �ֲ�ʽ���̹�����
import time  # �������ʱ��
import queue  # ����
import threading
import pymysql as pymysql

task_queue = queue.Queue()  # ����
result_queue = queue.Queue()  # ���mail
url_queue = queue.Queue()  # ���url


def return_task():  # �����������
    return task_queue


def return_result():  # ���ؽ������
    return result_queue


class QueueManger(multiprocessing.managers.BaseManager):  # �̳У����̹���������
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
            print('���ⱻ��%s��ID��%s�����ͣ�%s,�ۿ�����%s����Ļ����%s' % (title, aid, tname, view1, danmaku))
            # ��ȡ��ѯsql�α�
            cursor.execute(
                "insert into bilibili3(title,aid,tname,view1,danmaku) values('%s','%s','%s','%s',%s)" % (
                str(title), str(aid), str(tname), str(view1), str(danmaku)))
            # �ύ
            conn.commit()
    conn.close()


if __name__ == "__main__":
    multiprocessing.freeze_support()  # �����ֲ�ʽ֧��
    QueueManger.register("get_task", callable=return_task)  # ע�ắ�����ͻ��˵���
    QueueManger.register("get_result", callable=return_result)
    manger = QueueManger(address=("192.168.0.107", 8888), authkey="123456".encode('utf-8'))  # ����һ�������������õ�ַ������
    manger.start()  # ����
    task, result = manger.get_task(), manger.get_result()  # ���񣬽��
    # �������ݿ�
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='314251612', db='b_station', charset='utf8')
    cursor = conn.cursor()
    cursor.execute(
        "create table bilibili3(id INT PRIMARY KEY AUTO_INCREMENT,title varchar(100),aid int (20),tname varchar(50),view1 int (20),danmaku int (20))")
    for i in range(1000000):
        url = "https://comment.bilibili.com/recommendnew,{}".format(i)  # ƴ����ַ
        print("task add data", url)
        task.put(url)
        print("waitting for------")
        threading.Thread(target=getmailfromclient, args=(result,)).start()  # �������յ��߳�
        time.sleep(1)

    manger.shutdown()  # �رշ�����
