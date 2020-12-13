# -*- coding: utf-8 -*-
"""
Created on 2020/12/13
@Author: 你们说的队
@Project: AIRA
@Product: PyCharm
@Description: 常用函数
"""
from selenium import webdriver
from fake_useragent import UserAgent
import json


def save(data, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data.__dict__, f, ensure_ascii=False)


def get_ua():
    ua = UserAgent()
    return ua.random


def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument(get_ua())
    options.add_argument('--headless')
    return webdriver.Chrome(options=options)
