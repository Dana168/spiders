import  scrapy
from  scrapy import cmdline

#cmdline.execute(["scrapy","crawl","ctospider","-o","51cto.json"])

cmdline.execute(["scrapy","crawl","baidubaike","-o","3.json"])
# cmdline.execute(["scrapy","crawl","baidubaike"])