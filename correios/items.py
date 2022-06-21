# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags
import re

def str_strip(string):
    return string.strip()

def limpa_localidade_complementar(string):
    match = re.match(r'.*(?=/[A-Z]{2})', string=string)
    return match.group(0)

class CorreiosItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    
    uf = scrapy.Field(
        input_processor=MapCompose(remove_tags, str_strip),
        output_processor=TakeFirst()
    )
    localidade = scrapy.Field(
        input_processor=MapCompose(remove_tags, str_strip),
        output_processor=TakeFirst()
    )
    faixa_cep = scrapy.Field(
        input_processor=MapCompose(remove_tags, str_strip),
        output_processor=TakeFirst()
    )
    situacao = scrapy.Field(
        input_processor=MapCompose(remove_tags, str_strip),
        output_processor=TakeFirst()
    )
    tipo_faixa = scrapy.Field(
        input_processor=MapCompose(remove_tags, str_strip),
        output_processor=TakeFirst()
    )

    data_raspagem = scrapy.Field()

class CorreiosComplementarItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()

    uf = scrapy.Field(
        input_processor=MapCompose(remove_tags, str_strip),
        output_processor=TakeFirst()
    )
    localidade = scrapy.Field(
        input_processor=MapCompose(remove_tags, str_strip, limpa_localidade_complementar),
        output_processor=TakeFirst()
    )
    cep = scrapy.Field(
        input_processor=MapCompose(remove_tags, str_strip),
        output_processor=TakeFirst()
    )

    data_raspagem = scrapy.Field()