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
            user = settings['MYSQL_USER'],
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
        query.addErrback(self.handle_error, item, spider)

    def handle_error(self,failure,item,spider):
        print(failure)
        import codecs
        fw = codecs.open('errLog.txt', 'a', 'utf-8')
        fw.write("网站地址：" + item['url'] + "\r\n" + str(failure))
        fw.close()

    def KeyJudge(self, item_dict, value):
        if value in item_dict.keys():
            return item_dict[value]
        else:
            return None

    def do_insert(self,cursor,item):

        # 判断是哪种类型 1,本站 0 其他网站
        if item['type'] == 0:
            # 如果连公司名都获取不到，那就是直接跳转到官网去了
            if self.KeyJudge(item, "company"):
                location = self.KeyJudge(item, 'location')
                major_label = self.KeyJudge(item, 'major_label')
                position_title = self.KeyJudge(item, 'position_title')

                insert_sql = """
                    insert into yjs_other(
                    url,
                    url_md5,
                    title,
                    tag,
                    company,
                    post_date,
                    location,
                    position_title,
                    position_type,
                    source,
                    major_label,
                    content,
                    created_at)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """
                cursor.execute(insert_sql, (
                    item['url'],
                    item['url_md5'],
                    item['title'],
                    item['tag'],
                    item['company'],
                    item['post_date'],
                    location,
                    position_title,
                    item['position_type'],
                    item['source'],
                    major_label,
                    item['content'],
                    item['created_at']
                ))
        else:

            recruit_num = self.KeyJudge(item, 'recruit_num')

            insert_sql = """
                insert into yjs_self(
                url,
                url_md5,
                title,
                tag,
                company,
                industry,
                company_size,
                company_type,
                position_title,
                location,
                recruit_num,
                position_type,
                position_desc,
                company_intro,
                company_site,
                created_at,
                valid_date)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """
            cursor.execute(insert_sql, (
                item['url'],
                item['url_md5'],
                item['title'],
                item['tag'],
                item['company'],
                item['industry'],
                item['company_size'],
                item['company_type'],
                item['position_title'],
                item['location'],
                recruit_num,
                item['position_type'],
                item['position_desc'],
                item['company_intro'],
                item['company_site'],
                item['created_at'],
                item['valid_date']
            ))


