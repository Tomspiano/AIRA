# -*- coding: utf-8 -*-
"""
Created on 2020/12/13
@Author: 你们说的队
@Project: AIRA
@Product: PyCharm
@Description: 西藏航空特价机票
"""
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pkg.items import Discount
from pkg import tools as tl
import re

WAIT = 60
path = 'data'

if __name__ == '__main__':
    driver = tl.setup_driver()
    driver.get('http://www.tibetairlines.com.cn/')
    # 点击“查看更多”
    more = WebDriverWait(driver, WAIT).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="allBody"]/div/div[5]/div[3]/div[2]/div[2]/div/div/a')))
    more.click()
    # 获取特价机票信息
    WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH, '//*[@id="initCity"]')))
    for option in driver.find_elements_by_xpath('//*[@id="initCity"]/option'):
        # 查询
        option.click()
        q = WebDriverWait(driver, WAIT).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="allBody"]/div/div[5]/div[1]/div[1]/div/div[3]/a')))
        q.click()
        WebDriverWait(driver, WAIT).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="loadMoreChange"]')))
        driver.find_element_by_xpath('//*[@id="loadMoreChange"]').click()
        WebDriverWait(driver, WAIT).until(
                EC.visibility_of_all_elements_located((By.XPATH, '//*[@id="lowPrice"]/div')))
        # 获取信息
        item = Discount()
        item.companyName = '西藏航空'
        for ticket in driver.find_elements_by_xpath('//*[@id="lowPrice"]/div'):
            locations = ticket.find_element_by_xpath('./a/div[1]/p[1]').text.split('－')
            item.acityName = locations[0]
            item.dcityName = locations[1]
            item.departureDate = ticket.find_element_by_xpath('./a/div[1]/p[2]').text
            item.price = eval(ticket.find_element_by_xpath('./a/div[2]/p[1]').text[1:])
            item.rate = eval(re.search(r'(?<=最低价).+(?=折)', ticket.find_element_by_xpath('./a/div[2]/p[2]').text)[0])
            tl.save(item, f'{path}/tibetairlines.json')  # 在这里断点！实际上只能保存一条数据！
