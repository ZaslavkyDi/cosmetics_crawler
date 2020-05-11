# -*- coding: utf-8 -*-
from typing import List, Union

import scrapy
from scrapy import Request

SCRAPED_CATEGORIES = [
    # 'dekorativnaya-kosmetika',
    'kosmetika-po-ukhodu',
]


class CosmeticComUaSpider(scrapy.Spider):
    name = 'cosmetic_com_ua'
    allowed_domains = ['cosmetic.com.ua']
    start_urls = ['http://cosmetic.com.ua']

    def start_requests(self):
        for category in SCRAPED_CATEGORIES:
            url = f'{self.start_urls[0]}/{category}'
            yield Request(url=url)

    def parse(self, response):
        product_listing_urls = response.xpath('//a[@class="fwd"]/@href').extract()
        for request in self.send_requests(product_listing_urls, self.parse_product_listing):
            yield request

    def parse_product_listing(self, response):
        product_urls = response.xpath('//div[@class="title"]/a/@href').extract()
        for request in self.send_requests(product_urls, self.parse_product):
            yield request

    def parse_product(self, response):
        breadcrumbs = response.xpath('//nav[@class="breadcrumbs"]//a//text()').extract()[1:]
        title = response.xpath('//h1//text()').extract_first()

        return {
            'breadcrumbs': breadcrumbs,
            'title': title,
        }

    def send_requests(self, urls: List[str], method_name) -> Union:
        for url in urls:
            if self.name not in url:
                url = f'{self.start_url}{url}'
                yield Request(url=url, callback=method_name)
