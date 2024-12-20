# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class QoutesItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()
    date = scrapy.Field()
    location = scrapy.Field()
    description = scrapy.Field()
