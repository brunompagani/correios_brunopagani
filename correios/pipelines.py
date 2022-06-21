# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from datetime import datetime

class CorreiosPipeline:
    def open_spider(self, spider):
        print(f'Spider "{spider.name}" iniciada...')

    def close_spider(self, spider):
        print(f'Spider "{spider.name}" finalizada.')
        print('Para mais informações da execução, verifique os logs em logs/log_spiders.txt.')

class DuplicatesPipeline:

    def __init__(self):
        self.correios_items = []
        self.corr_comp_items = []

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if spider.name == 'correios':
            correios_item = []
            for field in adapter.asdict().values():
                correios_item.append(field)
            if correios_item in self.correios_items:
                raise DropItem(f"Item duplicado encontrado: {item!r}")
            else:
                self.correios_items.append(correios_item)
                return item

        if spider.name == 'correios_complementar':
            corr_comp_item = []
            for field in adapter.asdict().values():
                corr_comp_item.append(field)
            if corr_comp_item in self.corr_comp_items:
                raise DropItem(f"Item duplicado encontrado: {item!r}")
            else:
                self.corr_comp_items.append(corr_comp_item)
                return item

class UniqueKeyPipeline:

    def __init__(self):
        self.last_id = 0

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        adapter['id'] = self.last_id + 1
        self.last_id += 1

        return item

class ScrapedDatePipeline:

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        adapter['data_raspagem'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        return item