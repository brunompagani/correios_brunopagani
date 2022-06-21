# Raspagem Correios

## Resumo do Projeto



## Ambiente Virtual
Antes de executar qualquer script abra um terminal na pasta raiz do repositório:

- Crie um ambiante virtual:

```
% python3 -m venv venv
```

Certifique-se de estar usando o Ambiente virtual:
```
% source venv/bin/activate
```
## Instalando dependências:

Instale o Scrapy:
```
% python -m pip install scrapy
```
Para realizar a junção da raspagem básica e da complementar instale também:
```
% python -m pip install pandas
% python -m pip install jsonlines
```
O arquivo “requirements.txt” guarda todas as versões utilizadas de cada biblioteca, incluindo suas dependências.

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
python3 -m http.server 8080
```
Em uma nova aba do terminal, execute os testes:

- Execute os testes para cada Spider
```
% scrapy check correios -v
% scrapy check correios_complementar -v
```
Descrição dos testes:

Os testes são realizados a partir dos scrapy.contracts, quando executados eles olham para htmls guardados localmente e tentam realizar a raspagem, retornando o sucesso ou a falha de cada um dos contracts.
Os parâmetros analisados em cada contract podem ser vistos na docstring de cada função das spiders.
A decisão pelo de uso arquivos armazenados localmente ajuda a entender se alguma mudança no código quebrou um comportamento esperado da função ou se uma mudança no site foi responsável. É sempre possível atualizar os htmls, simplesmente baixando outro html do site e substituindo o arquivo por um de mesmo nome.