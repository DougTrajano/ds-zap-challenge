import streamlit as st
import pandas as pd

def features_page():
    st.title("Features selection")

    st.markdown("""
    Arquivos:

    - code/processing.py
    - code/processing.ipynb
    - code/censo_ibge.py

    ---

    Aqui vamos falar sobre a seleção de features para o modelo.

    Utilizamos features geradas pelos datasets fornecidos pelo Grupo ZAP e features fornecidas pelo Censo IBGE 2010.

    O modelo de dados pode ser verificado em [code/data_models.py](code/data_models.py)

    ---

    ## IBGE - Setor censitário

    Fazemos o cruzamos da localização geográfica do imóvel com dados do Censo 2010 fornecido pelo IBGE.

    Os dados do IBGE são fornecidos em CSV ou EXCEL e possuem uma documentação para informar o conceito de cada variável disponível que normalmente seguem o padrão `V001`, `V002`, `etc.`.

    Para o cruzamos da base foi criada uma classe chamada `CensoData()` que está disponível no arquivo **code/censo_ibge.py**.

    Na função `get_censo_features()` é necessário informar um `census_code` (Cod_setor) e o arquivo censo_config que mapeia quais arquivos serão analisados e quais nomes as variáveis serão convertidas.

    O IBGE fornece 26 arquivos apenas para a cidade de São Paulo, ou seja, é uma fonte de dados extremamente rica, principalmente para este contexto (imobiliário).

    Nessa primeira versão usamos apenas 2 arquivos e algumas variáveis dentro desses arquivos.

    ### DomicilioRenda_SP1.csv

    | Variável IBGE | Nome da feature gerada   |
    |------|----------------------------------|
    | V001 | total\_dom\_part\_improvisados |
    | V002 | renda\_nom\_dom\_part            |
    | V003 | renda\_nom\_dom\_part\_perm      |
    | V004 | renda\_nom\_dom\_part\_imp       |
    | V005 | renda\_nom\_dom\_sal\_baixo1     |
    | V006 | renda\_nom\_dom\_sal\_baixo2     |
    | V007 | renda\_nom\_dom\_sal\_baixo3     |
    | V008 | renda\_nom\_dom\_sal\_baixo4     |
    | V009 | renda\_nom\_dom\_sal\_medio1     |
    | V010 | renda\_nom\_dom\_sal\_medio2     |
    | V011 | renda\_nom\_dom\_sal\_medio3     |
    | V012 | renda\_nom\_dom\_sal\_alto1      |
    | V013 | renda\_nom\_dom\_sal\_alto2      |
    | V014 | renda\_nom\_dom\_sem\_rendimento |

    ### Entorno01_SP1.csv

    | Variável IBGE | Nome da feature gerada      |
    |------|----------------------------------|
    | V002 | ident\_logradouro\_proprios |
    | V003 | nao\_ident\_logradouro\_proprios |
    | V004 | ident\_logradouro\_alugados      |
    | V005 | nao\_ident\_logradouro\_alugados |
    | V008 | ilum\_publica\_proprios          |
    | V009 | nao\_ilum\_publica\_proprios     |
    | V010 | ilum\_publica\_alugados          |
    | V011 | nao\_ilum\_publica\_alugados     |

    ### Exemplo

    Considerando o Cod_setor: **355030835000002**

    Temos as seguintes features:

    ```
    {
        "total_dom_part_improvisados": "0",
        "renda_nom_dom_part": "3102115",
        "renda_nom_dom_part_perm": "3102115",
        "renda_nom_dom_part_imp": "0",
        "renda_nom_dom_sal_baixo1": "0",
        "renda_nom_dom_sal_baixo2": "0",
        "renda_nom_dom_sal_baixo3": "1",
        "renda_nom_dom_sal_baixo4": "4",
        "renda_nom_dom_sal_medio1": "17",
        "renda_nom_dom_sal_medio2": "18",
        "renda_nom_dom_sal_medio3": "39",
        "renda_nom_dom_sal_alto1": "87",
        "renda_nom_dom_sal_alto2": "83",
        "renda_nom_dom_sem_rendimento": "11",
        "ident_logradouro_proprios": "164",
        "nao_ident_logradouro_proprios": "0",
        "ident_logradouro_alugados": "79",
        "nao_ident_logradouro_alugados": "0",
        "ilum_publica_proprios": "164",
        "nao_ilum_publica_proprios": "0",
        "ilum_publica_alugados": "79",
        "nao_ilum_publica_alugados": "0"
    }
    ```

    ---

    ## Description

    Para a descrição do texto, foi realizada um simples mapeamento de palavras.

    Acredito que a descrição do texto pode ser explorada com maior atenção no futuro, pois existem vários dados adicionais lá que agregarão valor ao modelo no futuro.

    As features geradas com base na descrição foram:

    - has_gym
    - has_garden
    - has_pool
    - has_sauna
    - has_lobby
    - has_partyRoom
    - has_balcony
    - has_playground
    - has_grill
    - has_games
    - has_closet
    - has_elevator
    - has_furnitures
    - has_toilet

    ---

    ## Geohash

    Geohash é um sistema de código para geolocalizações (latitude e longitude). Mais informações podem ser obtidas [aqui](https://en.wikipedia.org/wiki/Geohash).

    | Geohash | Precisão | Dimensão
    | - | - | - |
    | wecnvgm2re3u | 12 | ~ 3.7cm x 1.8cm |
    | wecnvgm2re3 | 11 | ~ 14.9cm x 14.9cm |
    | wecnvgm2re |10 | ~ 1.19m x 0.60m |
    | wecnvgm2r | 9 | ~ 4.78m x 4.78m |
    | wecnvgm2 | 8 | ~ 38.2m x 19.1m |
    | wecnvgm | 7 | ~ 152.8m x 152.8m |
    | wecnvg | 6 | ~ 1.2km x 0.61km |
    | wecnv | 5 | ~ 4.9km x 4.9km |
    | wecn | 4 | ~ 39km x 19.5km |
    | wec | 3 | ~ 156km x 156km |
    | we | 2 | ~ 1,251km x 652km |
    | w | 1 | ~ 5.004km x 5,004km |

    ### Como usamos isto no modelo?

    O geohash foi utilizado como uma forma de agrupar latitude e longitude para ser usado como uma *feature* de localização agrupada.
    
    """)

    st.write("## Localizações dos imóveis")
    df = pd.read_feather("data/processed/geolocations.feather")
    st.map(df)