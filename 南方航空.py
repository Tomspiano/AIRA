import requests
import json

url= 'https://b2c.csair.com/portal/minPrice/queryMinPriceInAirLines?jsoncallback=getMinPrice&inter=N&callback=getMinPrice&_=1607846317154'
reponse = requests.get(url=url).text
reponse = reponse[12:-1]
# print(reponse)
data = json.loads(reponse)
flights= data.get("FROMOFLIGHTS")
for flight in flights:
    dict = {}
    dict['dcityName'] = flight.get('DEPCTIYNAME_ZH')
    tickets = flight.get("FLIGHT")
    for ticket in tickets:
        dict['actiyName'] = ticket.get('ARRCTIYNAME_ZH')
        dict['price'] = ticket.get('MINPRICE')
        dict['company']  = '南方航空'
        print(dict)
