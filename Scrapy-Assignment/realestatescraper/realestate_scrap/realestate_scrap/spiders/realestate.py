import re


from datetime import datetime
from scrapy import Spider, Request
from collections import OrderedDict


class RealestateSpider(Spider):
    name = "realestate"
    allowed_domains = ["www.realestate.com.au"]
    start_urls = ["https://www.realestate.com.au/"]

    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': f'output/Results {datetime.now().strftime("%d%m%Y%H%M%S")}.csv',
        'FEED_EXPORT_FIELDS': ['Address', 'Price', 'Bed', 'Bath', 'Area', 'CarSpaces', 'Specification', 'Agent1 Name', 'Agent1 Number', 'Agent2 Name', 'Agent2 Number', 'PropertyId', 'image_urls', 'Url']
    }

    cookies = {
        'reauid': 'afec655f83f80000efe820660e020000472d4f00',
        'Country': 'FR',
        'KP_UIDz-ssn': '0AZbMn3u4Hlkp3UIvwcqUzaIudABoXbhUMwDvnjYyDnl8gQCq9hg5UEXXV64CwkW1xJZjBNtXjnBR3MirpqWeMbYf5DcqCDXLqrjmGebyl5ys1V2H3R954YEYcPkpl6Eqz09wQDnl13muAviXSJACD61O66z4JtPoCOItxuv',
        'KP_UIDz': '0AZbMn3u4Hlkp3UIvwcqUzaIudABoXbhUMwDvnjYyDnl8gQCq9hg5UEXXV64CwkW1xJZjBNtXjnBR3MirpqWeMbYf5DcqCDXLqrjmGebyl5ys1V2H3R954YEYcPkpl6Eqz09wQDnl13muAviXSJACD61O66z4JtPoCOItxuv',
        'split_audience': 'c',
        'fullstory_audience_split': 'B',
        's_nr30': '1713432891718-New',
        'utag_main': 'v_id:018ef08f01eb0014db1ada5293cc0506f001e06700978$_sn:1$_se:2$_ss:0$_st:1713434689630$ses_id:1713432887787%3Bexp-session$_pn:1%3Bexp-session$vapi_domain:realestate.com.au$_prevpage:undefined%3Bexp-1713436491725',
        's_ecid': 'MCMID%7C37523326437610805253636180700580951928',
        'AMCVS_341225BE55BBF7E17F000101%40AdobeOrg': '1',
        'AMCV_341225BE55BBF7E17F000101%40AdobeOrg': '-330454231%7CMCIDTS%7C19832%7CMCMID%7C37523326437610805253636180700580951928%7CMCAID%7CNONE%7CMCOPTOUT-1713440092s%7CNONE%7CMCAAMLH-1714037693%7C6%7CMCAAMB-1714037693%7Cj8Odv6LonN4r3an7LhD3WZrU1bUpAkFkkiY1ncBR96t2PTI%7CvVersion%7C3.1.2',
        's_cc': 'true',
        's_sq': 'rea-live%3D%2526c.%2526a.%2526activitymap.%2526page%253Drea%25253Ahomepage%2526link%253Drealestate.com.au%252520homepage%2526region%253Dargonaut-wrapper%2526pageIDType%253D1%2526.activitymap%2526.a%2526.c%2526pid%253Drea%25253Ahomepage%2526pidt%253D1%2526oid%253Dhttps%25253A%25252F%25252Fwww.realestate.com.au%25252F%2526ot%253DA',
    }

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'referer': 'https://www.realestate.com.au/',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    }

    def start_requests(self):
        yield Request(url=self.start_urls[0], headers=self.headers,
                      cookies=self.cookies)

    def parse(self, response, **kwargs):
        addresses = self.get_address_from_file()

        for address in addresses:
            url = f'https://www.realestate.com.au/buy/in-{address}/list-1?activeSort=relevance'
            yield Request(url, headers=self.headers,
                           cookies=self.cookies, callback=self.paggination)

    def paggination(self, response):
        names = response.css('.details-link::attr(href)').getall()

        for name in names:
            url = f'https://www.realestate.com.au{name}'
            yield Request(url, headers=self.headers,
                          cookies=self.cookies, callback=self.parse_data)

        next_url = response.css('.styles__Arrow-sc-1ciwyuo-0 a::attr(href)').get()

        if next_url:
            url = f'https://www.realestate.com.au{next_url}'
            yield Request(url, headers=self.headers,
                          cookies=self.cookies, callback=self.paggination)

    def parse_data(self, response):
        items = OrderedDict()

        items['Url'] = response.url
        items['Bed'] = self.get_value('bedroom', response )
        items['Bath'] = self.get_value('bathroom', response)
        items['Area'] = self.get_value('size', response)
        items['CarSpaces'] = self.get_value('parking space', response)
        items['Specification'] = response.css('.property-description__content::text').getall()
        items['PropertyId'] = self.get_property(response)
        items['Price'] = self.get_price(response)
        items['image_urls'] = self.get_pictures(response)
        items = self.get_adress(response, items)
        items = self.get_agents(response, items)

        yield items

    def get_address_from_file(self):
        with open('input/address.txt', 'r') as txt_file:
            return [line.strip() for line in txt_file.readlines() if line.strip()]

    def get_price(self, response):
        price = (response.css('.Text__Typography-sc-vzn7fr-0 strong::text').get('')
                 or response.css('.property-price::text').get('')
                 or response.css('.project-overview__price-range::text').get(''))

        if price == 'Contact Agent':
            price = ''

        return price

    def get_adress(self, response, items):
        address = response.css('.property-info-address::text').get('')

        if address == '':
            address = response.css('.project-overview__address::text').get('')
            items['Price'] = response.css('.project-overview__price-range::text').get('')
            items['Agent1 Number'] = response.css('.phone__number-text::text').get('')
            items['Agent1 Name'] = items['Agent2 Name'] = items['Agent1 Number'] = ''

        items['Address'] = address
        return items

    def get_pictures(self, response):
        image_urls = []
        script_content = response.css('script:contains("https://i2.au")::text').get('')

        if script_content:
            urls = re.findall(r'/{size}/([a-fA-F0-9]+)', script_content)

            for url in urls[1:6]:
                picture_url = f'https://i2.au.reastatic.net/800x600-resize,extend,r=33,g=40,b=46/{url}/image.jpg'
                image_urls.append(picture_url)

           # self.download_images(pictures)

        return image_urls

    def download_images(self, urls):
        for url in urls:
            yield Request(url=url, headers=self.headers,
                          cookies=self.cookies)

    def get_property(self, response):
        property = response.css('.dlyvPZ::text').re_first(r'\d+')
        return property

    def get_agents(self, response, items):
        names = response.css('.layout__sidebar-primary .agent-info__name::text').getall()
        numbers = response.css('.layout__sidebar-primary .phone ::attr(href)').re(r'\d+')
        agent_info = dict(zip(names, numbers))

        for i, (name, number) in enumerate(agent_info.items(), start=1):
            items[f'Agent{i} Name'] = name
            items[f'Agent{i} Number'] = number

        return items

    def get_area(self, value):
        value = self.get_number(value)
        return value + 'm²' if value != '' else value

    def get_value(self, name, response):
        value = response.css(f'[aria-label*="{name}"] ::attr(aria-label)').get('')

        if name == 'size':
            return self.get_area(value)

        return self.get_number(value)

    def get_number(self, number):
        if number != '':
            number = ''.join(re.findall(r'\d+', number))
            return number

        return ''
