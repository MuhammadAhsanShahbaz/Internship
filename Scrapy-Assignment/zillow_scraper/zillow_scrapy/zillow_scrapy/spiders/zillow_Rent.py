import csv
import json
import re

from scrapy import Spider, Request
from collections import OrderedDict


class ZillowRentSpider(Spider):
    name = "zillow_Rent"
    allowed_domains = ["www.zillow.com"]
    start_urls = ["https://www.zillow.com"]

    headers = {
        'authority': 'www.zillow.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'origin': 'https://www.zillow.com',
        'referer': 'https://www.zillow.com',
        'sec-ch-ua': '"Not A(Brand";v="99", "Opera GX";v="107", "Chromium";v="121"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/107.0.0.0',
    }

    def __init__(self, *args, **kwargs):
        super(ZillowRentSpider, self).__init__(*args, **kwargs)
        self.input_file_name = 'input/zip_codes.csv'
        self.file_name = 'output/rent.csv'
        self.zillow_type = 'rentals'
        self.input_rows = self.get_urlsfromfile()
        self.visited_urls = self.get_visited_urls()
        self.location = {}
        self.field_names = ['URL', 'Full Address', 'Type', 'Images', 'Beds', 'Baths', 'Sq Ft', 'Price', 'Latitude',
                            'Longitude', 'City', 'Street', 'State', 'Zip Code', 'Year Built', 'Style',
                            'Lot', 'Agent Name', 'Agent Phone', 'Agent Email', 'Broker Name', 'MLS', 'Tax',
                            'Availability Date']

    def start_requests(self):
        yield Request(url=self.start_urls[0], headers=self.headers)

    def parse(self, response):
        for row in self.input_rows:
            state = row.get("State", '')
            zip_code = row.get("Zip", '')
            url = f'https://www.zillow.com/{state}-{zip_code}/{self.zillow_type}/'

            yield Request(url=url, callback=self.get_pin_location,
                          headers=self.headers)

    def parse_urls(self, response):
        detail_urls = []
        # url = response.json().get('cat1', {}).get('searchResults', {}).get('mapResults', [])
        url = response.json().get('cat1', {}).get('searchResults', {}).get('listResults', [])

        for url_no in range(len(url)):
            detail_urls.append(url[url_no].get('detailUrl', ''))

        print(len(detail_urls))

        for url in detail_urls:
            if self.fix_url(url) in self.visited_urls:
                print(url)
                continue

            self.visited_urls.append(self.fix_url(url))

            yield Request(url=self.fix_url(url), callback=self.parse_detail,
                          headers=self.headers)

        next_url = response.json().get('cat1', {}).get('searchList', {}).get('pagination', {})

        if next_url:
            next_url = next_url.get('nextUrl', '')

            if next_url:
                page = re.search(r'(\d+)_p', next_url).group(1)
                form_data = self.get_form_data(page)
                #
                # yield Request(url='https://www.zillow.com/async-create-search-page-state',
                #         method='PUT',
                #         body=json.dumps(form_data),
                #         callback=self.parse_urls,
                #         headers=self.headers
                #               )

                yield self.get_pull_request_for_urls(form_data)

    def parse_detail(self, response):
        data_dict = self.get_json(response)
        items = OrderedDict()
        items['URL'] = response.url
        items['Full Address'] = self.get_address(response)
        items['Images'] = self.get_images(data_dict)
        items['Type'] = self.find_data(data_dict, 'homeType')
        items['Price'] = self.find_data(data_dict, 'price')
        items['Latitude'] = self.find_data(data_dict, 'latitude')
        items['Longitude'] = self.find_data(data_dict, 'longitude')
        items['City'] = self.find_data(data_dict, 'city')
        items['Street'] = self.find_data(data_dict, 'streetAddress')
        items['State'] = self.find_data(data_dict, 'state')
        items['Zip Code'] = self.find_data(data_dict, 'zipcode')
        items['Style'] = self.find_data(data_dict, 'propertyTypeDimension')
        items['Year Built'] = self.find_data(data_dict, 'yearBuilt')
        items['Beds'] = self.find_data(data_dict, 'bedrooms')
        items['Sq Ft'] = self.find_data(data_dict, 'livingArea')
        items['Baths'] = self.find_data(data_dict, 'bathrooms')

        items['Lot'] = self.find_fact(data_dict, 'Lot')
        items['Availability Date'] = self.find_fact(data_dict, 'available')

        items['Tax'] = self.get_tax(data_dict)

        items['Agent Name'] = self.find_agent(data_dict, 'agentName')
        items['Agent Phone'] = self.find_agent(data_dict, 'agentPhoneNumber')
        items['Agent Email'] = self.find_agent(data_dict, 'agentEmail')
        items['Broker Name'] = self.find_agent(data_dict, 'brokerName')
        items['MLS'] = self.find_agent(data_dict, 'mlsId')
        items['Sold Date'] = self.get_date(data_dict)

        self.write_csv(items)
        yield items

    def get_urlsfromfile(self):
        try:
            with open(self.input_file_name, 'r', encoding='utf-8') as csvfile:
                return list(csv.DictReader(csvfile))

        except FileNotFoundError:
            return []

    def find_data(self, data_dict, place):
        if isinstance(data_dict, dict):
            temp = data_dict
            data_dict = data_dict[(list(data_dict.keys())[0])]

            if data_dict is False:
                if place == 'homeType':
                    place = 'homeTypes'
                    temp = temp.get('initialReduxState', {}).get('gdp', {}).get('building', {}).get(place)

                    if isinstance(temp, list):
                        temp = temp[0]

                    return temp

                else:
                    data = temp.get('initialReduxState', {}).get('gdp', {}).get('building', {})
                    temp = data.get('ungroupedUnits', {})

                    if temp is None:
                        try:
                            return data.get(place)

                        except TypeError:
                            try:
                                temp = data.get('floorPlans', {})[0].get('units', {})[0].get(place)

                            except TypeError:
                                temp = data.get('floorPlans', {})[0].get('minPrice', {})

                            except KeyError:
                                return ''

                        except KeyError:
                            try:
                                temp = data.get('comps').get('compBuildings', {})[0].get(place)

                            except KeyError:
                                try:
                                    temp = data.get(place)

                                except KeyError:
                                    if place == 'price':
                                        return data.get('floorPlans', {})[0].get('minPrice', {})

                            except TypeError:
                                try:
                                    temp = data.get(place)

                                except KeyError:
                                    if place == 'propertyTypeDimension':
                                        return ''

                if place == 'bedrooms':
                    place = 'beds'

                if place == 'bathrooms':
                    place = 'baths'

                if isinstance(temp, list):
                    try:
                        temp = temp[0].get(place)

                    except KeyError:
                        try:
                            temp = temp.get(place)

                        except TypeError:
                            try:
                                temp = data.get(place)

                            except KeyError:
                                return ''

                if not temp:
                    temp = data.get(place)

                return temp

        data_dict = json.loads(data_dict)
        final = data_dict[next(iter(data_dict))].get("property", {}).get(place)
        return final

    def find_agent(self, data_dict, place):
        try:
            data_dict = json.loads(data_dict)

        except TypeError:
            return ''

        final = data_dict[next(iter(data_dict))].get("property", {}).get('attributionInfo', {}).get(place, {})

        if final and place == 'agentPhoneNumber':
            phone_numbers = re.findall(r'\d+', final)
            final = ''.join(phone_numbers)

        return final

    def find_fact(self, data_dict, place):
        try:
            data_dict = json.loads(data_dict)

        except TypeError:
            if place == 'Lot':
                return ''

        if place == 'available':
            place = 'Date available'

        try:
            final = data_dict[next(iter(data_dict))].get("property", {}).get('resoFacts', {}).get('atAGlanceFacts', {})

        except AttributeError:
            return ''

        if final:
            for item in final:
                if item['factLabel'] == place:
                    return item['factValue']

    def get_tax(self, data_dict):
        if isinstance(data_dict, dict):
            data_dict = data_dict[(list(data_dict.keys())[0])]

        try:
            data_dict = json.loads(data_dict)

        except TypeError:
            return ''

        final = data_dict[next(iter(data_dict))].get('property', {}).get('taxHistory', {}) or ''

        if final == '':
            return final

        if isinstance(final, list):
            return final[0].get('taxPaid')

        return final.get('taxPaid', {})

    def get_images(self, data_dict):
        if isinstance(data_dict, dict):
            temp = data_dict
            data_dict = data_dict[(list(data_dict.keys())[0])]

            if data_dict is False:
                try:
                    temp = (temp.get('initialReduxState', {}).get('gdp', {}).get('building', {}).get('photos', {})[0].
                            get('mixedSources', {}).get('jpeg', {}))

                except IndexError:
                    return ''

                image = []

                for i in range(len(temp)):
                    image.append(temp[i].get('url', {}))

                return image

        data_dict = json.loads(data_dict)
        final = (data_dict[next(iter(data_dict))].get('property', {}).get('responsivePhotos', {})[0].
                 get('mixedSources', {}).get('jpeg', {}))
        image = []

        for i in range(len(final)):
            image.append(final[i].get('url', {}))

        return image

    def get_visited_urls(self):
        urls = []
        try:
            with open(self.file_name, 'r', encoding='utf-8') as csvfile:
                rows = csv.reader(csvfile)

                for row in rows:
                    urls.append(row[0])

                return list(set(urls))

        except FileNotFoundError:
            return []

    def write_csv(self, data):

        with open(self.file_name, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.field_names)

            if csvfile.tell() == 0:
                writer.writeheader()

            data = dict(data)
            filtered_data = {key: data[key] for key in self.field_names if key in data}
            writer.writerow(filtered_data)

    def get_address(self, response):
        data_dict = self.get_json(response)
        try:
            address = ' '.join(str(value) for value in self.find_data(data_dict, 'address').values()
                               if value is not None)

        except AttributeError:
            address = self.find_data(response, 'address')

        if not address:
            address = response.css('[data-test-id="bdp-building-address"]::text').get('')

        return address

    def get_date(self, data_dict):
        if isinstance(data_dict, dict):
            data_dict = data_dict[(list(data_dict.keys())[0])]

        try:
            data_dict = json.loads(data_dict)

        except TypeError:
            return ''

        final = data_dict[next(iter(data_dict))].get('property', {}).get('priceHistory', {})

        if isinstance(final, list):
            dates = []

            for i in range(len(final)):
                dates.append(final[i].get('date', {}))

            return dates

        return final.get('date')

    def get_json(self, response):
        data_dict = (json.loads(response.css('#__NEXT_DATA__::text').get('')).get('props', {}).get('pageProps', {}).
                     get('componentProps', {}))

        if 'gdpClientCache' in data_dict:
            data_dict = data_dict.get('gdpClientCache', {})

        return data_dict

    def fix_url(self, url):
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "https://www.zillow.com" + url
        return url

    def get_pin_location(self, response):
        self.location = json.loads(response.css('script:contains("window.mapBounds")::text')
                                   .re_first(r'window\.mapBounds = ({.*?});'))

        form_data = self.get_form_data()
        self.get_pull_request_for_urls(form_data)
        a = ''

    def get_form_data(self, page_number=1):
        a = ''
        form_data = {
            'searchQueryState': {
                'pagination': {
                    'currentPage': page_number,
                },
                'isMapVisible': True,
                'mapBounds': self.location,
                'filterState': {
                    'isForRent': {
                        'value': True,
                    },
                    'isForSaleByAgent': {
                        'value': False,
                    },
                    'isForSaleByOwner': {
                        'value': False,
                    },
                    'isNewConstruction': {
                        'value': False,
                    },
                    'isComingSoon': {
                        'value': False,
                    },
                    'isAuction': {
                        'value': False,
                    },
                    'isForSaleForeclosure': {
                        'value': False,
                    },
                    'isAllHomes': {
                        'value': True,
                    },
                },
                'isListVisible': True,
                'mapZoom': 14,
            },
            'wants': {
                'cat1': [
                    'listResults',
                    'mapResults',
                ],
            },
            'requestId': 4,
            'isDebugRequest': False,
        }
        a = ''
        return form_data

    def get_pull_request_for_urls(self, form_data):
        yield Request(url='https://www.zillow.com/async-create-search-page-state',
                      method='PUT',
                      body=form_data,
                      callback=self.parse_urls,
                      headers=self.headers)
