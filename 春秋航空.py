import requests
import json
from bs4 import BeautifulSoup

url = "https://pages.ch.com/second-kill"
response = requests.get(url=url).text
# print(resonsse)
soup = BeautifulSoup(response,'lxml')
div = soup.find_all('div',attrs={'class':['travel-data']})
for i in div:
    dict = {}
    places = i.find('div',attrs={'class':['place']})
    price = i.find('div',attrs={'class':['price-detail']}).find('em').string
    cities = places.find_all('span')
    dict['price'] = price
    dict['dcityName'] = cities[0].string
    dict['acityName'] = cities[1].string
    dict['company'] = '春秋航空'
    # for city in cities:
        # print(city.string)
    # print(places)
    print(dict)