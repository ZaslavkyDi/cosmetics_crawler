# -*- coding: utf-8 -*-
from typing import List, Union, Dict, Any

import scrapy
from scrapy import Request

from constants import ItemAvailabilityStatus
from cosmetics_crawler.items import CosmeticsCrawlerItem

SCRAPED_CATEGORIES = [
    'kosmetika-po-ukhodu',
]


class CosmeticComUaSpider(scrapy.Spider):
    name = 'cosmetic_com_ua'
    allowed_domains = ['cosmetic.com.ua']
    start_urls = ['http://cosmetic.com.ua']
    main_url = 'http://cosmetic.com.ua'

    def start_requests(self):
        for category in SCRAPED_CATEGORIES:
            url = f'{self.main_url}/{category}'
            yield Request(url=url)

    def parse(self, response):
        product_listing_urls = response.xpath('//a[@class="fwd"]/@href').extract()[:1] #TODO remove afte creating a database
        for request in self.send_requests(product_listing_urls, self.parse_product_listing):
            yield request

    def parse_product_listing(self, response):
        product_urls = response.xpath('//div[@class="title"]/a/@href').extract()
        for request in self.send_requests(product_urls, self.parse_product):
            yield request

    def parse_product(self, response) -> CosmeticsCrawlerItem:
        item = CosmeticsCrawlerItem()

        item['url'] = response.url
        item['name'] = response.xpath('//h1//text()').extract_first()
        item['photo_url'] = self.parse_photo_url(response)
        item['breadcrumbs'] = ', '.join(response.xpath('//nav[@class="breadcrumbs"]//a//text()').extract()[1:])
        item['description'] = self.parse_description(response)
        item['price'] = self.parse_price(response)
        item['availability'] = self.parse_availability(response)
        item['size'] = self.parse_size(response)
        item['rating'] = response.xpath('//div[@class="rating"]//meta[@itemprop="ratingValue"]/@content').extract_first()
        item['feedback'] = response.xpath('//div[@class="rating"]//meta[@itemprop="reviewCount"]/@content').extract_first()

        attributes = self.parse_attributes(response)
        item['attributes'] = attributes
        item['brand'] = attributes.get('Бренд:')

        return item

    def parse_photo_url(self, response) -> Union[str, None]:
        photo_src = response.xpath('//div[@class="screen"]/img/@src').extract_first()
        if not photo_src:
            return None

        return self.main_url + photo_src

    def parse_description(self, response) -> Union[str, None]:
        description = response.xpath('//div[@class="product-description"]//text()').extract()
        if not description:
            return None

        return ', '.join(description)

    def parse_price(self, response) -> Union[int, None]:
        price = response.xpath('//div[@class="price" or @class="price discount"]//text()').extract_first()
        if not price:
            return None

        return int(price.replace('&nbsp;', '').replace('грн', '').strip())

    def parse_availability(self, response) -> str:
        availability = response.xpath('//div[@class="status"]/text()').extract_first()
        if not availability:
            return ItemAvailabilityStatus.UNKNOWN

        if availability == 'Есть в наличии':
            return ItemAvailabilityStatus.AVAILABLE
        else:
            return ItemAvailabilityStatus.NOT_AVAILABLE

    def parse_attributes(self, response) -> Dict[str, Any]:
        attrs = {}
        attrs_vals = response.xpath('//div[@class="attributes"]/table//tr')

        for attr in attrs_vals:
            key = attr.xpath('./td[@class="name"]//text()').extract_first()
            if not key:
                continue
            value = attr.xpath('./td[@class="attribute"]//text()').extract_first()
            attrs[key] = value

        return attrs

    def parse_size(self, response) -> Union[str, None]:
        size_value = response.xpath('//div[@class="f-left label"]/div[@class="select-like"]/text()').extract_first()
        if size_value:
            return size_value

        size_value = response.xpath('//div[@class="f-left label"]/select/option/text()').extract()
        if not size_value:
            return None

        clear_size_values = [size.strip('\n').strip() for size in size_value]
        return ', '.join(clear_size_values)

    def send_requests(self, urls: List[str], method_name) -> Union:
        for url in urls:
            if self.name not in url:
                url = f'{self.main_url}{url}'
                yield Request(url=url, callback=method_name)
