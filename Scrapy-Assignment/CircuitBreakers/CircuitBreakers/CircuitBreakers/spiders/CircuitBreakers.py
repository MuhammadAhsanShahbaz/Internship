import scrapy
from scrapy import Request, Spider
from scrapy.http import FormRequest
from ..items import CircuitbreakersItem
from scrapy.utils.response import open_in_browser

class CircuitBreakers(Spider):
    name = 'CircuitBreakers'
    start_urls = [
        'https://ktcables.com.au/'
    ]

    def parse(self, response):

        product = response.css(".navbar__category-col a::attr(href)").extract()

        for p in product:

            next_pages = 'https://ktcables.com.au' + str(p)
            yield Request(next_pages, callback=self.parse_product)

    def parse_product(self, response):
        #self.logger.info("Parse function called on %s", response.url)

        all_div = response.css(".woocommerce-loop-product__link::attr(href)").extract()

        next_pages = response.css('ul .page-numbers::attr(href)').extract()

        for href in all_div:

            items = CircuitbreakersItem()
            items['href'] = href
            yield Request(href, callback=self.detail_scrap, meta={'items': items})

        for next_page in next_pages:
            yield Request(next_page, callback=self.parse_product)


    def detail_scrap(self, response):

        #self.logger.info("Parse function called on %s", response.url)

        items = response.meta['items']
        items['categories'] = response.css("span a::text").extract_first()
        items['image'] = response.css("a .wp-post-image::attr(src)").extract_first()
        items['sku'] = response.css("span span::text").get()
        items['description'] = response.css(".panel-body p::text").get()
        yield items
