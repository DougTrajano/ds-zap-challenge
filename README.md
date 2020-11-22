# Data Science Challenge - Grupo ZAP

Autor: [Douglas Trajano](https://dougtrajano.github.io/resume/)

Este projeto faz parte do [Data Science Challenge](https://grupozap.github.io/cultura/challenges/data-science.html) do Grupo ZAP.

## Setup & Instalação

Este projeto foi desenvolvido no AWS SageMaker utilizando uma **ml.t3.xlarge**.

- **vCPU:** `4`
- **Memory:** `16GIB`

É necessário instalar os pacotes que estão listados no **requirements.txt**.

```
pip install -r requirements.txt
```

## App

Desenvolvemos uma aplicação interativa que permite apresentar melhor o projeto.

Você pode executar localmente após clonar o repositório com o comando abaixo:

```
streamlit run app.py
```

Ou acessar o link abaixo:

https://share.streamlit.io/dougtrajano/ds-zap-challenge/main/app.py

## Problema de negócio

Criar uma maneira automática de estimar um preço de venda para os apartamentos no dataset.

## Definição da estratégia

O projeto foi divido em 3 partes.

[code/processing.ipynb](code/processing.ipynb)
- Realiza o download, extração e preprocessamento dos datasets.

[code/exploratory_analysis.ipynb](code/exploratory_analysis.ipynb)
- Fornece algumas análises para interpretação dos dados.
- Deve ser utilizado com conjunto com o [pandas_profiling_report.html](pandas_profiling_report.html)

[code/modeling.ipynb](code/modeling.ipynb)
- Refinamento do dataset e treinamento do modelo.

A estratégia utilizada aqui foi realizar uma criteriosa seleção de features dos datasets (treino e teste), também foram coletadas features do dados geográficos fornecidos pelo Censo IBGE 2010.

Para explicar melhor a estratégia e os processos utilizados, acesse o app.

## Resultados

Os resultados e as respostas das perguntas solicitadas estão na página "Reports" do app.