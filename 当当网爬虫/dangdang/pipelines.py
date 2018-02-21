# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class DangdangPipeline(object):
    def process_item(self, item, spider):
        conn = pymysql.connect(host='localhost', user='root', password="Admin123456", port=3306, database='dd',
                               charset='utf8')
        cursor = conn.cursor()
        for i in  range(0,len(item['title'])):
            title = item['title'][i]
            link = item['link'][i]
            comment = item['comment'][i]
            print(title)

            sql = "insert into goods(title,link,comment) values('" + title + "','" + link + "','" + comment + "')"
            conn.query(sql)
            # cursor.execute(sql)
            # sql = "insert into goods(title,link,comment) VALUES  ('"+title+"', '"+ link+ "', '"+comment+"')"
            conn.commit()
        # 关闭数据库
        conn.close()
        return item
