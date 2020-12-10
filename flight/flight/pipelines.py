# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter


class FlightPipeline:
    def process_item(self, item, spider):
        return item


import json


class CtripPipeline:
    def __init__(self, path):
        self.info = json.loads(path)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(path=crawler.settings.get('REQUIRED_INFO'))

    def open_spider(self, spider):
        spider.get_info(self.info)


import pymysql
from twisted.enterprise import adbapi


class MysqlPipeline:
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparams = dict(
                host=settings['MYSQL_HOST'],
                db=settings['MYSQL_DBNAME'],
                user=settings['MYSQL_USER'],
                passwd=settings['MYSQL_PASSWD'],
                cursorclass=pymysql.cursors.DictCursor,
        )
        dbpool = adbapi.ConnectionPool('pymysql', **dbparams)
        return cls(dbpool)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.insert, item)
        query.addErrback(self.handle_error, spider)

    @staticmethod
    def insert(cursor, item):
        # TODO(Tomspiano): complete me
        insert_sql = 'insert into xxx(yyy, zzz) values (%s, %s)'
        cursor.execute(insert_sql, (item['']))

    def handle_error(self, spider, failure):
        # TODO(Tomspiano): check
        spider.logger.error(f'{failure}')
