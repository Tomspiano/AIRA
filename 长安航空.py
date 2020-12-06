import requests
import json
from fake_useragent import UserAgent
url = "http://www.airchangan.com/portal/api/v1/home/recommendList"

headers = {
    # "Accept":"application/json, text/plain",
    # "Host": "www.airchangan.com",
    # "Connection": "keep-alive",
    # "Origin": "http://www.airchangan.com",
    # "Referer": "http://www.airchangan.com/portal",
    "User-Agent":"{}".format(UserAgent().random)
    # "Cookie":"route=f99c91aea9ce8f88fcb593a28dd49be5; _4fd8e=http://172.31.95.93:8080; nodeWeb=s%3AKQnlf4_8eEmrJQ2LHplaL7kiiWscYn9X.57l3bNAs%2FHNFCGHhBMcOR%2Bl1fliPRrxkq1PZTiJb2Do; _ga=GA1.2.1384395914.1606895525; _gid=GA1.2.414949610.1606895525; _gat_TrueMetrics=1"
}
for i in range(10):
    response = requests.post(url=url, headers=headers).text
# print(response)
    data = json.loads(response)
# print(data)
    guesslike = data.get("data")
# print(flightroutes)
# print(type(flightroutes))
    dict = {}

    for flight in guesslike:
        dict["dcity"] = flight.get("cityFrom")
        dict["acity"] = flight.get("cityTo")
        dict["price"] = flight.get("price")
        dict['company'] = '长安航空'
        print(dict)