# Raspagem Correios

## Resumo do Projeto

### Objetivo

Raspar os dados em https://www2.correios.com.br/sistemas/buscacep/buscaFaixaCep.cfm 

![alt text](/git_resources/buscaFaixaCep.png)

### Abordagem

Ao visitar o site vi a possibilidade de extrair dados de duas maneiras, uma mais óbvia (selecionando a UF e clicando em buscar) e outra menos, (selecionando a UF e clicando no botão de interrogação ao lado de "Localidade"), por isso separei o projeto em dois módulos, o módulo básico, onde é feita a raspagem dos resultados do envio do formulário e o complementar, onde é feita a raspagem dos resultados obtidos ao clicar na interrogação.

Tomei essa decisão ao perceber que os resultados do básico e do complementar são similares, mas não iguais. Assim há a opção ainda de unir os dois resultados em uma mesma tabela para criar uma com os dados mais completos.

## Tecnologias

O código foi todo criado em Python com auxílio do framework Scrapy.
Para a união final dois módulos foi ainda utilizado o Pandas e o Jsonlines.

## Ambiente Virtual
Antes de executar qualquer script abra um terminal na pasta raiz do repositório:

- Crie um ambiante virtual:


```
% python3 -m venv venv
```

- Certifique-se de estar usando o Ambiente virtual:
```
% source venv/bin/activate
```
## Instalando dependências

Instale o Scrapy, pandas, jsonlines e as dependências dessas bibliotecas na versão que eu utilizei:
```
% python -m pip install -r requirements.txt
```

## Executando o projeto:

Para realizar a raspagem básica dos resultados obtidos pelo envio do formulário de cada uma das UFs, simplesmente rode a spider “correios” no terminal:

```
% scrapy crawl correios
```

Para realizar a raspagem complementar das páginas obtidas ao selecionar cada UF e clicar na interrogação, execute a spider “correios_complementar” no terminal:
```
% scrapy crawl correios_complementar
```
Finalmente para realizar a junção das informações em cada um dos resultados, execute o script “join_outputs.py”:
```
% python post_processing/join_outputs.py
```

Executando testes:

No terminal, abra os htmls de teste no seu browser:

- Entre na pasta com os htmls de teste
```
% cd correios/htmls_test/
```
- Carregue os htmls no browser 
```
python -m http.server 8080
```
Em uma nova aba do terminal, execute os testes:

- Execute os testes para cada Spider
```
% scrapy check -v -s LOG_LEVEL="WARNING" correios
% scrapy check -v -s LOG_LEVEL="WARNING" correios_complementar
```
Descrição dos testes:

Os testes são realizados a partir dos scrapy.contracts, quando executados eles olham para os htmls guardados localmente e tentam realizar a raspagem, retornando o sucesso ou a falha de cada um dos contracts.
Os parâmetros analisados em cada contract podem ser vistos na docstring de cada função das spiders.
A decisão pelo de uso de arquivos armazenados localmente ajuda a entender se alguma mudança no código quebrou um comportamento esperado da função ou se uma mudança no site foi responsável. É sempre possível atualizar os htmls, simplesmente baixando outro html do site e substituindo o arquivo por um de mesmo nome.

## Pastas

### correios:
Possui o core do projeto com as spiders e os scripts de apoio  

### output:
Guarda todas as saídas do projeto. 
Obs : Os arquivos dentro dessa pasta aqui no repositório são um exemplo de uma execução anterior.

### logs:
Guarda todos os logs do projeto

Obs : Os arquivos dentro dessa pasta aqui no repositório são um exemplo de uma execução anterior. Diferente dos arquivos da pasta "output", o log incrementa esse arquivo, então é recomendado que o arquivo exemplo seja excluído ou renomeado.

### git_resources:
Guarda a/as imagem/ns usadas nesse README