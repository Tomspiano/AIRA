# -*- coding: utf-8 -*-
"""
Created on 2020/11/17
@Author: 你们说的队
@Project: AIRA
@Product: PyCharm
@Description: 运行爬虫
"""
import scrapy.commands.crawl as crawl
from scrapy.exceptions import UsageError
from scrapy.commands import ScrapyCommand


class Command(crawl.Command):
    def add_options(self, parser):
        ScrapyCommand.add_options(self, parser)
        parser.add_option('-d', '--date', help='departure date, like 2020-12-01')
        parser.add_option('-c', '--dcity', help='departure city, like 福州')

    def process_options(self, args, opts):
        ScrapyCommand.process_options(self, args, opts)

        if opts.date and opts.dcity:
            self.settings.set('REQUEST_ENABLED', True, priority='cmdline')
            # self.settings.set('DATE', opts.date, priority='cmdline')
            # self.settings.set('ACITY', opts.dcity, priority='cmdline')

        else:
            self.settings.set('REQUEST_ENABLED', False, priority='cmdline')

    def run(self, args, opts):
        """ start crawling. """
        self.crawler_process.crawl('ctrip', **opts.__dict__)
        self.crawler_process.start()

# 在AIRA/flight输入如下命令
# scrapy run -d 2020-12-12 -c 福州
