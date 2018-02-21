# coding:utf-8
import smtplib
import ssl
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests
import time
import os
import send_email as Send_mail

# 实现获取和实时刷新火车票信息，并集成有无票提示功能



def get_bill(url, chinese_list, letter_list, mytrain, mysite):
    # 传递票的url 站点、站点代号、需要的车次和座位——参数
    while True:
        ip = 1
        ip = time_ip(ip)
        # 冒充浏览器，反反爬虫第一式
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0'
        headers = {"User-Agent": user_agent}

        # 把网站证书认证关闭
        req = requests.get(url, headers=headers, verify=False).text
        # 读取Json火车票信息
        dict = json.loads(req)
        result = dict['data']['result']
        list1 = []
        list2 = []
        # 接下来就是清洗数据环节

        # 用 | 分隔开信息并加入列表
        for bill in result:
            list1.append(bill.split("|"))
        # 然后通过分析得出，开头为空的是停运的火车，直接干掉，然后加入LIST2
        for i in list1:
            if i[0] != "":
                list2.append(i)
        # 遍历LIST2 把有用的数据提出来并加上备注，看上去不反人类
        for i in list2:
            train = "列车："
            start = "出发站："
            end = "到达站:"
            time_start = "出发时间:"
            time_end = "到达时间:"
            time_train = "历时:"

            train += i[3]
            # 反反爬虫第二式
            # 这里呢调用了 code_change_chinese 函数 ，源码里是用代号来表示站点的需要换回汉字，12306贼恶心，破解它想了2小时
            start += code_change_chinese(chinese_list, letter_list, i[6])
            end += code_change_chinese(chinese_list, letter_list, i[7])
            time_start += i[8]
            time_end += i[9]
            time_train += i[10]

            # 到这里这里为止（第一波），能轻松加愉快的提取出以上数据，下边的数据就要和12306斗志都用了

            staterroom = "商务座："
            one_room = "一等座："
            two_room = "二等座："
            high_grade_room = "高级软座："
            soft_room = "软卧："
            move_room = "动卧："
            hard_room = "硬卧："
            hard_seat = "硬座："
            no_room = "无座："

            message = ""
            # 反反爬虫第三式
            '''
            这个折磨了我一个晚上没睡好，上面的数据提取没压力，但是座位的数据就恶心了，
            提取的数据找不到规律，看了好久好久，查看了很多趟火车每一趟后面的代码不一样，查看网页页面也对不上号
            但是不能放弃呀，一直核对找规律，终于再看了不下20趟火车的情况下浪费一早上时间，有结果了：
            首先他用了无关紧要的数据随机放在每一趟火车数据中间
            然后他把座位和在网页的方向相反
            致命的一招，每一趟火车座位的数据提取位置不一样，好在他就有几种模式，全部不一样那就没辙了，分别有
            "OM9" "OF""1413""OMP"，目前发现这4种，一一把他搞定，终于看到希望了

          '''

            if i[len(i) - 1] == "OM9":
                staterroom += i[len(i) - 4]
                one_room += i[len(i) - 5]
                two_room += i[len(i) - 6]
                high_grade_room += i[len(i) - 7]
                soft_room += i[len(i) - 8]
                move_room += i[len(i) - 9]
                hard_room += i[len(i) - 10]
                hard_seat += i[len(i) - 11]
                no_room += i[len(i) - 12]
            if i[len(i) - 1] == "OF":
                staterroom += i[len(i) - 3]
                one_room += i[len(i) - 4]
                two_room += i[len(i) - 5]
                high_grade_room += i[len(i) - 6]
                soft_room += i[len(i) - 7]
                move_room += i[len(i) - 8]
                hard_room += i[len(i) - 9]
                hard_seat += i[len(i) - 10]
                no_room += i[len(i) - 11]
            if i[len(i) - 1] == 1413:
                staterroom += i[len(i) - 7]
                one_room += i[len(i) - 8]
                two_room += i[len(i) - 9]
                high_grade_room += i[len(i) - 10]
                soft_room += i[len(i) - 11]
                move_room += i[len(i) - 12]
                hard_room += i[len(i) - 13]
                hard_seat += i[len(i) - 14]
                no_room += i[len(i) - 15]
            if i[len(i) - 1] == "1413":
                staterroom += i[len(i) - 7]
                one_room += i[len(i) - 8]
                two_room += i[len(i) - 9]
                high_grade_room += i[len(i) - 10]
                soft_room += i[len(i) - 11]
                move_room += i[len(i) - 12]
                hard_room += i[len(i) - 13]
                hard_seat += i[len(i) - 14]
                no_room += i[len(i) - 15]
            if i[len(i) - 1] == "OMP":
                staterroom += i[len(i) - 5]
                one_room += i[len(i) - 6]
                two_room += i[len(i) - 7]
                high_grade_room += i[len(i) - 8]
                soft_room += i[len(i) - 9]
                move_room += i[len(i) - 10]
                hard_room += i[len(i) - 11]
                hard_seat += i[len(i) - 12]
                no_room += i[len(i) - 13]

                # 这里是有无票的提示功能，办法比较笨，勿喷 ，若有就返回False停止死循环
            if train == mytrain:
                if (staterroom.split("：")[0] + "：") == mysite and staterroom != mysite:
                    print(train + " " + staterroom + "===================赶紧下单")
                    sendMail()
                    return False

                elif (one_room.split("：")[0] + "：") == mysite and one_room != mysite:
                    print(train + " " + one_room + "===================赶紧下单")
                    sendMail()
                    return False
                elif (two_room.split("：")[0] + "：") == mysite and two_room != mysite:
                    print(train + " " + two_room + "===================赶紧下单")
                    sendMail()
                    return False
                elif (high_grade_room.split("：")[0] + "：") == mysite and high_grade_room != mysite:
                    print(train + " " + high_grade_room + "===================赶紧下单")
                    sendMail()
                    return False
                elif (soft_room.split("：")[0] + "：") == mysite and soft_room != mysite:
                    print(train + " " + soft_room + "===================赶紧下单")
                    sendMail()
                    return False
                elif (move_room.split("：")[0] + "：") == mysite and move_room != mysite:
                    print(train + " " + move_room + "===================赶紧下单")
                    sendMail()
                    return False
                elif (hard_room.split("：")[0] + "：") == mysite and hard_room != mysite:
                    print(train + " " + hard_room + "===================赶紧下单")
                    sendMail()
                    return False
                elif (hard_seat.split("：")[0] + "：") == mysite and hard_seat != mysite:
                    print(train + " " + hard_seat + "===================赶紧下单")
                    sendMail()
                    return False
                elif (no_room.split("：")[0] + "：") == mysite and no_room != mysite:
                    print(train + " " + no_room + "===================赶紧下单")
                    sendMail()
                    return False
                else:
                    print("================你要的票还没有，等朕消息，或者看看其他的呗=================")
            # 打印查询的所有不营运的火车消息
            message += train + "  " + start + "  " + end + "  " + time_start + "  " + time_end + "  " + time_train + "  " + staterroom + "  " + one_room + "  " + two_room + "  " + high_grade_room + "  " + soft_room + "  " + move_room + "  " + hard_room + "  " + hard_seat + "  " + no_room
            print(message)
        time_ip(ip)
        time.sleep(10)


def get_load():
    # 获取站点 和代号的函数，自己看 贼简单
    chinese = open("站点.txt", "rb")
    chinese_list = chinese.read().decode("utf-8", "ignore").split("\r\n")
    chinese.close()

    letter = open("站点代号.txt", "rb")
    letter_list = letter.read().decode("utf-8", "ignore").split("\r\n")
    letter.close()

    return chinese_list, letter_list


# https:/ /kyfw.12306.cn/otn/station_version=1.9044

# 这个能是换汉字的，自己看
def code_change_chinese(chinese_list, letter_list, code):
    for i in range(len(letter_list)):
        if letter_list[i] == code:
            return chinese_list[i]

#动态换ip的功能
def time_ip(ip):
    adslname = "宽带连接"
    username = "051916354748"
    password = "320481"
    if ip == 1:
        os.system("rasdial %s %s %s" % (adslname, username, password))
        ip = 2
        return ip
    elif ip == 2:
        os.system("rasdial %s /disconnect" % adslname)
        ip = 1
        return ip

#发邮件的功能
def sendMail():
    way = "QQ"
    # 收发人
    sender = '2962085938@qq.com'
    password = 'qygwpncvbqgqdcdg'
    receivers = ["1021321421@qq.com"]
    # 创建一个带附件的实例
    message = MIMEMultipart()
    message['Subject'] ='12306后门'
    message['From'] = sender
    message['To'] = ";".join(receivers)
    msgText = '兄弟有票啦，赶紧下单'
#-------------------------------------------
    # 邮件正文内容
    message.attach(MIMEText(msgText, 'plain', 'utf-8'))
    try:

        if way=="QQ":
            # 登录邮件服务器
            smtpObj = smtplib.SMTP_SSL()
            smtpObj.connect('smtp.qq.com', 465)
            smtpObj.login(sender, password)
            # 发送并退出
            smtpObj.sendmail(sender, receivers, message.as_string())
            smtpObj.quit()
            print("邮件发送成功")
        if way=="网易":
            # 登录163邮件服务器
            smtpObj = smtplib.SMTP('smtp.163.com', 25)
            smtpObj.login(sender, password)
            # 发送并退出
            smtpObj.sendmail(sender, receivers, message.as_string())
            smtpObj.quit()
            print("邮件发送成功")


    # 处理异常
    except smtplib.SMTPException as e:
        print("Error: 无法发送邮件", e)

if __name__ == '__main__':
    chinese_list, letter_list = get_load()
    start = "南昌"
    end = "深圳"
    start_code = ""
    end_code = ""
    # print(letter_list)
    # 这个是把输入进来的汉字转成代号，加入到URL实现查询全国火车站点
    for i in range(len(chinese_list)):
        if chinese_list[i] == start:
            start_code += letter_list[i]
            print(start_code)
        if chinese_list[i] == end:
            end_code += letter_list[i]
            print(end_code)

    mytrain = "列车：Z185"
    mysite = "一等座："
    url = "https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=2017-12-14&leftTicketDTO.from_station=" + start_code + "&leftTicketDTO.to_station=" + end_code + "&purpose_codes=ADULT"

    get_bill(url, chinese_list, letter_list, mytrain, mysite)

    """"
    在1.0的基础上加入了一个动态换ip的功能——反反爬虫之止防ip
    在2.0的基础上加入了邮箱通知
    """
    pass
