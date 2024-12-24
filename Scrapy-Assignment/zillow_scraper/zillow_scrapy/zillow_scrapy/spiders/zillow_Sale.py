import json

from scrapy import Request
from .zillow_Rent import ZillowRentSpider


class ZillowSaleSpider(ZillowRentSpider):
    name = "zillow_Sale"

    def __init__(self, *args, **kwargs):
        super(ZillowSaleSpider, self).__init__(*args, **kwargs)
        self.file_name = 'output/sale.csv'
        self.zillow_type = 'sale'
        self.field_names = ['URL', 'Full Address', 'Type', 'Images', 'Beds', 'Baths', 'Sq Ft', 'Price', 'Latitude',
                            'Longitude', 'City', 'Street', 'State', 'Zip Code', 'Year Built', 'Style',
                            'Lot', 'Agent Name', 'Agent Phone', 'Agent Email', 'Broker Name', 'MLS', 'Tax']
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
                    'isMultiFamily': {
                        'value': False,
                    },
                    'isLotLand': {
                        'value': False,
                    },
                    'isAllHomes': {
                        'value': True,
                    },
                },
                'isListVisible': True,
                'mapZoom': 13,
            },
            'wants': {
                'cat1': [
                    'listResults',
                    'mapResults',
                ],
                'cat2': [
                    'total',
                ],
            },
            'requestId': 4,
            'isDebugRequest': False,
        }
        return Request(url='https://www.zillow.com/async-create-search-page-state',
                       method='PUT',
                       body=json.dumps(json_data),
                       callback=self.parse_urls,
                       headers=self.headers)
