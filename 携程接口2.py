'''
Created on
@Author:你们说的队
@Project:ARIA
@product:PyCharm
@Description:$END$
'''
import requests
import json
import random


#读取文件
def readFile(path):
    content_list = []
    with open(path,'r') as f:
        for content in f:
            content_list.append(content.rstrip())
    return content_list

#写入文件
def writeFile(path,text):
    with open(path,'a') as f:
        f.write(text)
        f.write('\n')

#清空文件
def truncateFile(path):
    with open(path, 'w', encoding='utf-8') as f:
        f.truncate()

#整理城市编码
def splitCity():
    content_list = readFile("/Users/zll/pycharmProjects/studyPython/crawler_poject_base_part1/config/cityInfos")
    fromCity = {}
    cityResultList = []
    # print(content_list)
    for cityInfo in content_list:
        # print(cityInfo)
        cityInfoList = cityInfo.split(":")
        # print(cityInfoList)
        cityCode = cityInfoList[0].lower()
        cityName = cityInfoList[1]
        # print(cityCode)
        # print(cityName)
        cityResult_str = "{"+"\"city\":"+cityCode+","+"\"cityName\":"+cityName+"}"
        # print(cityResult_str)
        cityResult_dict = json.loads(cityResult_str)
        # print(cityResult_dict)
        cityResultList.append(cityResult_dict)
    return cityResultList

def judgeCity(fromCity,toCity,date):
    result = {}
    for city in splitCity():
        # print(city)
        fromResult = fromCity == str(city.get('cityName'))
        toResult = toCity == str(city.get('cityName'))
        if (fromResult == True):
            dcity = city.get('city')
            dcityName = city.get('cityName')
            # print(dcity)
            # print(dcityName)
            result['dcity'] = dcity
            result['dcityName'] = dcityName
        elif(toResult == True):
            acity = city.get('city')
            acityName = city.get('cityName')
            # print(acity)
            # print(acityName)
            result['acity'] = acity
            result['acityName'] = acityName
        else:
            continue
    return result

#随机选取一个代理
def getUserAgent():
    user_agent_list = readFile("/Users/zll/pycharmProjects/studyPython/crawler_poject_base_part1/config/user_agent.txt")
    userAgent = random.choice(user_agent_list)
    return userAgent

#随机选取一个代理ip
# def getIp():
#     ip_list = readFile('/Users/zll/pycharmProjects/studyPython/crawler_poject_base_part1/config/ip.txt')
#     # print(ip_list)
#     ip = random.choice(ip_list)
#     return ip

def getTokenResponse(fromCity,toCity,date):
    cityInfo = judgeCity(fromCity,toCity,date)
    dcity = cityInfo.get('dcity')
    dcityname = cityInfo.get('dcityname')
    acity = cityInfo.get('acity')
    acityname = cityInfo.get('acityname')
    referer = "https://flights.ctrip.com/itinerary/oneway/" + dcity + "-" + acity + "?date=" + date
    url = "https://flights.ctrip.com/itinerary/api/12808/records"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
        "Referer": referer,
        "Content-Type": "application/json"}
    request_payload = {
        "vid": "1586849490183.3km93i"
    }
    print(referer)
    # post请求
    response = requests.post(url, data=json.dumps(request_payload), headers=headers).text
    return response

#获取token
def getToken(fromCity,toCity,date):
    tokenResponse = getTokenResponse(fromCity,toCity,date)
    # print(type(tokenResponse))
    dataInfo_str = json.loads(tokenResponse).get('data')[0].get('data')
    token = dataInfo_str.replace("\\","").split("\"token\":")[1].split("\"")[1]
    return token

# 获取返回结果
def getResponse(fromCity,toCity,date):
    cityInfo = judgeCity(fromCity,toCity,date)
    dcity = cityInfo.get('dcity')
    dcityName = cityInfo.get('dcityName')
    acity = cityInfo.get('acity')
    acityName = cityInfo.get('acityName')
    token = getToken(fromCity,toCity,date)
    url = "https://flights.ctrip.com/itinerary/api/12808/products"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
        "Referer": "https://flights.ctrip.com/itinerary/oneway/"+dcity+"-"+acity+"?date="+date,
        "Content-Type": "application/json"}
    request_payload = {
        "flightWay": "Oneway",
        "classType": "ALL",
        "hasChild": False,
        "hasBaby": False,
        "searchIndex": 1,
        "airportParams": [
            {"dcity": dcity, "acity": acity, "dcityname": dcityName, "acityname": acityName, "date": date}],
        "token": token
    }

    # post请求
    response = requests.post(url, data=json.dumps(request_payload), headers=headers).text

    return response

# 解析返回结果
def parseInfo(fromCity,toCity,date):

    airplaneInfo = {}

    response = getResponse(fromCity,toCity,date)
    print(response)
    # 很多航班信息在此分一下
    routeList = json.loads(response).get('data').get('routeList')
    # print(routeList)
    # 依次读取每条信息
    for route in routeList:
        # 判断是否有信息，有时候没有会报错
        if len(route.get('legs')) == 1:
            legs = route.get('legs')
            flight = legs[0].get('flight')
            # 提取想要的信息
            airlineName = flight.get('airlineName')  # 航空公司
            flightNumber = flight.get('flightNumber')  # 航班编号
            departureDate = flight.get('departureDate')  # 出发时间
            arrivalDate = flight.get('arrivalDate')  # 到达时间
            craftTypeName = flight.get('craftTypeName')  # 飞机类型
            craftTypeKindDisplayName = flight.get('craftTypeKindDisplayName')  # 飞机型号：大型；中型，小型

            departureCityName = flight.get('departureAirportInfo').get('cityName')  # 出发城市
            departureAirportName = flight.get('departureAirportInfo').get('airportName')  # 出发机场名称
            departureTerminalName = flight.get('departureAirportInfo').get('terminal').get('name')  # 出发机场航站楼
            arrivalCityName = flight.get('arrivalAirportInfo').get('cityName')  # 到达城市
            arrivalAirportName = flight.get('arrivalAirportInfo').get('airportName')  # 到达机场名称
            arrivalTerminalName = flight.get('arrivalAirportInfo').get('terminal').get('name')  # 到达机场航站楼

            punctualityRate = flight.get('punctualityRate')  # 到达准点率
            mealType = flight.get('mealType')  # 是否有餐食  None：代表无餐食，Snack：代表小食，Meal：代表含餐食

            cabins = legs[0].get('cabins')
            price = cabins[0].get('price').get('price')  # 标准价格
            rate = cabins[0].get('price').get('rate')  # 折扣率
            seatCount = cabins[0].get('seatCount')  # 剩余座位数

            refundEndorse = cabins[0].get('refundEndorse').get('minRefundFee')  # 成人票：产品退订费
            minEndorseFee = cabins[0].get('refundEndorse').get('minRefundFee')  # 成人票：产品更改费
            endorseNote = cabins[0].get('refundEndorse').get('endorseNote')  # 成人票：签转条件

            freeLuggageAmount = cabins[0].get('freeLuggageAmount')  # 免费托运重量

            carryonLuggageMaxAmount = cabins[0].get('luggageLimitation').get(
                'carryonLuggageMaxAmount')  # 允许携带手提行李最大数量    0：代表无免费行李额，1：代表一件，-2：代表不限件数
            carryonLuggageMaxWeight = cabins[0].get('luggageLimitation').get('carryonLuggageMaxWeight')  # 允许携带手提行李最大重量
            carryonLuggageMaxSize = cabins[0].get('luggageLimitation').get('carryonLuggageMaxSize')  # 允许携带手提行李最大规格
            checkinLuggageMaxAmount = cabins[0].get('luggageLimitation').get(
                'checkinLuggageMaxAmount')  # 允许托运的行李最大数量类型   0：代表无免费行李额，1：代表一件，-2：代表不限件数
            checkinLuggageMaxWeight = cabins[0].get('luggageLimitation').get('checkinLuggageMaxWeight')  # 允许托运的行李最大重量
            checkinLuggageMaxSize = cabins[0].get('luggageLimitation').get('checkinLuggageMaxSize')  # 允许托运的行李最大规格

            characteristic = legs[0].get('characteristic')
            lowestPrice = characteristic.get('lowestPrice')  # 成人经济舱最低价
            lowestCfPrice = characteristic.get('lowestCfPrice')  # 成人公务舱最低价
            lowestChildPrice = characteristic.get('lowestChildPrice')  # 儿童经济舱最低价
            lowestChildCfPrice = characteristic.get('lowestChildCfPrice')  # 儿童公务舱最低价

            #将数据放入字典
            airplaneInfo["airlineName"] = airlineName
            airplaneInfo["flightNumber"] = flightNumber
            airplaneInfo["departureDate"] = departureDate
            airplaneInfo["arrivalDate"] = arrivalDate
            airplaneInfo["craftTypeName"] = craftTypeName
            airplaneInfo["craftTypeKindDisplayName"] = craftTypeKindDisplayName
            airplaneInfo["departureCityName"] = departureCityName
            airplaneInfo["departureAirportName"] = departureAirportName
            airplaneInfo["departureTerminalName"] = departureTerminalName
            airplaneInfo["arrivalCityName"] = arrivalCityName
            airplaneInfo["arrivalAirportName"] = arrivalAirportName
            airplaneInfo["arrivalTerminalName"] = arrivalTerminalName
            airplaneInfo["punctualityRate"] = punctualityRate
            airplaneInfo["mealType"] = mealType
            airplaneInfo["price"] = price
            airplaneInfo["rate"] = rate
            airplaneInfo["seatCount"] = seatCount
            airplaneInfo["refundEndorse"] = refundEndorse
            airplaneInfo["minEndorseFee"] = minEndorseFee
            airplaneInfo["endorseNote"] = endorseNote
            airplaneInfo["freeLuggageAmount"] = freeLuggageAmount
            airplaneInfo["carryonLuggageMaxAmount"] = carryonLuggageMaxAmount
            airplaneInfo["carryonLuggageMaxWeight"] = carryonLuggageMaxWeight
            airplaneInfo["carryonLuggageMaxSize"] = carryonLuggageMaxSize
            airplaneInfo["checkinLuggageMaxAmount"] = checkinLuggageMaxAmount
            airplaneInfo["checkinLuggageMaxWeight"] = checkinLuggageMaxWeight
            airplaneInfo["checkinLuggageMaxSize"] = checkinLuggageMaxSize
            airplaneInfo["lowestPrice"] = lowestPrice
            airplaneInfo["lowestCfPrice"] = lowestCfPrice
            airplaneInfo["lowestChildPrice"] = lowestChildPrice
            airplaneInfo["lowestChildCfPrice"] = lowestChildCfPrice


            print(airlineName, "\t",
                  flightNumber, "\t",
                  departureDate, "\t",
                  arrivalDate, "\t",
                  craftTypeName, "\t",
                  craftTypeKindDisplayName, "\t",
                  departureCityName, "\t",
                  departureAirportName, "\t",
                  departureTerminalName, "\t",
                  arrivalCityName, "\t",
                  arrivalAirportName, "\t",
                  arrivalTerminalName, "\t",
                  punctualityRate, "\t",
                  mealType, "\t",
                  price, "\t",
                  rate, "\t",
                  seatCount, "\t",
                  refundEndorse, "\t",
                  minEndorseFee, "\t",
                  endorseNote, "\t",
                  freeLuggageAmount, "\t",
                  carryonLuggageMaxAmount, "\t",
                  carryonLuggageMaxWeight, "\t",
                  carryonLuggageMaxSize, "\t",
                  checkinLuggageMaxAmount, "\t",
                  checkinLuggageMaxWeight, "\t",
                  checkinLuggageMaxSize, "\t",
                  lowestPrice, "\t",
                  lowestCfPrice, "\t",
                  lowestChildPrice, "\t",
                  lowestChildCfPrice, "\t"
                  )

        print(airplaneInfo)

if __name__ == "__main__":
    fromCity = input("出发城市：")
    toCity = input("目的城市：")
    date = input("出发日期：")
    # re = getResponse(fromCity,toCity,date)
    # print(re)
    # parseInfo(fromCity,toCity,date)
    # m = judgeCity(fromCity,toCity)
    # printa(m)
    a = getResponse(fromCity,toCity,date)
    print(a)

    t = getToken(fromCity,toCity,date)
    print(t)

