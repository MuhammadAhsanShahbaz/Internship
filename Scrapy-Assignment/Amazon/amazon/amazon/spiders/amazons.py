import re
import requests
from collections import OrderedDict

from scrapy import Request, Spider


class AmazonsSpider(Spider):
    name = "amazons"
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'device-memory': '8',
        'downlink': '0.45',
        'dpr': '1.25',
        'ect': '3g',
        'priority': 'u=0, i',
        'rtt': '1300',
        'sec-ch-device-memory': '8',
        'sec-ch-dpr': '1.25',
        'sec-ch-ua': '"Opera GX";v="111", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"15.0.0"',
        'sec-ch-viewport-width': '1536',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 OPR/111.0.0.0',
        'viewport-width': '1536',
    }
    start_urls = ['https://www.amazon.com/dp/B0CCM6K3HY?th=1']

    def start_requests(self):
        yield Request(self.start_urls[0], headers=self.headers,
                      callback=self.parse_data)

    def parse(self, response, **kwargs):
        page_no = int(response.css('.s-pagination-disabled::text').extract()[1])
        for p in range(1, page_no + 1):
            url = ('https://www.amazon.com/s?k=booka&i=stripbooks-intl-ship&page='
                   + str(p)
                   + '&crid=5OHRM1485BCW&qid=1710946091&sprefix=book%2Cstripbooks-intl-ship%2C474&ref=sr_pg_2')
            yield Request(url, headers=self.headers,
                          cookies=self.cookies, callback=self.parse_page)

    def parse_page(self, response):
        links = response.css('.a-size-mini .s-underline-link-text::attr(href)').extract()
        for url in links:
            if not url.startswith('https://aax-us-iad.amazon'):
                detail_page = ('https://www.amazon.com'
                               + str(url))
                yield Request(detail_page, headers=self.headers,
                              cookies=self.cookies, callback=self.parse_data)

    def parse_data(self, response):
        items = OrderedDict()
        items['title'] = response.css('#productTitle::text').get('').strip()
        items['price'] = ' - '.join(set(response.css('[data-a-color="price"] span ::text').getall()))
        # items['detail'] = response.css('.a-expander-partial-collapse-content span::text').get()
        list1 = response.css('.a-profile-name::text').extract()
        list2 = response.css('.reviewText span::text').extract()
        items['review'] = list(zip(list1[1:4], list2[:3]))
        # items['ISBN'] = response.css('.a-text-bold:contains("ISBN-13") +span::text').get()
        items['Rating'] = (response.css('[data-csa-c-type="widget"] a span:contains(".") ::text')
                           .re_first(r"\d+\.\d+") or '')
        items['Number of Votes'] = response.css('#acrCustomerReviewText:contains("rat") ::text').re_first(r"\d+\,?\d+") or ''
        items['Size Name'] = response.css('[data-csa-c-content-id="dropdown_selected_size_name"] span::text').get('')
        items['Color Name'] = response.css('#variation_color_name .selection ::text').get('').strip()

        item_names = response.css('.a-expander-partial-collapse-content .a-col-left span span ::text').getall() or response.css('td .a-text-bold ::text').getall()
        item_values = response.css('.a-expander-partial-collapse-content .a-col-right span span ::text').getall() or response.css('td .po-break-word::text').getall()

        for item_name, item_value in zip(item_names, item_values):
            items[f'{item_name}'] = item_value

        items['About'] = (', '.join(text.strip() for text in response.css('.a-expander-partial-collapse-content ul '
                                                                          '::text')
                                    .getall() if text).replace(', ,', '\n').strip())

        a = [text.replace(' ', '') for text in response.css('#detailBullets_feature_div li .a-text-bold ::text').re
        (r"[a-zA-Z0-9 ]+") if text and text.strip()]

        yield items
