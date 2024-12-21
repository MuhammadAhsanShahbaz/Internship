# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CircuitbreakersItem(scrapy.Item):
    # define the fields for your item here like:
    href = scrapy.Field()
    image = scrapy.Field()
    sku = scrapy.Field()
    description = scrapy.Field()
    categories = scrapy.Field()
