# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class QoutesPipeline:
    def process_item(self, item, spider):

        adapter = ItemAdapter(item)

        name = adapter.field_names()
        for n in name:
            if n == 'description':
                value = str(adapter.get(n))
                value = value.replace('\n','').strip()
                adapter[n] = value

        #item['description'] = item['description'].replace('\n','')
        return item