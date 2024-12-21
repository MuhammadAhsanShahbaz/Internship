import csv
import json
from collections import OrderedDict
from datetime import datetime

from scrapy import Spider, Request


class HonestdoorSpider(Spider):
    name = "honestdoor"
    allowed_domains = ["honestdoor.com"]
    start_urls = ["https://honestdoor.com"]

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Origin': 'https://honestdoor.com',
        'Referer': 'https://honestdoor.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/107.0.0.0',
        'sec-ch-ua': '"Not A(Brand";v="99", "Opera GX";v="107", "Chromium";v="121"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': f'output/Results {datetime.now().strftime("%d%m%Y%H%M%S")}.csv',
        'FEED_EXPORT_FIELDS': ['Searched Address', 'Address', 'City', 'Province', 'Postal Code', 'City Assessment 2024',
                               'Sold Price', 'Sold Date', 'Last Estimated Price', 'Last Estimated Date', 'URL']
    }

    def __init__(self, *args, **kwargs):
        super(HonestdoorSpider, self).__init__(*args, **kwargs)
        self.output_file_name = 'output/Results.csv'
        self.input_file_name = 'input/addresses.txt'
        # self.seen_urls = [row.get('URL', '') for row in self.read_csv_file()]
        self.search_addresses = self.get_input_addresses

    def start_requests(self):
        yield Request(url=self.start_urls[0], headers=self.headers)

    def parse(self, response, **kwargs):
        for address in self.search_addresses():
            form_data = {
                'query': '\n    query multiSearch($query: String!) {\n  multiSearch(query: $query) {\n    properties {\n      id\n      unparsedAddress\n      cityName\n      province\n      slug\n      accountNumber\n      location {\n        lat\n        lon\n      }\n      bathroomsTotal\n      bedroomsTotal\n      houseStyle\n      livingArea\n      lotSizeArea\n      yearBuiltActual\n      basement\n      show\n      creaListing {\n        slug\n        listingId\n        meta {\n          id\n        }\n        location {\n          lat\n          lon\n        }\n      }\n    }\n    cities {\n      id\n      name\n      provinceAbbr\n      centroid {\n        lat\n        lon\n      }\n    }\n    neighbourhoods {\n      id\n      name\n      city {\n        id\n        provinceAbbr\n      }\n      cityName\n      centroid {\n        lat\n        lon\n      }\n    }\n  }\n}\n    ',
                'variables': {
                    'query': address,
                },
            }

            yield Request(
                url='https://api.honestdoor.com/api/v1',
                method='POST',
                body=json.dumps(form_data),
                callback=self.parse_id,
                headers=self.headers,
                meta={'handle_httpstatus_all': True, 'address': address})

    def parse_id(self, response):
        property_id = ''

        suggested_properties = response.json().get('data', {}).get('multiSearch', {}).get('properties', [])

        for property in suggested_properties:
            found_address = property.get('unparsedAddress', '').lower()

            # To get the exact search name else continue
            # if response.meta.get('address').lower() not in found_address or found_address not in response.meta.get('address').lower():
            #     continue

            # To search the first suggested address
            property_id = response.json().get('data', {}).get('multiSearch', {}).get('properties', [])[0].get('id', '')
            break

        # if there is no suggested address for the search name
        if not property_id:
            items = OrderedDict()
            items['Searched Address'] = response.meta.get('address')

            yield items

            return

        #next_id = response.json().get('data', {}).get('multiSearch', {}).get('properties', [])[0].get('id', '')
        form_data = {
            'query': '\n    query propertyFull($slug: String, $id: String) {\n  property(slug: $slug, id: $id) {\n    ...PropertyFull\n  }\n}\n    \n    fragment PropertyFull on ESProperty {\n  ...PropertyCore\n  ...PropertyBuilding\n  ...PropertyBuildingEstimates\n  ...PropertyPricesDates\n  ...PropertyAddress\n  ...PropertyLocation\n  ...PropertyValuations\n  ...PropertyAssessments\n  ...PropertyRentalActual\n  ...PropertyAirBnBActual\n  ...PropertyCloses\n}\n    \n\n    fragment PropertyCore on ESProperty {\n  id\n  slug\n  assessmentClass\n  zoning\n  accountNumber\n  creaListing {\n    meta {\n      id\n    }\n    slug\n    price\n    location {\n      lon\n      lat\n    }\n  }\n}\n    \n\n    fragment PropertyBuilding on ESProperty {\n  bathroomsTotal\n  bedroomsTotal\n  livingArea\n  lotSizeArea\n  yearBuiltActual\n  show\n  fireplace\n  garageSpaces\n  houseStyle\n  livingAreaUnits\n  basement\n  building {\n    propertyCount\n  }\n}\n    \n\n    fragment PropertyBuildingEstimates on ESProperty {\n  bathroomsTotalEst\n  bedroomsTotalEst\n  livingAreaEst\n  lotSizeAreaEst\n}\n    \n\n    fragment PropertyPricesDates on ESProperty {\n  closeDate\n  closePrice\n  lastEstimatedPrice\n  lastEstimatedYear\n  predictedDate\n  predictedValue\n}\n    \n\n    fragment PropertyAddress on ESProperty {\n  unparsedAddress\n  province\n  city\n  cityName\n  neighbourhood\n  neighbourhoodName\n  postal\n}\n    \n\n    fragment PropertyLocation on ESProperty {\n  location {\n    lat\n    lon\n  }\n}\n    \n\n    fragment PropertyValuations on ESProperty {\n  valuations {\n    id\n    predictedValue\n    predictedDate\n  }\n}\n    \n\n    fragment PropertyAssessments on ESProperty {\n  assessments {\n    id\n    value\n    year\n  }\n}\n    \n\n    fragment PropertyRentalActual on ESProperty {\n  rentalActual {\n    rentEstimate\n    rentalYield\n  }\n}\n    \n\n    fragment PropertyAirBnBActual on ESProperty {\n  airbnbActual {\n    airbnbEstimate\n  }\n}\n    \n\n    fragment PropertyCloses on ESProperty {\n  closes {\n    id\n    price\n    date\n  }\n}\n    ',
            'variables': {
                'id': property_id,
            },
        }

        yield Request(
            url='https://api.honestdoor.com/api/v1',
            method='POST',
            body=json.dumps(form_data),
            callback=self.parse_detail, headers=self.headers,
            meta={'address': response.meta.get('address')})

    def parse_detail(self, response):
        data = response.json().get('data', '').get('property', {})

        items = OrderedDict()

        items['Searched Address'] = response.meta.get('address')
        items['Address'] = data.get('unparsedAddress', '')
        items['City'] = data.get('cityName', '')
        items['Province'] = data.get('province', '')
        items['Postal Code'] = data.get('postal', '')
        items['City Assessment 2024'] = data.get('lastEstimatedPrice', '')
        items['Sold Price'] = data.get('closePrice', '')
        items['Sold Date'] = data.get('closeDate', '')
        items['Last Estimated Price'] = data.get('predictedValue', '')
        items['Last Estimated Date'] = data.get('predictedDate', '')
        items['URL'] = f"https://honestdoor.com/property/{data.get('slug', '')}"

        yield items

    def get_input_addresses(self):
        try:
            with open(self.input_file_name, "r") as txt_file:
                return [line.strip() for line in txt_file.readlines() if line.strip()]

        except FileNotFoundError:
            return []

    # def read_csv_file(self):
    #     try:
    #         with open(self.output_file_name, 'r', encoding='utf-8') as csvfile:
    #             return list(csv.DictReader(csvfile))
    #
    #     except FileNotFoundError:
    #         return []