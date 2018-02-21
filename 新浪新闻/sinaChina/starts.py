import  scrapy
from  scrapy import cmdline
#pycharm执行风格
cmdline.execute(["scrapy","crawl","sinaChinaSpider"])

#cmdline.execute(["scrapy","crawl","ctospider"])
#正统方法
#cookie。每链接一次，TCP 断开,再链接不行。
#selenium登陆，保持会话，