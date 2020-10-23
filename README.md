# Data Science Challenge - Grupo ZAP

Autor: [Douglas Trajano](https://dougtrajano.github.io/resume/)

Este projeto faz parte do [Data Science Challenge](https://grupozap.github.io/cultura/challenges/data-science.html) realizado no processo seletivo para cientista de dados no Grupo ZAP.

## Setup & Instalação

O projeto necessita de uma máquina com +- 20GB de memória.

Este projeto foi desenvolvido no AWS SageMaker utilizando uma **ml.m5.2xlarge**.

- **vCPU:** `8`
- **Memory:** `32GIB`

É necessário instalar os pacotes que estão listados no **requirements.txt**.

```
pip install -r requirements.txt
```

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

Para explicar melhor a estratégia e os processos utilizados, existe uma pasta na raiz do repositório chamada [docs](docs) com mais informações sobre as *features* utilizadas, modelos, etc.

## Resultados

Os resultados e as respostas das perguntas solicitadas estão no arquivo [docs/reports.md](docs/reports.md)
