# -*- coding: utf-8 -*-
"""
Created on 2020/12/13
@Author: 你们说的队
@Project: AIRA
@Product: PyCharm
@Description: 成都航空特价机票
"""
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
from pkg.items import Discount
import re
import json

WAIT = 60
path = 'data'


def save(data):
    with open(f'{path}/cdal.json', 'w', encoding='utf-8') as f:
        json.dump(data.__dict__, f, ensure_ascii=False)

def get_ua():
    ua = UserAgent()
    return ua.random

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument(get_ua())
    options.add_argument('--headless')
    return webdriver.Chrome(options=options)

if __name__ == '__main__':
    driver = setup_driver()
    driver.get('https://www.cdal.com.cn/')
    # 点击“查看更多”
    more = WebDriverWait(driver, WAIT).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="allBody"]/div/div[7]/div[4]/div[2]/a')))
    more.click()
    # 获取特价机票信息
    WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH, '//*[@id="initCity"]')))
    for option in driver.find_elements_by_xpath('//*[@id="initCity"]/option'):
        # 查询
        option.click()
        q = WebDriverWait(driver, WAIT).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="allBody"]/div/div[6]/div[1]/div[1]/div/div[3]/a')))
        q.click()
        WebDriverWait(driver, WAIT).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="loadMoreChange"]')))
        driver.find_element_by_xpath('//*[@id="loadMoreChange"]').click()
        WebDriverWait(driver, WAIT).until(
                EC.visibility_of_all_elements_located((By.XPATH, '//*[@id="lowPrice"]/div')))
        # 获取信息
        item = Discount()
        item.companyName = '成都航空'
        for ticket in driver.find_elements_by_xpath('//*[@id="lowPrice"]/div'):
            locations = ticket.find_element_by_xpath('./a/div[1]/p[1]').text.split('－')
            item.acityName = locations[0]
            item.dcityName = locations[1]
            item.departureDate = ticket.find_element_by_xpath('./a/div[1]/p[2]').text
            item.price = eval(ticket.find_element_by_xpath('./a/div[2]/p[1]').text[1:])
            item.rate = eval(re.search(r'(?<=最低价).+(?=折)', ticket.find_element_by_xpath('./a/div[2]/p[2]').text)[0])
            save(item) # 在这里断点！实际上只能保存一条数据！
