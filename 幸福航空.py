# -*-codeing = utf-8 -*-
'''
Created on 
@Author:你们说的队
@Project:proxyPool.py
@product:PyCharm
@Description:$END$
'''
import time
import requests
import json
import execjs
import random
from fake_useragent import UserAgent
import pprint
def MyRequest():
    url = "http://www.joy-air.com/api/index!getRecommandAirlines.action?depCode=ALL"
    User_Agent = str(UserAgent().random)
    headers = {
        "User-Agent": User_Agent
    }
    response = requests.get(url=url,headers = headers).text
    get_content(response)
def get_content(response):
    datas = json.loads(response).get('data')
    for data in datas:
        acity = data.get("tktFrom")
        dcity = data.get("tktTo")
        begintime = data.get("beginTime")
        endtime = data.get("endTime")
        price = data.get("preferentialPrice")
        print(acity,dcity,begintime,endtime,price)
if __name__ == '__main__':
    MyRequest()