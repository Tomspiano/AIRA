# -*- coding: utf-8 -*-
"""
Created on 2020/12/17
@Author: 你们说的队
@Project: AIRA
@Product: PyCharm
@Description: 瑞丽航空特价机票爬取
"""

import requests
import json
def getRlairSpecialTickets():
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }
    url = 'https://www.rlair.net/BasicInfo/Specialticket/GetSpecialTicketDatas'
    # 字符串传递参数, pageSize为该接口一次返回特价机票数
    # 通过该接口返回数据中的total参数可获知特价机票数
    # 故只需通过两次GET请求就可获得全部特价机票信息
    pageSize = 1
    pageIndex = 1
    flightDateBegin = ''
    flightDateEnd = ''
    topIATACode = 'FOC'
    queryStringParameters = \
        '?pageSize={}&' \
        'pageIndex={}&' \
        'flightDateBegin={}&' \
        'flightDateEnd={}&' \
        'topIATACode={}'.format(
            pageSize, pageIndex,
            flightDateBegin, flightDateEnd,
            topIATACode
            )

    ticketInfo = {
        'dcity': '',
        'dcityName': '',
        'acity': '',
        'acityName': '',
        'price': '',
        'dtime': '',
        'url': 'https://www.rlair.net/BasicInfo/Specialticket/GetSpecialTicketDatas',
        'companyName': '瑞丽航空'
    }
    r = requests.get(url+queryStringParameters, headers=headers)
    if r.status_code != 200:
        return None
    data = r.json()
    # pageSize = total
    queryStringParameters = \
        '?pageSize={}&' \
        'pageIndex={}&' \
        'flightDateBegin={}&' \
        'flightDateEnd={}&' \
        'topIATACode={}'.format(
                data['total'], pageIndex,
                flightDateBegin, flightDateEnd,
                topIATACode
        )
    r = requests.get(url + queryStringParameters, headers=headers)
    if r.status_code != 200:
        return None
    data = r.json()
    ticketInfoList = data['rows']
    tickets = []
    for info in ticketInfoList:
        ticketInfo['dcityName'] = info['DEPARTURENAME']
        ticketInfo['dcity'] = info['DEPARTURE']
        ticketInfo['acityName'] = info['ARRIVALNAME']
        ticketInfo['acity'] = info['ARRIVAL']
        ticketInfo['price'] = info['PRICE']
        ticketInfo['dtime'] = info['FLIGHTDATE']
        tickets.append(ticketInfo.copy())

    return tickets


if __name__ == '__main__':
    print('rlair')
    tickets = getRlairSpecialTickets()
    for ticket in tickets:
        print(ticket)
