# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb
import MySQLdb.cursors
from scrapy.exporters import CsvItemExporter
from twisted.enterprise import adbapi

class YjsPipeline(object):
    def __init__(self,dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls,settings):
        dbparms = dict(
            host = settings['MYSQL_HOST'],
            user = settings['MYsql_USER'],
            password = settings['MYSQL_PASSWORD'],
            db = settings['MYSQL_DBNAME'],
            charset = 'utf8',
            cursorclass = MySQLdb.cursors.DictCursor,
            use_unicode = True
        )
        dbpool = adbapi.ConnectionPool("MySQLdb",**dbparms)

        return cls(dbpool)

    def process_item(self,item,spider):
        # 异步插入
        query = self.dbpool.runInteraction(self.do_insert,item)
        # 处理异常
        query.addErrback(self.handle_error)

    def handle_error(self,failure,item,spider):
        print(failure)

    def do_insert(self,cursor,item):
        insert_sql = """
            insert into table(cols1,cols2)
            VALUES (%s,%s)
        """
        cursor.execute(insert_sql,(item[''],item['']))

