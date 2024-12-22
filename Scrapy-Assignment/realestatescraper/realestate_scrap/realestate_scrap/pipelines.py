import scrapy

from scrapy.pipelines.images import ImagesPipeline
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class CustomImagePipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        PropertyId = item['PropertyId']
        index = request.meta['index']
        filename = f'{PropertyId}([{index}.jpg'

        return filename

    def get_media_requests(self, item, info):
        for index, image_url in enumerate(item["image_urls"], start=1):
            yield scrapy.Request(image_url, meta={'index': index})

    def item_completed(self, results, item, info):
        image_paths = [x["path"] for ok, x in results if ok]

        if not image_paths:
            raise DropItem("Item contains no images")

        adapter = ItemAdapter(item)
        adapter["image_paths"] = image_paths

        return item