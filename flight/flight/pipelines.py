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
