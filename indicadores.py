#%%
import pandas as pd
import numpy as np

# %%
df_1 = pd.read_csv('./microdados_enamed_2025/microdados_enamed_2025_19-01-26/DADOS/Enade/microdados_enade_2025_arq1.txt', sep=';', encoding='latin1')

# %%
df_1.head()

# %%
df_5 = pd.read_csv('./microdados_enamed_2025/microdados_enamed_2025_19-01-26/DADOS/Enade/microdados_enade_2025_arq5.txt', sep=';', encoding='latin1')


# %%
df_5.head()
# %%
df_5['TP_SEXO'].unique()

# %%
df_6 = pd.read_csv('./microdados_enamed_2025/microdados_enamed_2025_19-01-26/DADOS/Enade/microdados_enade_2025_arq6.txt', sep=';', encoding='latin1')   

# %%
df_6.head()

# %%
df_9 = pd.read_csv('./microdados_enamed_2025/microdados_enamed_2025_19-01-26/DADOS/Enade/microdados_enade_2025_arq9.txt', sep=';', encoding='latin1')
# %%
df_9.head()
# %%
concatenado = pd.concat([df_1, df_5, df_6, df_9], axis = 1)

# %%
concatenado.head()
# %%
concatenado['TP_SEXO'].unique()
# %%
concatenado['NU_IDADE'].unique()
# %%
concatenado['QE_I03'].unique()
# %%
concatenado.to_excel('indicadores_enade_2025.xlsx', index=False)
# %%
