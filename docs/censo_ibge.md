# IBGE Censo 2010

Fazemos o cruzamos da localização geográfica do imóvel com dados do Censo 2010 fornecido pelo IBGE.

Os dados do IBGE são fornecidos em CSV ou EXCEL e possuem uma documentação para informar o conceito de cada variável disponível que normalmente seguem o padrão `V001`, `V002`, `etc.`.

Para o cruzamos da base foi criada uma classe chamada `CensoData()` que está disponível no arquivo **code/censo_ibge.py**.

Na função `get_censo_features()` é necessário informar um `census_code` (Cod_setor) e o arquivo censo_config que mapeia quais arquivos serão analisados e quais nomes as variáveis serão convertidas.

Como este trabalho é uma POC/challenge, usamos uma definição simples usando apenas 2 dos 26 arquivos disponíveis.


```
censo_config = {
    "DomicilioRenda_SP1.csv": {
        "V001": "total_dom_part_improvisados",
        "V002": "renda_nom_dom_part",
        "V003": "renda_nom_dom_part_perm",
        "V004": "renda_nom_dom_part_imp",
        "V005": "renda_nom_dom_sal_baixo1",
        "V006": "renda_nom_dom_sal_baixo2",
        "V007": "renda_nom_dom_sal_baixo3",
        "V008": "renda_nom_dom_sal_baixo4",
        "V009": "renda_nom_dom_sal_medio1",
        "V010": "renda_nom_dom_sal_medio2",
        "V011": "renda_nom_dom_sal_medio3",
        "V012": "renda_nom_dom_sal_alto1",
        "V013": "renda_nom_dom_sal_alto2",
        "V014": "renda_nom_dom_sem_rendimento"
    },
    "Entorno01_SP1.csv": {
        "V002": "ident_logradouro_proprios",
        "V003": "nao_ident_logradouro_proprios",
        "V004": "ident_logradouro_alugados",
        "V005": "nao_ident_logradouro_alugados",
        "V008": "ilum_publica_proprios",
        "V009": "nao_ilum_publica_proprios",
        "V010": "ilum_publica_alugados",
        "V011": "nao_ilum_publica_alugados"
    }
}
```

## Exemplo

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

## Considerações

A exploração dos dados do IBGE Censo 2010 seja um trabalho futuro que poderá aprimorar os resultados do modelo final.