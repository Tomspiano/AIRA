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
from flight.items import ScheduleItem
from modules import dictionary as dic


class SchedulesSpider(scrapy.Spider):
    name = 'schedules'

    def start_requests(self):
        for cityName, cityAbbr in dic.city.items():
            url = 'https://flights.ctrip.com/schedule/{}..html'.format(cityAbbr)
            yield scrapy.Request(url=url, callback=self.parse, cb_kwargs={'dcityName': cityName, 'dcityAbbr': cityAbbr})

    def parse(self, response, **kwargs):
        dcityName = kwargs['dcityName']
        dcity = kwargs['dcityAbbr']
        acitysNames = response.css('div.m a::text').re(r'-(\w+)')

        if len(acitysNames) == 0:
            self.logger.info('无从{}出发的国内航班'.format(dcityName))
            return

        item = ScheduleItem()
        item['dcityname'] = dcityName
        item['dcity'] = dcity
        for acitysName in acitysNames:
            item['acityname'] = acitysName
            item['acity'] = dic.city[acitysName]
            # TODO(Tomspiano): 保存到数据库
            self.logger.info('已保存{}-{}'.format(dcityName, acitysName))


if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    process.crawl(SchedulesSpider)
    process.start()
