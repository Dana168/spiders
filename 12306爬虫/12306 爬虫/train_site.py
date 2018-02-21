import re

import requests

def  get_site(url):
    user_agent='Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0'
    headers={"User-Agent":user_agent}
    req=requests.get(url,headers=headers,verify=False).text
    list1=req.split("|")
    patarn_chinese=re.compile("[\u4e00-\u9fa5]+")
    patarn_letter=re.compile("[A-Z]+")
    file_chinese=open("站点.txt","wb")
    file_letter=open("站点代号.txt","wb")
    for i in list1:
        if len(patarn_chinese.findall(i))>0:
            chinese=patarn_chinese.findall(i)[0] + "\r\n"
            file_chinese.write(chinese.encode("utf-8","ignore"))
            file_chinese.flush()
            print(patarn_chinese.findall(i)[0])
        elif len(patarn_letter.findall(i))>0:
            letter=patarn_letter.findall(i)[0] + "\r\n"
            file_letter.write(letter.encode("utf-8", "ignore"))
            file_letter.flush()
            print(patarn_letter.findall(i)[0])
    file_letter.close()
    file_chinese.close()
if __name__ == '__main__':
    url="https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9044:21"
    get_site(url)