from scrapy import Request, Spider
from ..items import FourbyItem


class Fourby(Spider):
    name = 'Fourby'

    headers = {
        'authority': 'www.4x4modsaustralia.com.au',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    }

    start_urls = [
        'https://www.4x4modsaustralia.com.au',
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, callback=self.parse)

    def parse(self, response, **kwargs):
        ul_element = response.css('ul.dropdown-menu#pf1-items')

        li_elements = ul_element.css('li')

        for li in li_elements:
            li_content = li.css('::text').extract_first().strip()
            yield {
                'li_content': li_content
            }