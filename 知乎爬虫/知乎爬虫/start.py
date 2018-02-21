from scrapy import cmdline
from selenium import webdriver

cmdline.execute(['scrapy','crawl','zhihuspider'])
# cmdline.execute(['scrapy','crawl','zhihuspider','-o','cto.xml'])
# cmdline.execute(['scrapy','crawl','zhihuspider','-o','51cto.json'])
webdriver.Chrome().switch_to.active_element({'class':'qrcode-signin-cut-button'})


