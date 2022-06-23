# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags
import re

def str_strip(string):
    return string.strip()

def limpa_localidade_complementar(string):
    cleaned = re.sub(r'/[A-Z]{2}$', '', string=string)
    return cleaned

def get_first_cep(string):
    first = re.findall(r'^[0-9]{5}-[0-9]{3}', string=string)[0]
    return first

def get_last_cep(string):
    last = re.findall(r'[0-9]{5}-[0-9]{3}$', string=string)[0]
    return last

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
    faixa_cep_min = scrapy.Field(
        input_processor=MapCompose(remove_tags, str_strip, get_first_cep),
        output_processor=TakeFirst()
    )
    faixa_cep_max = scrapy.Field(
        input_processor=MapCompose(remove_tags, str_strip, get_last_cep),
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