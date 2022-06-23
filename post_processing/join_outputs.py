import pandas as pd
from pathlib import Path
from datetime import datetime
import jsonlines
import numpy as np

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
correios_comp_sub = correios_complementar.loc[~correios_complementar['subordinada_a'].isna()]

# separa faixas tipo 'Total do município'
correios_tot = correios.loc[correios['tipo_faixa'] == 'Total do município', :]

# cria tabela com ids de 'municipio-sede'
merge = pd.merge(correios_tot, correios_comp_sub, how='inner', left_on=['localidade', 'uf'], right_on=['subordinada_a', 'uf'])

select_merge = merge.loc[:, [
    'uf', 'localidade_y', 'situacao', 'subordinada_a', 'cep', 'faixa_cep_max', 'id_x'
]]

select_merge.rename({'localidade_y': 'localidade', 'id_x': 'id_subordinacao', 'cep': 'faixa_cep_min'}, axis=1, inplace=True)

select_merge['faixa_cep'] = select_merge['faixa_cep_min']+ ' a ' + select_merge['faixa_cep_max']
select_merge['tipo_faixa'] = 'Faixa de CEP aproximada'

# print(select_merge.head(5)) ##############

# atualiza id para tabela completa
ultimo_id = correios['id'].max()
select_merge['id'] = select_merge.index + ultimo_id + 1
# correios.insert(0, 'id', correios.pop('id')) #############

# cria tabela completa
select_correios = correios.loc[:, [
     'id', 'uf', 'localidade', 'faixa_cep', 'situacao', 'tipo_faixa',  'faixa_cep_min', 'faixa_cep_max'
]]
correios_join = pd.concat([select_correios, select_merge])

correios_join['data_join'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

correios_join['id_subordinacao'] = correios_join['id_subordinacao'].fillna(0)
correios_join['id_subordinacao'] = correios_join['id_subordinacao'].astype(int)

# Exporta em formato correto:
list_dicts = correios_join.to_dict(orient='records')

for i in range(len(list_dicts)):
    dict = list_dicts[i]
    for k, v in dict.items():
        if pd.isna(v):
            list_dicts[i][k] = None
    

with jsonlines.open(out_file, 'w') as j:
        j.write_all(list_dicts)

print('Processamento concluído!')

# print(correios_join.head(30))
# print(correios_join.tail(30))