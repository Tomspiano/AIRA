# -*- coding: utf-8 -*-
"""
Created on 2020/11/30
@Author: 你们说的队
@Project: AIRA
@Product: PyCharm
@Description: 
"""
import requests
import json

# 其实可以不通过接口爬,特价机票页面网址:https://www.okair.net/services.html#/onSaleLines
# 但该网站特价机票页面上的数据有限
# 看后面给的特价机票接口是怎样的了
"""奥凯航空特价机票"""
def okairTickets():
    tickets = []
    fltDate = []
    ticketInfo = {
        'departureDate': '',
        'arrivalDate': '',
        'dairport': '',
        'aairport': '',
        'flightNumber': '',
        'dcity': '',
        'dcityName': '',
        'acity': '',
        'acityName': '',
        'price': 0,
        'rate': 0.0,
        'url': 'https://www.okair.net/api/pub/initHomePageSaleInfo',
        'companyName': '奥凯航空'
    }
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }
    url = 'https://www.okair.net/api/pub/initHomePageSaleInfo'
    payload = {
        "org": ""
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    # 向这个Url发送Post请求 得到的数据只有一个航班日期, 没有出发时间和到达时间和航班号信息
    saleInfo = response.json()
    if saleInfo['errorMsg'] == '成功':
        ticketData = saleInfo['resData']['allSaleInfo']
        for sameDiscountRateTickets in ticketData.values():
            for aTicket in sameDiscountRateTickets:
                ticketInfo['dcity'] = aTicket['org']
                ticketInfo['dcityName'] = aTicket['orgName']
                ticketInfo['dairport'] = aTicket['orgInfo']['airportLongName']
                ticketInfo['acity'] = aTicket['dst']
                ticketInfo['acityName'] = aTicket['dstName']
                ticketInfo['aairport'] = aTicket['dstInfo']['airportLongName']
                ticketInfo['price'] = aTicket['priceInfo']['skPrice']
                ticketInfo['rate'] = float(aTicket['disCount'])/10.0
                tickets.append(ticketInfo.copy())
                fltDate.append(aTicket['fltDate'])
    # 最终数据
    finalTickets = []
    # 向这个Url发送Post请求 data 为出发和目的地点城市编码和fltDate
    url = 'https://www.okair.net/api/pub/queryFare'
    for i in range(0, len(tickets)):
        payload = {
                'org': tickets[i]['dcity'],
                'dst': tickets[i]['acity'],
                'fltDate': fltDate[i]
        }
        r = requests.post(url, headers=headers, data=json.dumps(payload))
        if r.status_code == 200:
            dayInfo = r.json()
            if dayInfo['errorMsg'] == '成功':
                # 如果同一天飞往从同一起点飞往同一个终点的航班有多个可能会数量会多于1
                for t in dayInfo['resData']:
                    tempTicket = tickets[i].copy()
                    if len(t['segmentList']) > 1:
                        # 我是真的不知道为什么这个列表数据会多于1了
                        print("我好菜啊")
                        return
                    segmentList = t['segmentList'][0]
                    ddateStr = segmentList['depDate'] + segmentList['depTime']
                    adateStr = segmentList['arrDate'] + segmentList['arrTime']
                    tempTicket['departureDate'] = '{}-{}-{} {}:{}:00'.format(ddateStr[0:4], ddateStr[4:6],
                                                                            ddateStr[6:8], ddateStr[8:10],
                                                                             ddateStr[10:12])
                    tempTicket['arrivalDate'] = '{}-{}-{} {}:{}:00'.format(adateStr[0:4], adateStr[4:6],
                                                                            adateStr[6:8], adateStr[8:10],
                                                                           adateStr[10:12])
                    tempTicket['flightNumber'] = segmentList['fltNo']
                    print(tempTicket)
                    finalTickets.append(tempTicket)

            else:
                print("没有该机票的航班信息"+str(fltDate[i])+str(tickets[i]))
                # 可是为什么有特价机票里有却没有航班信息啊
                # 重复测试却可能会再次出现航班信息,好奇怪啊
        else:
            print("Post请求失败")
            # 这个航空网站太友好了,怎么请求都不会封

    return finalTickets


if __name__ == '__main__':
    tickets = okairTickets()
    print('----------------------------------------------------------------')
    for ticket in tickets:
        print(ticket)