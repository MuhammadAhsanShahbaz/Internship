import re
import csv
import random

from scrapy import Spider, Request
from collections import OrderedDict


class GumtreeSpider(Spider):
    name = "gumtree"
    allowed_domains = ["www.gumtree.com"]
    start_urls = ["https://www.gumtree.com"]

    custom_settings = {
        'CONCURRENT_REQUESTS': 1,
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 0.2,
        'AUTOTHROTTLE_MAX_DELAY': 5,

        'RETRY_TIMES': 2,
        'RETRY_HTTP_CODES': [500, 502, 503, 504, 400, 403, 404, 408, 429],
    }

    def __init__(self, *args, **kwargs):
        super(GumtreeSpider, self).__init__(*args, **kwargs)
        self.file_name = 'output/final_output.csv'
        self.sort_list = ['date', 'price_lowest_first', 'price_highest_first', 'distance']
        self.distance = ['1', '3', '5', '10', '15', '30', '50', '75', '100']
        self.field_names = ['Name', 'Location', 'Price', 'Date Posted', 'Product URL', 'Image URL']
        self.visited_urls = self.get_visited_urls()
        self.proxy_urls = self.get_proxy_urls()

    def start_requests(self):
        # Choosing random proxy for each request
        yield Request(url=self.start_urls[0],
                      meta={'proxy': random.choice(self.proxy_urls)})

    def parse(self, response, **kwargs):
        names = response.css('.css-15qmqfw .e25keea16::attr(href)').getall()
        date = response.css('[data-q="tile-datePosted"]::text').getall()

        visited_urls = self.get_visited_urls()

        for i in range(len(date)):
            url = f'https://www.gumtree.com{names[i]}'
            posted_date = self.date_check(date[i])

            if url in visited_urls:
                print(url)
                continue

            if posted_date and url not in self.visited_urls:
                self.visited_urls.append(url)
                yield Request(url=url, callback=self.parse_detail,
                              meta={'date': posted_date, 'proxy':
                                  random.choice(self.proxy_urls)})

        for dis in self.distance:
            for sor in self.sort_list:
                for page in range(1, 51):
                    url = f'https://www.gumtree.com/search?search_category=bicycles&search_location=uk&page={page}&distance={dis}&sort={sor}'
                    yield Request(url=url, callback=self.parse,
                                  meta={'proxy': random.choice(self.proxy_urls)})

    def parse_detail(self, response):
        items = OrderedDict()

        items['Name'] = self.data_tag(response, 'vip-title')
        items['Location'] = self.data_tag(response, 'ad-location')
        items['Price'] = self.data_tag(response, 'ad-price')
        items['Image URL'] = response.css('[data-testid="carousel"] img::attr(src)').getall()
        items['Product URL'] = response.url
        items['Date Posted'] = response.meta.get('date')

        self.write_csv(items)

        yield items

    def date_check(self, date):
        if 'just now' in date:
            return date

        elif 'min' in date:
            return date

        elif 'day' in date:
            number = int(''.join(re.findall(r'\d+', date)))

            if number < 30:
                return date

            return ''

    def data_tag(self, response, name):
        text = response.css(f'[data-q="{name}"]::text').get('').strip()
        return text

    def get_visited_urls(self):
        urls = []
        try:
            with open(self.file_name, 'r', encoding='utf-8') as csvfile:
                rows = csv.reader(csvfile)

                for row in rows:
                    urls.append(row[4])

                return list(set(urls))

        except FileNotFoundError:
            return []

    def write_csv(self, data):
        with open(self.file_name, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.field_names)

            if csvfile.tell() == 0:
                writer.writeheader()

            data = dict(data)
            writer.writerow(data)

    def get_proxy_urls(self):
        with open('Webshare 10 proxies.txt', 'r') as file:
            read = file.readlines()
            proxy_urls = []

            for proxy in read:
                parts = proxy.strip('\n').split(':')
                proxy_urls.append(f'http://{parts[2]}:{parts[3]}@{parts[0]}:{parts[1]}')

            return proxy_urls