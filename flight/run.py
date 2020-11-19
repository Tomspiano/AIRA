# -*- coding: utf-8 -*-
"""
Created on 2020/11/17
@Author: 你们说的队
@Project: AIRA
@Product: PyCharm
@Description: 运行爬虫
"""


def crawler_runner():
    from twisted.internet import reactor
    from scrapy.crawler import CrawlerRunner
    from scrapy.utils.log import configure_logging

    from flight.spiders.ctrip_spider import CtripSpider

    configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
    runner = CrawlerRunner()

    d = runner.crawl(CtripSpider)
    d.addBoth(lambda _: reactor.stop())
    reactor.run()  # the script will block here until the crawling is finished


def crawler_process(spider_name):
    from scrapy.crawler import CrawlerProcess
    from scrapy.utils.project import get_project_settings

    process = CrawlerProcess(get_project_settings())

    process.crawl(spider_name)
    process.start()  # the script will block here until the crawling is finished


if __name__ == '__main__':
    # q = {
    #     'dcityname': '北京', 'dcity': 'bjs',
    #     'acities'  : {'阿尔山': 'yie', '毕节': 'bfj'},
    #     'date'     : '2020-12-1'}
    # crawler_process('ctrip', q)
    crawler_process('ctrip')
