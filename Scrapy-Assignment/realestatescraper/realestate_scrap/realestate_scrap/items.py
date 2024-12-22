# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RealestateScrapItem(scrapy.Item):
    Address = scrapy.Field()
    Price = scrapy.Field()
    Bed = scrapy.Field()
    Bath = scrapy.Field()
    Area = scrapy.Field()
    CarSpaces = scrapy.Field()
    Specification = scrapy.Field()
    Agent1Name = scrapy.Field()
    Agent1Number = scrapy.Field()
    Agent2Name = scrapy.Field()
    Agent2Number = scrapy.Field()
    PropertyId = scrapy.Field()
    Pictures = scrapy.Field()
    Url = scrapy.Field()
