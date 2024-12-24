import json

from scrapy import Request
from .zillow_Rent import ZillowRentSpider


class ZillowSoldSpider(ZillowRentSpider):
    name = "zillow_sold"

    def __init__(self, *args, **kwargs):
        super(ZillowSoldSpider, self).__init__(*args, **kwargs)
        self.file_name = 'output/sold.csv'
        self.zillow_type = 'sold'
        self.field_names = ['URL', 'Full Address', 'Type', 'Images', 'Beds', 'Baths', 'Sq Ft', 'Price', 'Latitude',
                            'Longitude', 'City', 'Street', 'State', 'Zip Code', 'Year Built', 'Style', 'Lot',
                            'Agent Name', 'Agent Phone', 'Agent Email', 'Broker Name', 'MLS', 'Tax', 'Sold Date']
        self.visited_urls = self.get_visited_urls()

    def get_form_data(self, page_number=1):
        json_data = {
            'searchQueryState': {
                'pagination': {
                    'currentPage': page_number,
                },
                'isMapVisible': True,
                'mapBounds': self.location,
                'filterState': {
                    'sortSelection': {
                        'value': 'globalrelevanceex',
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
                    'isRecentlySold': {
                        'value': True,
                    },
                },
                'isListVisible': True,
                'mapZoom': 12,
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

        return json_data

        # return Request(url='https://www.zillow.com/async-create-search-page-state',
        #                method='PUT',
        #                body=json.dumps(json_data),
        #                callback=self.parse_urls,
        #                headers=self.headers)
#