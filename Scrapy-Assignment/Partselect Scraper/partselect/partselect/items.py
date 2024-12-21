# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PartselectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    price = scrapy.Field()
    title = scrapy.Field()
    manufacturer = scrapy.Field()
    description = scrapy.Field()
    partno = scrapy.Field()
    pass
