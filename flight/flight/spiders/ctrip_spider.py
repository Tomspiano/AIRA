# -*- coding: utf-8 -*-
"""
Created on 2020/11/13
@Author: 你们说的队
@Project: AIRA
@Product: PyCharm
@Description: 携程旅行直达查询
"""
from abc import ABC
import scrapy
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

    def __init__(self):
        super(CtripSpider, self).__init__()
        # self.dcityname = '北京'
        # self.dcity = 'bjs'
        # self.acities = [{'阿尔山': 'yie'}, {'毕节': 'bfj'}]
        # self.date = '2020-12-1'
        self.dcityname = ''
        self.dcity = ''
        self.acities = []
        self.date = ''

        self.context = execjs.compile(js_from_file('flight/spiders/modules/token.js'))
        self.referer = 'https://flights.ctrip.com/itinerary/oneway/'
        self.api = 'https://flights.ctrip.com/itinerary/api/12808/products'

        self.remote = 'http://airaflyscanner.site:8000/normalResearch/'

    def get_info(self, info):
        self.dcityname = info['dcityname']
        self.dcity = info['dcity']
        self.acities = info['acities']
        self.date = info['date']

    def start_requests(self):
        for acityname, acity in self.acities.items():
            token = self.context.call('get_token', str.upper(self.dcity), str.upper(acity), 'Oneway')
            headers = {
                'content-Type': 'application/json',
                'referer'     : ''.join(
                        [self.referer, self.dcity, '-', acity, '?', 'date=', self.date, '&sortByPrice=true']),
                'user-agent'  : ''
            }
            payload = {
                'airportParams': [
                    {
                        'dcity'    : self.dcity, 'acity': acity,
                        'dcityname': self.dcityname, 'acityname': acityname,
                        'date'     : self.date}],
                'classType'    : 'ALL',
                'date'         : self.date,
                'flightWay'    : 'Oneway',
                'hasBaby'      : 'false',
                'hasChild'     : 'false',
                'searchIndex'  : '1',
                'sortByPrice'  : 'true',
                'token'        : token
            }
            yield scrapy.Request(url=self.api, method='POST', headers=headers, body=json.dumps(payload),
                                 callback=self.parse, cb_kwargs={'acityname': acityname, 'acity': acity})

    def parse(self, response, **kwargs):
        routeList = json.loads(response.text)['data']['routeList']

        item = LowestPrice()
        lowest = -1
        for i, route in enumerate(routeList):
            if route['routeType'] != 'Flight':
                if i == 0:
                    self.logger.info('无{}-{}的直达航班'.format(self.dcityname, kwargs['acityname']))
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
                item['url'] = ''.join(
                        [self.referer, self.dcity, '-', kwargs['acity'], '?', 'date=', self.date, '&sortByPrice=true'])

        headers = {
            'content-Type': 'application/json',
            'user-agent'  : ''
        }
        yield scrapy.Request(url=self.remote, method='POST', headers=headers, body=json.dumps(dict(item)),
                             callback=self.check_info)

    @staticmethod
    def check_info(response):
        print(response.text)
