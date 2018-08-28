# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import JsonLinesItemExporter
import pymongo

class DyttPipeline(object):
    def __init__(self):
        self.fp = open("dytt.json","wb")
        self.exporter = JsonLinesItemExporter(self.fp,ensure_ascii=False,encoding='utf-8')
    def open_spider(self,spider):
        print('开始写入。。。')
    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def close_spider(self,spider):
        print('写入完成！')

class DyttmongoPipeline(object):
    def __init__(self):
        self.client = pymongo.MongoClient("127.0.0.1",port=27017)
        self.db = self.client.dytt
        self.collection = self.db.info

    def open_spider(self,spider):
        print("开始保存到mongodb...")

    def process_item(self,item,spider):
        # 不能直接将item对象数据保存到mongodb,先转化为字典。
        self.collection.insert_one(dict(item))

    def close_spider(self,spider):
        print("保存完成！")