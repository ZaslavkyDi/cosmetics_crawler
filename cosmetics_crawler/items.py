# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CosmeticsCrawlerItem(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()
    photo_url = scrapy.Field()
    breadcrumbs = scrapy.Field()
    description = scrapy.Field()
    price = scrapy.Field()
    availability = scrapy.Field()
    brand = scrapy.Field()
    attributes = scrapy.Field()
    rating = scrapy.Field()
    feedback = scrapy.Field()
    size = scrapy.Field()

    create_date = scrapy.Field()
    update_date = scrapy.Field()
    site_name = scrapy.Field()
