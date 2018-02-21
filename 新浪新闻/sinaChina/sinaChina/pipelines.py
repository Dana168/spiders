# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class SinachinaPipeline(object):
    def process_item(self, item, spider):
        #保存文件，开国上将旧居被拆续:哈尔滨双城区长等11人受处.txt


        filepathdir=r"C:\Users\Tsinghua-yincheng\Desktop\SZday29\sinaChina\sinaChina\spiders\data"
        filepathdir += "\\"
        filepathdir+=item["level1"]
        filepathdir += "\\"
        filepathdir += item["level2"]
        filepathdir += "\\"
        filepathdir += item["level3"]




        filename=filepathdir+"\\"+item["title"]+".txt"
        savefile=open(filename,"wb")
        savefile.write(item["content"].encode("utf-8","ignore"))
        savefile.close()
        return item
