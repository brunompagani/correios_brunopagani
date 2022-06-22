import scrapy
from scrapy.utils.project import get_project_settings
from correios.items import CorreiosComplementarItem
from scrapy.loader import ItemLoader
import re

class CorreiosComplementarSpider(scrapy.Spider):
    name = 'correios_complementar'
    allowed_domains = ['www2.correios.com.br']
    start_urls = ['https://www2.correios.com.br/sistemas/buscacep/buscaFaixaCep.cfm']
    uf_parcial_url = 'https://www2.correios.com.br/sistemas/buscacep/consultaLocalidade.cfm?mostrar=1&UF='
    letter_url = 'https://www2.correios.com.br/sistemas/buscacep/consultaLocalidade.cfm?mostrar=2'

    # Arquivos de saída
    settings = get_project_settings()
    out_file = settings.get('OUTPUT_PATH') / 'correios_complementar.jsonl'

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
        ''' Essa função raspa os dados de UF do dropdown e faz o GET request
        para cada um dos resultados.

        Essa docstring contém scrapy.contracts para testes:
        @url http://localhost:8080/buscaFaixaCep.html
        @returns requests 27 27
        '''
        opcoes_uf = response.css('select[name=UF] option::text').getall()
        for uf in opcoes_uf:
                if re.match('^[A-Z]{2}$', uf):
                    yield response.follow(
                        url=f'{self.uf_parcial_url}{uf}',
                        callback=self.parse_uf_letters,
                        cb_kwargs={'uf': uf}
                    )
                
                    print(f'Carregamento de páginas de {uf} iniciado')

    def parse_uf_letters(self, response, uf):
        '''Essa função raspa os dados de letras iniciais para localidades
        de cada uf e faz o POST request correspondente para cada inicial.
        
        Essa docstring contém scrapy.contracts para testes:
        @url http://localhost:8080/ConsultaLocalidade_mostrar1.html
        @cb_kwargs {"uf": "TO"}
        @returns requests 1 26
        '''
        letras = response.css('a[name=Letra]::text').re('^[A-Z]')
        ultima_letra = letras[-1]

        for letra in letras:
            formdata={
                'UF': uf,
                'Letra': letra,
            }
            last_page_uf = letra == ultima_letra
        
            yield scrapy.FormRequest(
                url=self.letter_url,
                formdata=formdata,
                callback=self.parse_localidade,
                cb_kwargs = {'uf': uf, 'last_page_uf': last_page_uf}
            )

    def parse_localidade(self, response, uf, last_page_uf):
        '''Essa função raspa os dados das tabelas para cada inicial de localidades
        de cada uf.
        
        Essa docstring contém scrapy.contracts para testes:
        @url http://localhost:8080/ConsultaLocalidade_mostrar2.html
        @cb_kwargs {"uf": "TO"}
        @returns requests 0 0
        @returns items 1
        @scrapes uf localidade cep
        '''
        rows = response.css('table tr')

        # conta o num de linhas
        last_row = len(rows)
        i = 0

        for row in rows:
            i += 1
            header = row.css('td b')
            if not header:
                l = ItemLoader(item=CorreiosComplementarItem(), selector=row)

                l.add_value('uf', uf)
                l.add_css('localidade', 'td:nth-child(2)')
                l.add_css('cep', 'td:nth-child(3)')
                
                yield l.load_item()
         
        if last_page_uf and (i == last_row):
            print(f'Processamento de páginas e itens em {uf} finalizado!')
