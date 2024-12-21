from typing import Any

import scrapy
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser

from ..items import QoutesItem


class Qoutespider(scrapy.Spider):
    name = 'quotes'
    start_urls = [
        'https://quotes.toscrape.com/login'
    ]
    page = 2

    def parse(self, response):

        token = response.css('form input::attr(value)').extract_first()
        return FormRequest.from_response(response, formdata={
            'csrf_token': token,
            'username': 'jackson',
            'password': 'asdfhkasj'
        }, callback=self.start_scraping)

    def start_scraping(self, response):
        #open_in_browser(response)


        all_div = response.css('div.quote')

        self.logger.info("Parse function called on %s", response.url)

        for q in all_div:
            items = QoutesItem()

            title = q.css('span.text::text').get()
            author = q.css('.author::text').get()
            tags = q.css('.tag::text').get()
            href = q.css("span a::attr(href)").extract_first()
            print(href)

            about_page = 'https://quotes.toscrape.com' + str(href) + '/'

            items['title'] = title
            items['author'] = author
            items['tags'] = tags

            yield response.follow(about_page, callback=self.scrap_about,
                                  meta={'items': items}, dont_filter=True)

        next_page = 'https://quotes.toscrape.com/page/' + str(Qoutespider.page) + '/'

        if self.page <= 11:
            Qoutespider.page += 1
            yield response.follow(next_page, callback=self.start_scraping)

    def scrap_about(self, response):

        items = response.meta['items']
        date = response.css(".author-born-date::text").get()
        location = response.css(".author-born-location::text").get()
        description = response.css(".author-description::text").get()

        items['date'] = date
        items['location'] = location
        items['description'] = description

        yield items
