# -*- coding: utf-8 -*-
"""
Created on 2020/11/19
@Author: 你们说的队
@Project: AIRA
@Product: PyCharm
@Description: 航班时刻表
"""
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
# from flight.items import ScheduleItem
import json
from modules import dictionary as dic


class SchedulesSpider(scrapy.Spider):
    name = 'schedules'
    custom_settings = {'LOG_FILE': 'schedules_log.txt'}

    def start_requests(self):
        # cityName = '甘孜'
        # cityAbbr = 'gzg'
        for cityName, cityAbbr in dic.city.items():
            url = f'https://flights.ctrip.com/schedule/{cityAbbr}..html'
            yield scrapy.Request(url=url, callback=self.parse, cb_kwargs={'dcityName': cityName, 'dcityAbbr': cityAbbr})

    def parse(self, response, **kwargs):
        dcityName = kwargs['dcityName']
        # dcity = kwargs['dcityAbbr']
        acitysNames = response.css('div.m a::text').re(r'-(\w+)')

        if len(acitysNames) == 0:
            self.logger.info(f'无从{dcityName}出发的国内航班')
            return

        # item = ScheduleItem()
        # item['dcityname'] = dcityName
        # item['dcity'] = dcity
        with open(f'../data/flights.json', 'a', encoding='utf-8') as f:
            f.write(f'"{dcityName}": ')
            f.write('{')
            f.write(f'"dcity": "{dic.city[dcityName]}", "acityInfo": ')
            acityInfo = {}
            for acitysName in acitysNames:
                # item['acityname'] = acitysName
                # item['acity'] = dic.city[acitysName]
                acityInfo[acitysName] = dic.city[acitysName]
            json.dump(acityInfo, f, ensure_ascii=False)
            f.write('},\n')
            self.logger.info(f'已保存从{dcityName}出发的直达航班')


if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    process.crawl(SchedulesSpider)
    process.start()
