# -*- coding: utf-8 -*-
"""
Created on 2020/12/17
@Author: 你们说的队
@Project: AIRA
@Product: PyCharm
@Description: 华夏航空特价机票获取
"""
import requests
import bs4
import lxml
import json
import time

def getChinaexpressairSpecialTickets():
    ticketInfo = {
        'dcity'      : '',
        'dcityName'  : '',
        'acity'      : '',
        'acityName'  : '',
        'price'      : '',
        'dtime'      : '',
        'url'        : 'https://www.chinaexpressair.com',
        'companyName': '华夏航空'
    }
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Host': 'www.chinaexpressair.com',
        'Referer': 'https://www.chinaexpressair.com/',
        'Accept': '*/*'
    }
    url = 'https://www.chinaexpressair.com/index/tejia.jhtml'
    # 字符串传递参数, depCode为出发地城市代码
    # 返回结果为机票信息
    # 观察官网可发现官网只给出了几个城市代码，故  默认  特价机票只有官网给出的几个城市
    # 所以先通过官网Html页面获取给出的城市代码 depCodeList = getDepCodeList()
    # 但是返回结果可能存在重复，而且即使设置了出发城市也会返回不同的出发城市的结果？？？
    depCodeList = getDepCodeList()
    tickets = []
    for depCode in depCodeList:
        queryStringParameters = '?depCode={}&callback=showTejia'.format(depCode)
        print(url+queryStringParameters)
        # verify=False 否则会出现Max retries exceeded with url错误
        r = requests.get(url + queryStringParameters, headers=headers, verify=False)
        dataStr = r.content.decode('utf-8')[10:-1]
        dataList = json.loads(dataStr)
        for data in dataList:
            # print(data)
            if data['depCode'] in cityNameAbbr.keys() and data['arrCode'] in cityNameAbbr.keys():
                ticketInfo['dcity'] = data['depCode']
                ticketInfo['acity'] = data['arrCode']
                ticketInfo['dcityName'] = cityNameAbbr[data['depCode']]
                ticketInfo['acityName'] = cityNameAbbr[data['arrCode']]
                ticketInfo['dtime'] = data['depDate']+' '+data['depTime']+':00'
                ticketInfo['price'] = data['price']
                ticketInfo['rate'] = float(data['discount'])
                tickets.append(ticketInfo.copy())
    # 去重
    tickets = deleteDuplicate(tickets)
    return tickets
def getDepCodeList():
    """ 获取华夏航空网站首页特价机票起始城市代码列表 """
    DepCodeList = []
    url = 'https://www.chinaexpressair.com'
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }
    try:
        # verify=False 否则会出现Max retries exceeded with url错误
        response = requests.get(url, headers=headers, verify=False)
        if response.status_code == 200:
            htmlStr = response.text
    except requests.RequestException:
        print('获取网页失败')
        return None
    soup = bs4.BeautifulSoup(htmlStr, 'lxml')
    items = soup.find(class_='cities-active')
    infos = items.find_all('a')
    for info in infos:
        DepCodeList.append(info.get('data-code'))
    return DepCodeList

def deleteDuplicate(sourceList):
    """ 字典列表去重 """
    return [dict(t) for t in set([tuple(d.items()) for d in sourceList])]

cityNameAbbr = {
    "AAT": "阿勒泰", "AKU": "阿克苏", "AOG": "鞍山", "AQG": "安庆", "AVA": "安顺", "AXF": "阿拉善左旗", "MFM": "澳门",
    "NGQ": "阿里", "RHT": "阿拉善右旗", "YIE": "阿尔山", "BZX": "巴中", "AEB": "百色", "BAV": "包头", "BFJ": "毕节",
    "BHY": "北海", "BJS": "北京", "BPL": "博乐", "BSD": "保山", "DBC": "白城", "KJI": "布尔津", "NBS": "白山",
    "RLK": "巴彦淖尔", "BPX": "昌都", "CDE": "承德", "CGD": "常德", "CGQ": "长春", "CHG": "朝阳", "CIF": "赤峰",
    "CIH": "长治", "CKG": "重庆", "CSX": "长沙", "CTU": "成都", "CWJ": "沧源", "CZX": "常州", "JUH": "池州", "SWA": "汕头",
    "DAT": "大同", "DAX": "达州", "DCY": "稻城", "DDG": "丹东", "DIG": "香格里拉", "DLC": "大连", "DLU": "大理", "DNH": "敦煌",
    "DOY": "东营", "DQA": "大庆", "HXD": "德令哈", "LUM": "芒市", "DSN": "鄂尔多斯", "EJN": "额济纳旗", "ENH": "恩施",
    "ERL": "二连浩特", "FOC": "福州", "FUG": "阜阳", "FYJ": "抚远", "FYN": "富蕴", "CAN": "广州", "GMQ": "果洛",
    "GOQ": "格尔木", "GYS": "广元", "GYU": "固原", "KHH": "高雄", "KOW": "赣州", "KWE": "贵阳", "KWL": "桂林", "AHJ": "红原",
    "HAK": "海口", "HCJ": "河池", "HDG": "邯郸", "HEK": "黑河", "HET": "呼和浩特", "HFE": "合肥", "HGH": "杭州", "HIA": "淮安",
    "HJJ": "芷江", "HLD": "海拉尔", "HMI": "哈密", "HNY": "衡阳", "HRB": "哈尔滨", "HTN": "和田", "HTT": "花土沟",
    "HUN": "花莲", "HUO": "霍林郭勒", "HUZ": "惠州", "HZG": "汉中", "TXN": "黄山", "XRQ": "呼伦贝尔", "CYI": "嘉义",
    "JDZ": "景德镇", "JGD": "加格达奇", "JGN": "嘉峪关", "JGS": "井冈山", "JHG": "西双版纳", "JIC": "金昌", "JIU": "九江",
    "JJN": "石狮", "JM1": "荆门", "JMU": "佳木斯", "JNG": "济宁", "JNZ": "锦州", "JSJ": "建三江", "JXA": "鸡西",
    "JZH": "九寨沟", "KNH": "金门", "TNA": "济南", "KCA": "库车", "KGT": "康定", "KHG": "喀什", "KJH": "凯里", "KMG": "昆明",
    "KRL": "库尔勒", "KRY": "克拉玛依", "HZH": "黎平", "JMJ": "澜沧", "LCX": "龙岩", "LFQ": "临汾", "LHW": "兰州",
    "LJG": "丽江", "LLB": "荔波", "LLV": "吕梁", "LNJ": "临沧", "LNL": "陇南", "LPF": "六盘水", "LXA": "拉萨", "LYA": "洛阳",
    "LYG": "连云港", "LYI": "临沂", "LZH": "柳州", "LZO": "泸州", "LZY": "林芝", "MDG": "牡丹江", "MFK": "马祖", "MIG": "绵阳",
    "MXZ": "梅州", "MZG": "澎湖列岛", "NZH": "满洲里", "OHE": "漠河", "KHN": "南昌", "LZN": "南竿", "NAO": "南充",
    "NGB": "宁波", "NKG": "南京", "NLH": "宁蒗", "NNG": "南宁", "NNY": "南阳", "NTG": "南通", "PZI": "攀枝花", "SYM": "普洱",
    "BAR": "琼海", "BPE": "秦皇岛", "HBQ": "祁连", "IQM": "且末", "IQN": "庆阳", "JIQ": "黔江", "JUZ": "衢州",
    "NDG": "齐齐哈尔", "TAO": "青岛", "RIZ": "日照", "RKZ": "日喀则", "RQA": "若羌", "HPG": "神农架", "QSZ": "莎车",
    "SHA": "上海", "SHE": "沈阳", "SHF": "石河子", "SJW": "石家庄", "SQD": "上饶", "SQJ": "三明", "SYX": "三亚",
    "SZX": "深圳", "WDS": "十堰", "WGN": "邵阳", "YSQ": "松原", "HYN": "台州", "RMQ": "台中", "TCG": "塔城", "TCZ": "腾冲",
    "TEN": "铜仁", "TGO": "通辽", "THQ": "天水", "TLQ": "吐鲁番", "TNH": "通化", "TNN": "台南", "TPE": "台北", "TSN": "天津",
    "TTT": "台东", "TVS": "唐山", "TYN": "太原", "YTY": "扬州", "DTU": "五大连池", "HLH": "乌兰浩特", "UCB": "乌兰察布",
    "URC": "乌鲁木齐", "WEF": "潍坊", "WEH": "威海", "WNH": "文山", "WNZ": "温州", "WUA": "乌海", "WUH": "武汉",
    "WUS": "武夷山", "WUX": "无锡", "WUZ": "梧州", "WXN": "万州", "WZQ": "乌拉特中旗", "WSK": "巫山", "ACX": "兴义",
    "GXH": "夏河", "HKG": "香港", "NLT": "新源", "SIA": "咸阳", "WUT": "忻州", "XAI": "信阳", "XFN": "襄阳", "XIC": "西昌",
    "XIL": "锡林浩特", "XMN": "厦门", "XNN": "西宁", "XUZ": "徐州", "ENY": "延安", "INC": "银川", "LDS": "伊春", "LLF": "永州",
    "UYN": "榆林", "YBP": "宜宾", "YCU": "运城", "YIC": "宜春", "YIH": "宜昌", "YIN": "伊宁", "YIW": "义乌", "YKH": "营口",
    "YNJ": "延吉", "YNT": "烟台", "YNZ": "盐城", "YUS": "玉树", "YYA": "岳阳", "CGO": "郑州", "DYG": "张家界", "HSN": "舟山",
    "NZL": "扎兰屯", "YZY": "张掖", "ZAT": "昭通", "ZHA": "湛江", "ZHY": "中卫", "ZQZ": "张家口", "ZUH": "珠海", "ZYI": "遵义"
}
if __name__ == '__main__':
    print('chinaexpressair')
    tickets = getChinaexpressairSpecialTickets()
    for ticket in tickets:
        print(ticket)
    # DepCodeList = getDepCodeList()
    # print(DepCodeList)

    """
    with open('./cityNameAbbr1.json', 'r', encoding='utf-8') as jf:
        data = json.load(jf)
    newData = {}
    for key, value in data.items():
        newData[value.upper()] = key
    with open('./cityNameAbbr2.json', 'w', encoding='utf-8') as jf:
        json.dump(newData, jf, ensure_ascii=False)
    """