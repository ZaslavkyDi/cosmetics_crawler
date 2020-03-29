# -*- coding: utf-8 -*-
import scrapy


class CosmeticComUaSpider(scrapy.Spider):
    name = 'cosmetic_com_ua'
    allowed_domains = ['cosmetic.com.ua']
    start_urls = ['http://cosmetic.com.ua/']

    def parse(self, response):
        pass
