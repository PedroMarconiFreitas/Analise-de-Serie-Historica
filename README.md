# ENAMED 2025 — Pipeline de ETL e Dashboard Interativo (Python + Power BI)

Projeto de ETL e análise aplicada a microdados educacionais do **ENAMED 2025 (INEP)**.  
O objetivo foi **extrair, padronizar, validar e integrar** diferentes arquivos de microdados, gerando uma base única para **análises e dashboards interativos** no Power BI, com recortes por **sexo, idade, raça/cor, UF, região, categoria administrativa da IES e tipo de inscrição**.

---

## Visão geral

- **Fonte:** Microdados oficiais do INEP (ENAMED/Enade)
- **ETL:** Python (pandas / numpy)
- **Entrega:** Base tratada em Excel + dashboards interativos no PowerBI
- **Foco analítico:** desempenho (média de acertos) geral e por áreas de conhecimento, com análises institucionais e territoriais

---

## Estrutura do projeto

```text
.
├── microdados_enamed_2025/
│   └── microdados_enamed_2025_19-01-26/
│       └── DADOS/Enade/
│           ├── microdados_enade_2025_arq1.txt
│           ├── microdados_enade_2025_arq3.txt
│           ├── microdados_enade_2025_arq5.txt
│           ├── microdados_enade_2025_arq6.txt
│           └── microdados_enade_2025_arq9.txt
├── etl_enamed_2025.py               # (sugestão) script do pipeline
├── indicadores_enamed_2025.xlsx     # saída do ETL (base tratada)
└── README.md
```

> **Nota:** os microdados não são versionados no repositório (tamanho/licença). O pipeline espera os arquivos `.txt` na estrutura acima.

---

## Pipeline de ETL (Python)

### 1) Leitura dos microdados (arquivos .txt)

O pipeline carrega múltiplos arquivos de microdados com separador `;` e encoding `latin1`.

- `arq3`: contém os **acertos por área** (`QT_ACERTO_AREA_1` a `QT_ACERTO_AREA_5`)
- `arq1, arq5, arq6, arq9`: contêm variáveis de **perfil e contexto** (sexo, idade, raça/cor, UF, região, categoria administrativa, tipo de inscrição)

Exemplo de leitura:

```python
import pandas as pd

df_3 = pd.read_csv(
    "./microdados_enamed_2025/microdados_enamed_2025_19-01-26/DADOS/Enade/microdados_enade_2025_arq3.txt",
    sep=";",
    encoding="latin1"
)
```

---

### 2) Seleção e renomeação dos acertos por área

O arquivo `arq3` é filtrado para manter apenas as colunas de acertos e, em seguida, renomeado para termos descritivos:

- `QT_ACERTO_AREA_1` → `Acertos_Clinica_Medica`
- `QT_ACERTO_AREA_2` → `Acertos_Pediatria`
- `QT_ACERTO_AREA_3` → `Acertos_Cirurgia_Geral`
- `QT_ACERTO_AREA_4` → `Acertos_Ginecologia_Obstetricia`
- `QT_ACERTO_AREA_5` → `Acertos_Medicina_Familia_Saude_Coletiva`

---

### 3) Integração dos arquivos de perfil/contexto

Os arquivos `arq1, arq5, arq6, arq9` são carregados e concatenados horizontalmente (`axis=1`), formando uma base única de características do participante/curso:

```python
import pandas as pd

indicadores = [1, 5, 6, 9]
df = {}

for i in indicadores:
    df[i] = pd.read_csv(
        f"./microdados_enamed_2025/microdados_enamed_2025_19-01-26/DADOS/Enade/microdados_enade_2025_arq{i}.txt",
        sep=";",
        encoding="latin1"
    )

df_concatenado = pd.concat(df.values(), ignore_index=False, axis=1)
```

---

### 4) Renomeação de variáveis e padronização (mapeamentos)

As variáveis do INEP foram renomeadas para facilitar leitura e uso no Power BI:

- `TP_INSCRICAO` → `Tipo de Inscrição`
- `TP_SEXO` → `Sexo`
- `NU_IDADE` → `Idade`
- `QE_I03` → `Raça ou Cor`
- `CO_UF_CURSO` → `UF do Curso`
- `CO_REGIAO_CURSO` → `Região do Curso`
- `CO_CATEGAD` → `Categoria Administrativa`

Em seguida, são aplicados dicionários de mapeamento para transformar códigos em rótulos interpretáveis (ex.: UF numérica → sigla; Sexo `M/F` → texto; Raça/cor por categorias).

---

### 5) Base final e exportação

Após padronizar variáveis e anexar os acertos por área, a base final é exportada para Excel e usada no Power BI:

```python
df_concatenado = pd.concat([df_concatenado, df_3], axis=1)
df_concatenado.to_excel("indicadores_enamed_2025.xlsx", index=False)
```

---

## Dashboards no Power BI

Com a base `indicadores_enamed_2025.xlsx`, foi construído um conjunto de páginas interativas para análise de desempenho por áreas e recortes por perfil, instituição e território.

### Indicadores e métricas

- Médias de acertos por área:
  - Clínica Médica
  - Pediatria
  - Cirurgia Geral
  - Ginecologia/Obstetrícia
  - Medicina de Família e Comunidade

Exemplo de medida DAX usada para calcular uma **média geral (média das áreas)**:

```DAX
Média Geral das Áreas =
AVERAGEX(
    {
        AVERAGE(Sheet1[Acertos_Cirurgia_Geral]),
        AVERAGE(Sheet1[Acertos_Clinica_Medica]),
        AVERAGE(Sheet1[Acertos_Ginecologia_Obstetricia]),
        AVERAGE(Sheet1[Acertos_Medicina_Familia_Saude_Coletiva]),
        AVERAGE(Sheet1[Acertos_Pediatria])
    },
    [Value]
)
```

### Filtros e segmentações (interatividade)

O relatório permite exploração dinâmica por:
- **Sexo**
- **Idade / Faixa etária**
- **Raça ou Cor**
- **UF do Curso**
- **Região do Curso**
- **Categoria Administrativa**
- **Tipo de Inscrição**

### Visuais principais

- **KPIs (cartões):** média geral, médias por área e total de participantes
- **Rankings:** Top/Bottom UFs por desempenho
- **Mapa:** distribuição territorial por UF
- **Barras:** desempenho por raça/cor, sexo e faixa etária
- **Matrizes:** comparativos região × categoria administrativa

---

## Entregas do projeto

- Pipeline em Python para:
  - leitura e integração de múltiplos arquivos
  - seleção de variáveis relevantes
  - padronização de variáveis categóricas com dicionários
  - validação por inspeção de categorias/valores
  - geração de base consolidada para BI
- Base final em Excel pronta para consumo no Power BI
- Dashboards interativos com análises:
  - **institucionais** (categoria administrativa)
  - **territoriais** (UF, região)
  - **equidade** (sexo, raça/cor, idade)

---

