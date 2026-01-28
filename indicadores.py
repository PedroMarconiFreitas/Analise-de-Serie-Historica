#%%
import pandas as pd
import numpy as np
import time

#%%
df_3 = pd.read_csv('./microdados_enamed_2025/microdados_enamed_2025_19-01-26/DADOS/Enade/microdados_enade_2025_arq3.txt', sep=';', encoding='latin1')
#%%
df_3.head()
#%%
df_3 = df_3[['QT_ACERTO_AREA_1',
'QT_ACERTO_AREA_2',
'QT_ACERTO_AREA_3',
'QT_ACERTO_AREA_4',
'QT_ACERTO_AREA_5']]
#%%
df_3.rename(columns={
    'QT_ACERTO_AREA_1': 'Acertos_Clinica_Medica',
    'QT_ACERTO_AREA_2': 'Acertos_Pediatria',
    'QT_ACERTO_AREA_3': 'Acertos_Cirurgia_Geral',
    'QT_ACERTO_AREA_4': 'Acertos_Ginecologia_Obstetricia',
    'QT_ACERTO_AREA_5': 'Acertos_Medicina_Familia_Saude_Coletiva'
}, inplace=True)
#%%
df_3.head()
#%%

grupo_renomeado = ['Acertos_Clinica_Medica',
'Acertos_Pediatria', 'Acertos_Cirurgia_Geral',
'Acertos_Ginecologia_Obstetricia', 'Acertos_Medicina_Familia_Saude_Coletiva']

for i in grupo_renomeado:
    print(df_3[i].unique(), flush = True)

#%%

indicadores = [1, 5, 6, 9]

df = {}

#%%
for i in indicadores:
    
    df[i] = pd.read_csv(f'./microdados_enamed_2025/microdados_enamed_2025_19-01-26/DADOS/Enade/microdados_enade_2025_arq{i}.txt', sep = ';', encoding = 'latin1')

#%%
df[1].head()
#%%
for i in indicadores:
    print('DF do arquivo', i)
    print(f'DF{i} possui {df[i].shape[0]} linhas e {df[i].shape[1]} colunas.')
    display(df[i].head())
    display(df[i].info())
    time.sleep(0.5)
#%%

df_concatenado = pd.concat(df.values(), ignore_index=False, axis=1)

# %%
df_concatenado.head()

#%%
df_concatenado.tail()
#%%
df_concatenado.info()
#%%
df_concatenado.shape[0]
#%%
df_concatenado.shape[1]
#%%


#%%

df_concatenado.rename(columns={
    'TP_INSCRICAO': 'Tipo de Inscrição',
    'TP_SEXO': 'Sexo',
    'NU_IDADE': 'Idade',
    'QE_I03': 'Raça ou Cor',
    'CO_UF_CURSO': 'UF do Curso',
    'CO_REGIAO_CURSO': 'Região do Curso',
    'CO_CATEGAD': 'Categoria Administrativa'
}, inplace=True)

#%%
df_concatenado.head()
#%%
df_concatenado.info()
# %%
df_concatenado = df_concatenado[['Idade','Raça ou Cor', 'Sexo', 'Região do Curso','UF do Curso', 'Categoria Administrativa', 'Tipo de Inscrição']]

#%%
df_concatenado.head()
#%%
df_concatenado.tail()
#%%

map_tp_inscricao = {
    0: 'Concluinte do Enade',
    1: 'Demais participantes'
}

map_cor_raca = {
    'A': 'Branca',
    'B': 'Preta',
    'C': 'Amarela',
    'D': 'Parda',
    'E': 'Indígena',
    'F': 'Não quero declarar',
    '.': 'Sem resposta'
}

map_sexo = {
    'M': 'Masculino',
    'F': 'Feminino',
    9: 'Indefinido'
}

map_categoria_ies = {
    1: 'Pública Federal',
    2: 'Pública Estadual',
    3: 'Pública Municipal',
    4: 'Privada com fins lucrativos',
    5: 'Privada sem fins lucrativos',
    7: 'Especial',
    8: 'Comunitária / Confessional'
}

map_uf = {
    11: 'RO', 12: 'AC', 13: 'AM', 14: 'RR', 15: 'PA', 16: 'AP', 17: 'TO',
    21: 'MA', 22: 'PI', 23: 'CE', 24: 'RN', 25: 'PB', 26: 'PE',
    27: 'AL', 28: 'SE', 29: 'BA',
    31: 'MG', 32: 'ES', 33: 'RJ', 35: 'SP',
    41: 'PR', 42: 'SC', 43: 'RS',
    50: 'MS', 51: 'MT', 52: 'GO', 53: 'DF'
}

map_regiao = {
    1: 'Norte',
    2: 'Nordeste',
    3: 'Sudeste',
    4: 'Sul',
    5: 'Centro-Oeste'
}

df_concatenado['Tipo de Inscrição'] = df_concatenado['Tipo de Inscrição'].map(map_tp_inscricao)
df_concatenado['Raça ou Cor'] = df_concatenado['Raça ou Cor'].map(map_cor_raca)
df_concatenado['Categoria Administrativa'] = df_concatenado['Categoria Administrativa'].map(map_categoria_ies)
df_concatenado['UF do Curso'] = df_concatenado['UF do Curso'].map(map_uf)
df_concatenado['Região do Curso'] = df_concatenado['Região do Curso'].map(map_regiao)
df_concatenado['Sexo'] = df_concatenado['Sexo'].map(map_sexo)

#%%
df_concatenado = pd.concat([df_concatenado, df_3], axis=1)
#%%
df_concatenado.head()
#%%
df_concatenado.info()
#%%
colunas = df_concatenado.columns

for c in colunas:
    print(f'Coluna: {c}')
    print(df_concatenado[c].unique(), flush=True)
    print('\n')
    time.sleep(0.5)
    

#%%
grupos = ['Idade', 'Raça ou Cor', 'Sexo', 'Região do Curso', 'UF do Curso',
       'Categoria Administrativa', 'Tipo de Inscrição']


# %%
df_concatenado.to_excel('indicadores_enamed_2025.xlsx', index=False)
