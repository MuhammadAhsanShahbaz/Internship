import os

from twisted.internet import defer, reactor

from spiders.zillow_Rent import ZillowRentSpider
from spiders.zillow_sold import ZillowSoldSpider
from spiders.zillow_Sale import ZillowSaleSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def start_seq(process: CrawlerProcess, crawlers: list):
    deferreds = []
    for crawler in crawlers:
        print('Start Spider {}'.format(crawler.__name__))
        deferred = process.crawl(crawler)
        deferreds.append(deferred)

    return defer.DeferredList(deferreds)


if __name__ == '__main__':
    crawlers = [ZillowSoldSpider, ZillowRentSpider, ZillowSaleSpider]
    settings_file_path = 'zillow_scrapy.zillow_scrapy'
    os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
    process = CrawlerProcess(get_project_settings())

    d = start_seq(process, crawlers)

    d.addBoth(lambda _: reactor.stop())
    reactor.run()

