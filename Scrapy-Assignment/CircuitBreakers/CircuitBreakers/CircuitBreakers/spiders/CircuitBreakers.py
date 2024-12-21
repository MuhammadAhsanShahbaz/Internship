from scrapy import Request, Spider
from ..items import CircuitbreakersItem


class CircuitBreakers(Spider):
    name = 'CircuitBreakers'
    start_urls = ['https://ktcables.com.au/']

    def start_requests(self):
        yield Request(url=self.start_urls[0],
                      callback=self.parse)

    def parse(self, response, **kwargs):
        products = response.css(".navbar__category-col a::attr(href)").extract()

        for product in products:
            next_pages = 'https://ktcables.com.au' + str(product)
            yield Request(url=next_pages,
                          callback=self.parse_product)

    def parse_product(self, response):
        all_div = response.css(".woocommerce-loop-product__link::attr(href)").getall()

        next_pages = response.css('ul .page-numbers::attr(href)').get('')

        for product_url in all_div:
            items = CircuitbreakersItem()

            items['href'] = product_url

            yield Request(url=product_url,
                          callback=self.detail_scrap,
                          meta={'items': items})

        # Pagination for all pages
        for next_page in next_pages:
            yield Request(next_page, callback=self.parse_product)


    def detail_scrap(self, response):
        items = response.meta['items']

        items['categories'] = response.css("span a::text").extract_first()
        items['image'] = response.css("a .wp-post-image::attr(src)").extract_first()
        items['sku'] = response.css("span span::text").get()
        items['description'] = response.css(".panel-body p::text").get()

        yield items
