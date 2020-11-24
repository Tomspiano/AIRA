# -*- coding: utf-8 -*-
"""
Created on 2020/11/13
@Author: 你们说的队
@Project: AIRA
@Product: PyCharm
@Description: 携程旅行直达航班
"""
from abc import ABC
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from flight.items import LowestPrice
import execjs
import json


def js_from_file(file_name):
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            js = f.read()
        return js
    except FileNotFoundError:
        import os
        print('无法读取js文件，当前路径为：{}'.format(os.getcwd()))


class CtripSpider(scrapy.Spider, ABC):
    name = 'ctrip'

    custom_settings = {'LOG_FILE': 'ctrip_log.txt'}

    def __init__(self):
        super(CtripSpider, self).__init__()
        self.max_retry_times = 2
        self.priority_adjust = -2

        self.flights = {}
        self.dates = []
        self.get_info('info/post_info.json')

        self.context = execjs.compile(js_from_file('modules/token.js'))
        self.referer = 'https://flights.ctrip.com/itinerary/oneway/'
        self.api = 'https://flights.ctrip.com/itinerary/api/12808/products/oneway'

        self.remote = 'http://airaflyscanner.site:8000/normalResearch/'

    def get_info(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            info = json.load(f)

        self.flights = info['flights']
        self.dates = info['date']

    def start_requests(self):
        for date in self.dates:
            for dcityname, info in self.flights.items():
                dcity = info['dcity']
                acityInfo = info['acityInfo']
                for acityname, acity in acityInfo.items():
                    token = self.context.call('get_token', str.upper(dcity), str.upper(acity), 'Oneway')
                    headers = {
                        'content-Type': 'application/json',
                        'referer'     : ''.join(
                                [self.referer, dcity, '-', acity, '?', 'date=', date, '&sortByPrice=true']),
                        'user-agent'  : ''
                    }
                    payload = {
                        'airportParams': [
                            {
                                'dcity'    : dcity, 'acity': acity,
                                'dcityname': dcityname, 'acityname': acityname,
                                'date'     : date}],
                        'classType'    : 'ALL',
                        'date'         : date,
                        'flightWay'    : 'Oneway',
                        'hasBaby'      : 'false',
                        'hasChild'     : 'false',
                        'searchIndex'  : '1',
                        'sortByPrice'  : 'true',
                        'token'        : token
                    }
                    yield scrapy.Request(url=self.api, method='POST', headers=headers, body=json.dumps(payload),
                                         callback=self.parse, cb_kwargs={
                            'dcityname': dcityname, 'acityname': acityname,
                            'url'      : headers['referer']})

    def parse(self, response, **kwargs):
        # with open('response/ctrip.json', 'a', encoding='utf-8') as f:
        #     f.write(f'{response.text}\n')

        try:
            routeList = json.loads(response.text)['data']['routeList']

            item = LowestPrice()
            lowest = -1
            for i, route in enumerate(routeList):
                if route['routeType'] != 'Flight':
                    if i == 0:
                        self.logger.info('无{}-{}的直达航班'.format(kwargs['dcityname'], kwargs['acityname']))
                        return
                    break

                priceInfo = route['legs'][0]['cabins'][0]['price']
                price = priceInfo['price']
                if lowest == -1 or price < lowest:
                    item['price'] = price
                    item['rate'] = priceInfo['rate']

                    flight = route['legs'][0]['flight']
                    # item['airlineName'] = flight['airlineName']
                    item['flightNumber'] = flight['flightNumber']
                    # item['flightId'] = flight['id']
                    item['acity'] = flight['arrivalAirportInfo']['airportTlc']
                    item['acityName'] = flight['arrivalAirportInfo']['cityName']
                    item['arrivalDate'] = flight['arrivalDate']
                    item['aairport'] = flight['arrivalAirportInfo']['airportName']
                    item['dcity'] = flight['departureAirportInfo']['airportTlc']
                    item['dcityName'] = flight['departureAirportInfo']['cityName']
                    item['departureDate'] = flight['departureDate']
                    item['dairport'] = flight['departureAirportInfo']['airportName']
                    item['url'] = kwargs['url']

        except KeyError:
            self.logger.critical('无法获取数据')
            self.crawler.engine.close_spider(self, '无法获取数据，请分析原因')

        except TypeError:
            retries = response.meta.get('empty_retry', 0) + 1
            stats = self.crawler.stats
            if retries <= self.max_retry_times:
                self.logger.debug('"routeList" is not iterable')
                retryreq = response.request.copy()
                retryreq.meta['empty_retry'] = retries
                retryreq.dont_filter = True
                retryreq.priority = response.request.priority + self.priority_adjust
                stats.inc_value('retry/count')
                yield retryreq
            else:
                stats.inc_value('retry/max_reached')
                self.logger.error(
                        f'放弃重试{response.request} (failed {retries}d times): '
                        f'\'NoneType\' object is not iterable')

        else:
            headers = {
                'content-Type': 'application/json',
                'user-agent'  : ''
            }
            yield scrapy.Request(url=self.remote, method='POST', headers=headers, body=json.dumps(dict(item)),
                                 callback=self.check_info, cb_kwargs=kwargs)

    def check_info(self, response, **kwargs):
        if response.text not in ['OK', '更新成功']:
            self.logger.info(f'保存情况({kwargs["dcityname"]}-{kwargs["acityname"]}): {response.text}')


if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    process.crawl(CtripSpider)
    process.start()
