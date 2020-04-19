# -*- coding: utf-8 -*-
import scrapy


class BcbrasilSpider(scrapy.Spider):
    name = 'bcbrasil'
    allowed_domains = ['www.bcb.gov.br/']
    start_urls = ['https://www.bcb.gov.br//']

    def parse(self, response):
         = response.css()
