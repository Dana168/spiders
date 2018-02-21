import requests
import urllib.parse
import random
import time
import sys
import re
import urllib3
import getpass # 密文输入

req = requests.session()
urllib3.disable_warnings()
# 登陆-------------------------
apptklist = []
newStrList = []
def signin():
 ran = random.uniform(1, 0)
 imgUrl = ('https://kyfw.12306.cn/passport/captcha/captcha-image?'
    'login_site=E&module=login&rand=sjrand&%s' % ran)
 print(imgUrl)
 imgresponse = req.get(url=imgUrl, verify=False)
 codeimg = imgresponse.content
 fn = open('code.png', 'wb')
 fn.write(codeimg)
 fn.close()
 codeStr = input('请输入验证码的坐标:')
 a = ''
 b = ''
 c = ''
 d = ''
 e = ''
 f = ''
 g = ''
 h = ''
 if '1' in codeStr:
  a = '37,37,'
 if '2' in codeStr:
  b = '100,37,'
 if '3' in codeStr:
  c = '180,37,'
 if '4' in codeStr:
  d = '250,37,'
 if '5' in codeStr:
  e = '37,100,'
 if '6' in codeStr:
  f = '100,100,'
 if '7' in codeStr:
  g = '180,100,'
 if '8' in codeStr:
  h = '250,100,'
 newCodeStr = a+b+c+d+e+f+g+h
 newStr = newCodeStr[:-1]
 newStrList.append(newStr)
 url = 'https://kyfw.12306.cn/passport/captcha/captcha-check'
 data = {
  'answer':newStr,
  'login_site':'E',
  'rand':'sjrand'
 }
 headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
      ' Chrome/63.0.3239.108 Safari/537.36',
 }
 response = req.post(url=url, data=data, headers=headers, verify=False)
 print('检测图片-----------', url)
 print(response.text)
 result = response.json()
 if result['result_code'] == '4':
  print('验证码校验成功')
 else:
  print('验证码校验失败,请注意填写正确的坐标')
  signin()
  return
 userName = input('Please input your userName:')
 # password = input('Please input your password:')
 password = getpass.getpass('Please input your password:')
 loginData = {
  'username':userName,
  'password':password,
  'appid':'otn'
 }
 headers = {
  'Host':'kyfw.12306.cn',
  'Referer':'https://kyfw.12306.cn/otn/login/init',
  'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2)'
      ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 '
      'Safari/537.36'
 }
 response = req.post('https://kyfw.12306.cn/passport/web/login', data=loginData, headers=headers, verify=False)
 print('--------------登陆中--------------------')
 print('https://kyfw.12306.cn/passport/web/login')
 print('response', response.text.encode('utf-8').decode('utf-8'))
 fd = open("locate.html", 'wb+')
 fd.write(response.content)
 yzData = {
  'appid':'otn'
 }
 response = req.post('https://kyfw.12306.cn/passport/web/auth/uamtk', data=yzData, headers=headers, verify=False)
 print('---------------------第一次验证---------------------')
 print(response.text)
 # print('typeof response',type(response))
 loginMessage = response.json()['newapptk']
 print('loginMessage=', loginMessage)
 # 第二次验证开始++++++++++++++++++++++++++++++
 yz2Data = {
  'tk': loginMessage
 }
 response = req.post('https://kyfw.12306.cn/otn/uamauthclient', data=yz2Data, headers=headers,verify=False)
 print('---------------------第二次验证---------------------')
 print(response.text)
 apptk = response.json()['apptk']
 apptklist.append(apptk)
def buy():
 print(newStrList)
 req.headers['Referer'] = 'https://kyfw.12306.cn/otn/leftTicket/init'
 result = req.post('https://kyfw.12306.cn/otn/login/checkUser')
 print('----------------购票系统--------------')
 print(result.text)
 print('验证登录状态成功checkUser')
 headers = {
  'Referer':'https://kyfw.12306.cn/otn/leftTicket/init',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36'
      ' (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
 }
 data = {
  # 'secretStr':reserve[1],
  'train_date':'2018-01-17',
  'back_train_date':'2018-01-17',
  'tour_flag':'dc', # dc 单程
  'purpose_codes':'ADULT', # adult 成人票
  'query_from_station_name':'成都',
  'query_to_station_name':'长沙',
  'undefined':''
 }
def ticket():
 # 先登陆、然后查询车票信息
 signin()
 url = ('https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date=2018-02-10&'
   'leftTicketDTO.from_station=SZQ&leftTicketDTO.to_station=NFG&purpose_codes=ADULT')
 try:
  response = requests.get(url, verify=False)
  result = response.json()
  print(result)
  return result['data']['result']
 except Exception as e:
  return None
if __name__ == "__main__":
 # ticket()
 # with open('./aaa.xlsx', encoding='utf-8') as f:
 #
 #  print(f.read())
 dic = {}
 context = [('IDS_ABOUT_OFFICAL_PHONE', 'Službeni telefon'),
    ('IDS_ABOUT_OFFICAL_WEBSITE', 'Službeno web-mjesto'),
    ('IDS_ABOUT_OFFICIAL_PHONE_CALL_NOT_SUPPORT', 'Trenutni uređaj ne može pozivati.')]
 for i in range(len(context)):
  print(i)
  dic.setdefault(context[i][0],context[i][1])
 print(dic)
 print(dic.keys())