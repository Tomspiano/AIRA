from bs4 import BeautifulSoup
import requests
import json
from fake_useragent import UserAgent

url = "https://www.hnair.com/"
headers = {
    'Accept-Language':'zh-CN',
    'User-Agent':'{}'.format(UserAgent().random)
}
response = requests.get(url=url,headers=headers).text.encode('iso-8859-1').decode('utf8')
# print(response)
soup = BeautifulSoup(response,'lxml')
div = soup.find_all('div',attrs={'class':['tab-item-flight']})
for i in div:
    dict = {}
    dcity = i.find('span',attrs={'class':['site-origin']})
    acity = i.find('span',attrs={'class':['site-end']})
    price = i.find('strong')
    dict['dcity'] = dcity.string
    dict['acity'] = acity.string
    dict['price'] = price.string
    dict['company'] = '海南航空'
    print(dict)