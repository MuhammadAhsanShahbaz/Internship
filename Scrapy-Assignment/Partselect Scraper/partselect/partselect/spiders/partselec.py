from scrapy import Spider, Request
from scrapy.http import FormRequest

from ..items import PartselectItem


class PartselecSpider(Spider):
    name = "partselec"
    allowed_domains = ["www.partselect.com"]
    start_urls = ["https://www.partselect.com/"]

    def parse(self, response):
        with open('part_numbers.txt', 'r') as f:
            read = f.readlines()

            for r in read:
                a = r.strip()
                url = f'http://www.partselect.com/api/search/?searchterm={a}'
                yield Request(url=url, callback=self.start_scraping,
                              meta={'proxy': 'https://proxy.scrapeops.io/v1/'},
                              headers={'api_key': ''})

    def start_scraping(self, response):
        items = PartselectItem()

        items['price'] = response.css('.js-partPrice::text').get()
        items['title'] = response.css('.title-lg::text').get()
        items['manufacturer'] = response.css('.text-teal span::text').get()
        items['description'] = response.css('.pd__description div::text').get()
        items['partno'] = response.css('.js-qnaResponse div +.bold::text').extract()

        yield items

