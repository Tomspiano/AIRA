import requests
import json
# from fake_useragent import UserAgent

url = 'https://www.fuzhou-air.cn/frontend/api/flight.action'

headers = {
            'Accept': 'application/json',
            # 'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json;charset=UTF-8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.47',
            # 不需要referer
            # Referer
            # 'Referer':'http://www.fuzhou-air.cn/b2c/search/searchflight.jsp?type=TKT\
            #     &orgCityCode={}\
            #     &dstCityCode={}\
            #     &orgDate={}\
            #     &dstDate=&adult=1&child=0&infant=0&trip=ONEWAY'.format('FOC','YIH','2020-12-1'),
            }

request_payload = {
    'orgCity':'FOC',
    'dstCity':'YIH',
    'flightdate':'2020-11-29',
    'index':0,
    'tripType':'ONEWAY',
    'type':1
}
# response = requests.post(url=url, timeout=30).text
response = requests.post(url=url, data=json.dumps(request_payload), headers=headers).text
data = json.loads(response).get('data')
print(type(data))
flights = data.get('flights')
# print(flights)
dict = {}
departCity = data.get('orgCity')
arrivalCity = data.get('dstCity')
dict['dcityName'] = departCity.get('name')
dict['acityName'] = arrivalCity.get('name')
dict['dairportName'] = departCity.get('orgAirport')
dict['aairportName'] = arrivalCity.get('dstAirport')
dict['dcityCode'] = departCity.get('code')
dict['acityCode'] = arrivalCity.get('code')

for flight in flights:
    # print(flight)
    segments = flight.get('segments')
    for segment in segments:
        dict['departureDate'] = segment.get('departureTime')
        dict['arrivalDate'] = segment.get('arriveTime')
        dict['flightNumber'] = segment.get('airline').get('airline') + segment.get('flightno')
        dict['companyName'] = segment.get('airline').get('name')
        dict['price'] = segment.get('lowestPrice')
        print(dict)