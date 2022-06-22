import scrapy
from scrapy.utils.project import get_project_settings
from correios.items import CorreiosItem
from scrapy.loader import ItemLoader
import re

class CorreiosSpider(scrapy.Spider):
    name = 'correios'
    allowed_domains = ['www2.correios.com.br']
    start_urls = ['https://www2.correios.com.br/sistemas/buscacep/buscaFaixaCep.cfm']
    result_url = 'https://www2.correios.com.br/sistemas/buscacep/ResultadoBuscaFaixaCEP.cfm'

    # Arquivos de saída
    settings = get_project_settings()
    out_file = settings.get('OUTPUT_PATH') / 'correios.jsonl'

    # Saída
    custom_settings = {
        'FEEDS': {
            out_file: {
                'format': 'jsonlines',
                'encoding': 'utf8',
                'overwrite': True,
                'store_empty': False,
            }
        }
    }

    def parse(self, response):
        ''' Essa função raspa os dados de UF do dropdown e faz o primeiro POST request
        para cada um dos resultados.

        Essa docstring contém scrapy.contracts para testes:
        @url http://localhost:8080/buscaFaixaCep.html
        @returns requests 27 27
        '''

        opcoes_uf = response.css('select[name=UF] option::text').getall()

        for uf in opcoes_uf:
                if re.match('^[A-Z]{2}$', uf):
                    formdata={
                        'UF': uf,
                        'Localidade': '**',
                        'Bairro': '',
                        'qtdrow': '50',
                        'pagini': '1',
                        'pagfim': '50'
                    }

                    yield scrapy.FormRequest(
                        url=self.result_url,
                        formdata=formdata,
                        callback=self.parse_uf,
                        cb_kwargs = {'uf': uf}
                    )
                    
                    print(f'Carregamento de páginas de {uf} iniciado') 

    def parse_uf(self, response, uf):
        ''' Essa função raspa os dados de uma página de resultados, faz o POST request
        para a próxima página, repetindo o processo até encontrar a última.

        Essa docstring contém scrapy.contracts para testes:
        @url http://localhost:8080/ResultadoBuscaFaixaCep.html
        @cb_kwargs {"uf": "TO"}
        @returns items 1 50
        @scrapes uf localidade faixa_cep situacao tipo_faixa
        '''
        
        records_str = response\
            .css('div.ctrlcontent::text')\
            .re('[0-9]{1,4} a [0-9]{1,4} de [0-9]{1,4}')[0]
        records_list = re.findall('[0-9]{1,4}', records_str)

        page_first_rec, page_last_rec, total_records = [int(x) for x in records_list]

        table = response.css('table.tmptabela:last-of-type')
        rows = table.css('tr')

        for row in rows:
            if row.css('td'):
                l = ItemLoader(item=CorreiosItem(), selector=row)

                l.add_value('uf', uf)
                l.add_css('localidade', 'td:nth-child(1)')
                l.add_css('faixa_cep', 'td:nth-child(2)')
                l.add_css('situacao', 'td:nth-child(3)')
                l.add_css('tipo_faixa', 'td:nth-child(4)')

                yield l.load_item()

        if page_last_rec != total_records:
            formdata={
                'UF': uf,
                'Localidade': '**',
                'Bairro': '',
                'qtdrow': '50',
                'pagini': str(page_last_rec + 1),
                'pagfim': str(page_last_rec + 50)
            }

            yield scrapy.FormRequest(
                url=self.result_url,
                formdata=formdata,
                callback=self.parse_uf,
                cb_kwargs = {'uf': uf}
            )

        if page_last_rec == total_records:
            print(f'Processamento de páginas e itens em {uf} finalizado!')