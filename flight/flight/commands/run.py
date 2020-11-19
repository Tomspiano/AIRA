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
        parser.add_option('-i', '--info', metavar='FILE',
                          help='json file. for crawling')

    def process_options(self, args, opts):
        ScrapyCommand.process_options(self, args, opts)
        if opts.info:
            self.settings.set('REQUIRED_INFO', opts.info, priority='cmdline')
        else:
            raise UsageError('You MUST pass the information to start crawling')

    def run(self, args, opts):
        """ start crawling. """
        self.crawler_process.crawl('ctrip')
        self.crawler_process.start()

# 在AIRA/flight输入如下命令
# scrapy run -i json/file/path
# TODO(Tomspiano): 命令待测试
