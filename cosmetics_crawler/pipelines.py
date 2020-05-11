# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime

from cosmetics_crawler.items import CosmeticsCrawlerItem


class CosmeticsCrawlerPipeline(object):

    def process_item(self, item, spider):
        if not item or not isinstance(item, CosmeticsCrawlerItem):
            return item

        if not item.get('create_date'):
            item['create_date'] = datetime.utcnow()

        item['update_date'] = datetime.utcnow()
        item['site_name'] = spider.name
        return item

