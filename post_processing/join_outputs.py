import pandas as pd
from pathlib import Path
from datetime import datetime
import jsonlines

print('Processamento iniciado...')
# acha arquivos
root = Path('./').parent
out_path = root / 'output'
correios_file = out_path / 'correios.jsonl'
correios_complementar_file = out_path / 'correios_complementar.jsonl'
out_file = out_path / 'correios_join.jsonl'

if not correios_file.exists() or not correios_file.is_file():
    raise Exception(f'O arquivo {correios_file.resolve()} não existe')
if not correios_complementar_file.exists() or not correios_complementar_file.is_file():
    raise Exception(f'O arquivo {correios_complementar_file.resolve()} não existe')

#Lê arquivos
correios = pd.read_json(correios_file, lines=True)
correios_complementar = pd.read_json(correios_complementar_file, lines=True)

# Cria coluna subordinado_a, baseado em localidade
correios_complementar['subordinada_a'] = correios_complementar['localidade'].str.extract(r'.*\((.*)\).*')

# separa localidades com subordinação
correios_sub = correios_complementar.loc[~correios_complementar['subordinada_a'].isna()]

# separa faixas tipo 'Total do município'
correios_tot = correios.loc[correios['tipo_faixa'] == 'Total do município', :]

# cria tabela com ids de 'municipio-sede'
merge = pd.merge(correios_tot, correios_sub, how='inner', left_on=['localidade', 'uf'], right_on=['subordinada_a', 'uf'])

select_merge = merge.loc[:, [
    'uf', 'localidade_y', 'faixa_cep', 'situacao',
    'tipo_faixa', 'subordinada_a','id_x'
]]

select_merge.rename({'localidade_y': 'localidade', 'id_x': 'id_subordinacao'}, axis=1, inplace=True)

# atualiza id para tabela completa
ultimo_id = correios['id'].max()
select_merge['id'] = select_merge.index + ultimo_id + 1
correios.insert(0, 'id', correios.pop('id'))

# cria tabela completa
correios_join = pd.concat([correios, select_merge])

correios_join['data_join'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

correios_join['id_subordinacao'] = correios_join['id_subordinacao'].fillna(0)
correios_join['id_subordinacao'] = correios_join['id_subordinacao'].astype(int)

# Exporta em formato correto:
dict = correios_join.to_dict(orient='records')

with jsonlines.open(out_file, 'w') as j:
        j.write_all(dict)

print('Processamento concluído!')

# print(correios_join.head(30))
# print(correios_join.tail(30))