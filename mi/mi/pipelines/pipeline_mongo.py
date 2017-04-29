# -*- coding: utf-8 -*-
import pymongo
from mi.items import ArticleItem
from mi.items import DomTreeItem
import mi.settings as settings

class MongoPipeline(object):
    # 集合名 使用之前会赋值
    hp_collection_name = ''

    # 初始化该数据库
    def __init__(self, mongo_host, mongo_port, mongo_db):
        self.mongo_host = mongo_host
        self.mongo_port = mongo_port
        self.mongo_db = mongo_db

    @classmethod  # 指定该方法为类方法
    def from_crawler(cls, crawler):
        return cls(
            mongo_host = crawler.settings.get('MONGO_HOST', 'items'),
            mongo_port = crawler.settings.get('MONGO_PORT', 'items'),
            mongo_db = crawler.settings.get('MONGO_DATABASE', 'items'),
        )

    # 数据库连接
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_host, self.mongo_port)
        self.db = self.client[self.mongo_db]

    # 数据库关闭
    def close_spider(self, spider):
        self.client.close()

    # 将数据存入到数据库中
    def process_item(self, item, spider):
        print "catch a item"
        print type(item)
        if isinstance(item, ArticleItem):
            self.hp_collection_name = settings.MONGO_COLLECTION_NAME
            self.db[self.hp_collection_name + '_' + 'ArticleItem'].insert(dict(item))  # 存入数据库原始数据
        if isinstance(item, DomTreeItem):
            self.hp_collection_name = settings.MONGO_COLLECTION_NAME
            self.db[self.hp_collection_name + '_' + "DomTreeItem"].insert(dict(item))  # 存入数据库原始数据
        return item