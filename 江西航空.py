# -*-codeing = utf-8 -*-
'''
Created on 
@Author:你们说的队
@Project:proxyPool.py
@product:PyCharm
@Description:$END$
'''
import requests
import json
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
def post():
    orgcity = 'KHN'
    dstcity = 'PEK'
    url = "http://www.airjiangxi.com/jiangxiair/book/findFlights.action?tripType=0&queryFlightInfo=KHN,PEK,2020-12-01&adult=1&child=0&infant=0"
    User_Agent = str(UserAgent().random)
    headers = {
        "User-Agent":User_Agent,
        'Referer':"http://www.airjiangxi.com/jiangxiair/book/findFlights.action?tripType=0&queryFlightInfo=KHN,PEK,2020-12-01&adult=1&child=0&infant=0"
    }
    response = requests.post(url,headers=headers).text
    soup = BeautifulSoup(response, 'html.parser')
    r = soup.find('input', id='random')['value']
    url2 = "http://www.airjiangxi.com/jiangxiair/book/findFlights.json?" + "r="+r+"&takeoffDate=2020-12-01&returnDate=&orgCity=KHN&dstCity=PEK&tripType=0&adult=1&child=0&infant=0&channelId=1&_=1606471679641"
    response2 = requests.post(url2, headers=headers).text
    print(response2)
    return
post()
