# -*- coding: utf-8 -*-
"""
Created on 2020/11/18
@Author: 你们说的队
@Project: AIRA
@Product: PyCharm
@Description: 国内城市补充
"""
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from modules import dictionary as dic


class CitiesSpider2(scrapy.Spider):
    name = 'cities2'
    custom_settings = {'LOG_FILE': 'cities_log.txt'}
    start_urls = ['https://flights.ctrip.com/schedule/']

    def parse(self, response, **kwargs):
        i = 0
        with open('../data/cityNameAbbr2.txt', 'w', encoding='utf-8') as f:
            for flight in response.css('div.m a'):
                cityName = flight.css('::text').re(r'(\w+)航班')[0]
                if cityName not in dic.city:
                    cityAbbr = flight.css('::attr(href)').re(r'/(\w+)..html$')[0]
                    f.write(''.join(["'", cityName, "':'", cityAbbr, "',"]))
                    i += 1
                    if i % 5 == 0:
                        f.write('\n')


if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    process.crawl(CitiesSpider2)
    process.start()
