# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from datetime import datetime
import logging
import os

class LogsPipeline:

    def __init__(self):
        self.ufs_raspadas = {}

    def open_spider(self, spider):
        if not os.environ.get('SCRAPY_CHECK'):
            print(f'Spider "{spider.name}" iniciada...')

    def process_item(self, item, spider):
        '''Conta ufs extraídas e avisa inicio de cada uf'''
        adapter = ItemAdapter(item)
        uf = adapter.asdict()['uf']
        if uf not in self.ufs_raspadas.keys():
            self.ufs_raspadas[uf] = 1
            print(f'Processamento de itens de {uf} iniciada..')
        else:
            self.ufs_raspadas[uf] += 1
        return item

    def close_spider(self, spider):
        if not os.environ.get('SCRAPY_CHECK'):
            print(f'Spider "{spider.name}" finalizada.')
            print('-------------------------------------------')
            print(f'Foram coletados {sum(self.ufs_raspadas.values())} itens.')
            logging.info(f'Foram coletados {sum(self.ufs_raspadas.values())} itens.')
            print('-------------------------------------------')
            print('Itens por região:')
            logging.info('Itens por região:')
            for uf, qnt in self.ufs_raspadas.items():
                print(f'{uf}: {qnt} itens')
                logging.info(f'{uf}: {qnt} itens')
            print('-------------------------------------------')
            print('Para mais informações da execução, verifique os logs em logs/log_spiders.txt.')

class DuplicatesPipeline:

    def __init__(self):
        self.items_raspados = []

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        item_raspado = []
        for field in adapter.asdict().values():
            item_raspado.append(field)
        if item_raspado in self.items_raspados:
            raise DropItem(f"Item duplicado encontrado: {item!r}")
        else:
            self.items_raspados.append(item_raspado)
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

class MyOverwritePipeline:

    def close_spider(self, spider):
        print(spider.out_file)
        with open(spider.out_file) as f:
            lines = f.readlines()
            starts = []
            for i in range(len(lines)):
                if '"id": 1,' in lines[i]:
                    starts.append(i)

        if len(starts) == 2:
            with open(spider.out_file, 'w') as f:
                f.writelines(lines[starts[1]:])