import pandas as pd
import streamlit as st
from skopt.space import Real, Categorical, Integer


def modeling_page():
    st.title("Modeling")
    st.markdown("""
    Arquivos:

    - [code/modeling.py](https://github.com/DougTrajano/ds-zap-challenge/blob/main/code/modeling.py)
    - [code/modeling.ipynb](https://github.com/DougTrajano/ds-zap-challenge/blob/main/code/modeling.ipynb)

    ---

    ## Métricas

    Ao decidir quais métricas fariam mais sentido para o modelo, analisei as seguintes métricas:

    - Mean Squared Error - MSE
    - Mean Absolute Error - MAE
    - Mean Absolute Percentage Error - MAPE

    Uma descrição que eu usei para avaliar as métricas e que explica muito bem os objetivos de cada uma pode ser vista [aqui](https://www.mariofilho.com/as-metricas-mais-populares-para-avaliar-modelos-de-machine-learning/)

    Enfim, optei por usar a **Mean Squared Error - MSE**, pois no contexto de imóvel, grandes erros nas previsões irão gerar um impacto maior no negócio do que erros menores. Essa métrica irá elevar a diferença na predição ao quadrado, ou seja, quanto maior o erro do modelo, maior a penalização que ele sofrerá.

    ### Exemplo

    Imagine um imóvel de **R$ 500.000,00**.
    Se o modelo prever **R$ 450.000,00**, isto é melhor do que o modelo prever **R$ 200.000,00**.

    Também será usado a função `score()` do próprio modelo de regressão. Essa função aplica o [coeficiente de determinação - R²](https://pt.wikipedia.org/wiki/Coeficiente_de_determina%C3%A7%C3%A3o).

    Complementando nosso conjunto de métricas, pensei em uma métrica de negócio que fizesse mais sentido ao modelo.

    Criei então uma métrica binária que avaliará se a predição do modelo ficou entre 75% e 125% do valor real (os valores podem ser ajustados conforme necessário). Essa métrica terá o nome de `price_range_score()`

    ---

    ## Refinamento do dataset

    Para refinar o dataset, usei algumas técnicas que foram encapsuladas dentro da função `prep_modeling()`.

    Remoção de colunas inválidas (identificadas no exploratory_analysis.ipynb)
    - Essas variáveis tiveram problemas em seu processamento ou não agregarão valor ao modelo, por isso foram removidas.

    Conversão de variáveis categóricas para numéricas
    - Optei por desenvolver meu próprio Categorical Encoder, com ele é possível salvar um arquivo JSON que poderá ser usado posteriormente para explicar as conversões feitas pelo codec. Também existe uma função de `decode()`, foi implementada, mas não foi usada neste projeto.

    Dados faltantes
    - Para os dados faltantes, foi utilizado o [KNNImputer](https://scikit-learn.org/stable/modules/generated/sklearn.impute.KNNImputer.html) que preenche os dados faltantes utiizando geometria não euclidiana (nan_euclidean) como distância entre os dados vizinhos.

    ---

    ## Treinamento do modelo

    ### Feature importances

    Analisamos quais variáveis sensibilizam mais o nosso modelo e com isso, identificamos também como tirar mais proveito de variáveis hierarquizadas, por exemplo, geohash.
    """)

    st.image("images/feature_importances.png", use_column_width=True)

    st.markdown("""
    ### Split

    O conjunto de dados foi dividido em **train/test** com uma proporção de 0.67 e 0.33 respectivamente.

    ### Stratify

    Também foi aplicada uma estratificação com base na variável target `price` para garantir que tenhamos imóveis de vários grupos de preços (para isto foram gerados bins com base na estatística descritiva da própria variável).

    ### Cross-validation

    A técnica de [cross-validation](https://scikit-learn.org/stable/modules/cross_validation.html) nos permite avaliar melhor o modelo treinado, visto que o conjunto de treino é dividido em partes iguais que em algum momento, serão usadas como teste para o modelo.
    """)

    st.image("https://scikit-learn.org/stable/_images/grid_search_cross_validation.png",
             use_column_width=True)

    st.markdown("""
    ### Otimização de hiperparâmetros

    Para encontrar os melhores hiperparâmetros, usamos a [BayesSearchCV](https://scikit-optimize.github.io/stable/modules/generated/skopt.BayesSearchCV.html) que aplicará *gaussian process* para otimizar a procura dos hiperparâmetros.
    
    Abaixo podemos ver os espaços para cada hiperparâmetro testado.
    """)

    st.json({
        "max_depth": "Integer(5, 15)",
        "learning_rate": "Real(3e-4, 3e-1, prior='log-uniform')",
        "objective": "Categorical(['reg:squarederror', 'reg:gamma', 'reg:tweedie'])",
        "booster": "Categorical(['gbtree', 'dart'])",
        "reg_alpha": "Real(0.01, 1.0, prior='log-uniform')",
        "reg_lambda": "Real(0.5, 2.0, prior='log-uniform')",
        "colsample_bytree": "Real(0.01, 1.0, prior='log-uniform')",
        "colsample_bylevel": "Real(0.01, 1.0, prior='log-uniform')",
        "colsample_bynode": "Real(0.01, 1.0, prior='log-uniform')",
        "subsample": "Real(0.01, 1.0, prior='log-uniform')"
    })

    st.markdown("Em 200 interações, encontramos os seguintes hiperparêmtros:")

    st.json({'objective': 'reg:tweedie',
             'base_score': 0.5,
             'booster': 'gbtree',
             'colsample_bylevel': 1.0,
             'colsample_bynode': 1.0,
             'colsample_bytree': 1.0,
             'gamma': 0,
             'gpu_id': -1,
             'importance_type': 'gain',
             'interaction_constraints': '',
             'learning_rate': 0.3,
             'max_delta_step': 0,
             'max_depth': 5,
             'min_child_weight': 1,
             'missing': 'nan',
             'monotone_constraints': '()',
             'n_estimators': 100,
             'n_jobs': 0,
             'num_parallel_tree': 1,
             'random_state': 0,
             'reg_alpha': 1.0,
             'reg_lambda': 0.5,
             'scale_pos_weight': None,
             'subsample': 1.0,
             'tree_method': 'exact',
             'validate_parameters': 1,
             'verbosity': None})

    st.markdown("""
    ---

    ## Modelo

    Usei o algoritmo [XGBRegressor](https://xgboost.readthedocs.io/en/latest/python/python_api.html#xgboost.XGBRegressor) neste projeto.

    É um algoritmo versátil e que atende vários problemas de negócio.

    Como trabalho futuro, seria interessante testar outros algoritmos também.
    """)

    st.image("images/validation_loss.png", use_column_width=True)

    st.markdown("""
    ---

    ## Avaliação

    Como visto acima, usei duas métricas: **RME** e **R²** do próprio algoritmo.

    Os resultados obtidos com um modelo otimizado no dataset de valiação foram:
    """)

    st.json({'mse': 128522463228.4819, 'r2_score': 0.8647867673514608})

    st.image("images/R2_score.png", use_column_width=True)

    st.markdown("""
    O **MSE** serve apenas para otimização do algoritmo, analisando o **R²** tivemos um bom resultado para uma primeira imersão do projeto.

    O resultado do **cross-validation** foi:

    | Fold | Score |
    | - | - |
    | 1 | 0.9119 |
    | 2 | 0.9116 |
    | 3 | 0.9190 |
    | 4 | 0.8995 |
    | 5 | 0.5486 |

    Precisamos entender melhor o motivo pelo qual o modelo não performou tão bem na última fold.
    
    Clicando no botão abaixo é possível ver 50 predições que o modelo realizou, comparando o **valor real** e o **valor predito**.

    """)

    if st.button("Ver predições"):
        df_preds = pd.DataFrame([{'Prediction': 'R$ 299,617.50', 'Real': 'R$ 315,000.00'},
                                 {'Prediction': 'R$ 1,175.22',
                                     'Real': 'R$ 2,800.00'},
                                 {'Prediction': 'R$ 220,586.39',
                                  'Real': 'R$ 301,000.00'},
                                 {'Prediction': 'R$ 461,148.47',
                                  'Real': 'R$ 392,000.00'},
                                 {'Prediction': 'R$ 3,997.23',
                                     'Real': 'R$ 3,849.00'},
                                 {'Prediction': 'R$ 478,642.22',
                                  'Real': 'R$ 486,499.00'},
                                 {'Prediction': 'R$ 345,251.19',
                                  'Real': 'R$ 343,000.00'},
                                 {'Prediction': 'R$ 319,405.66',
                                  'Real': 'R$ 371,000.00'},
                                 {'Prediction': 'R$ 344,907.62',
                                  'Real': 'R$ 364,000.00'},
                                 {'Prediction': 'R$ 1,868,469.00',
                                  'Real': 'R$ 2,050,999.00'},
                                 {'Prediction': 'R$ 265,740.72',
                                  'Real': 'R$ 203,000.00'},
                                 {'Prediction': 'R$ 426,435.66',
                                  'Real': 'R$ 460,039.00'},
                                 {'Prediction': 'R$ 289,741.94',
                                  'Real': 'R$ 350,000.00'},
                                 {'Prediction': 'R$ 269,690.34',
                                  'Real': 'R$ 259,699.00'},
                                 {'Prediction': 'R$ 195,506.27',
                                  'Real': 'R$ 224,000.00'},
                                 {'Prediction': 'R$ 701,194.62',
                                  'Real': 'R$ 910,000.00'},
                                 {'Prediction': 'R$ 380,444.78',
                                  'Real': 'R$ 409,500.00'},
                                 {'Prediction': 'R$ 2,231,330.75',
                                  'Real': 'R$ 2,450,000.00'},
                                 {'Prediction': 'R$ 847,415.31',
                                  'Real': 'R$ 840,000.00'},
                                 {'Prediction': 'R$ 250,960.81',
                                  'Real': 'R$ 210,000.00'},
                                 {'Prediction': 'R$ 2,096,365.25',
                                  'Real': 'R$ 2,374,400.00'},
                                 {'Prediction': 'R$ 390,016.12',
                                  'Real': 'R$ 448,000.00'},
                                 {'Prediction': 'R$ 5,694,209.00',
                                  'Real': 'R$ 4,094,999.00'},
                                 {'Prediction': 'R$ 378,576.50',
                                  'Real': 'R$ 417,900.00'},
                                 {'Prediction': 'R$ 677,944.56',
                                  'Real': 'R$ 840,000.00'},
                                 {'Prediction': 'R$ 285,764.00',
                                  'Real': 'R$ 273,000.00'},
                                 {'Prediction': 'R$ 214,485.86',
                                  'Real': 'R$ 157,500.00'},
                                 {'Prediction': 'R$ 305,092.50',
                                  'Real': 'R$ 297,500.00'},
                                 {'Prediction': 'R$ 285,173.75',
                                  'Real': 'R$ 276,500.00'},
                                 {'Prediction': 'R$ 351,125.81',
                                  'Real': 'R$ 332,500.00'},
                                 {'Prediction': 'R$ 295,060.12',
                                  'Real': 'R$ 394,398.00'},
                                 {'Prediction': 'R$ 1,796.97',
                                     'Real': 'R$ 3,500.00'},
                                 {'Prediction': 'R$ 232,911.47',
                                  'Real': 'R$ 192,500.00'},
                                 {'Prediction': 'R$ 817,136.69',
                                  'Real': 'R$ 584,500.00'},
                                 {'Prediction': 'R$ 372,465.59',
                                  'Real': 'R$ 258,999.00'},
                                 {'Prediction': 'R$ 254,315.53',
                                  'Real': 'R$ 230,999.00'},
                                 {'Prediction': 'R$ 3,828,712.25',
                                  'Real': 'R$ 2,275,000.00'},
                                 {'Prediction': 'R$ 454,967.28',
                                  'Real': 'R$ 280,000.00'},
                                 {'Prediction': 'R$ 9,293.00',
                                     'Real': 'R$ 17,500.00'},
                                 {'Prediction': 'R$ 2,536,921.50',
                                  'Real': 'R$ 2,520,000.00'},
                                 {'Prediction': 'R$ 3,796.08',
                                     'Real': 'R$ 3,779.00'},
                                 {'Prediction': 'R$ 347,148.28',
                                  'Real': 'R$ 350,000.00'},
                                 {'Prediction': 'R$ 225,177.89',
                                  'Real': 'R$ 154,000.00'},
                                 {'Prediction': 'R$ 321,149.09',
                                  'Real': 'R$ 273,000.00'},
                                 {'Prediction': 'R$ 1,703.32',
                                     'Real': 'R$ 1,575.00'},
                                 {'Prediction': 'R$ 1,565,395.38',
                                  'Real': 'R$ 1,924,999.00'},
                                 {'Prediction': 'R$ 526,470.31',
                                  'Real': 'R$ 448,000.00'},
                                 {'Prediction': 'R$ 193,677.59',
                                  'Real': 'R$ 185,500.00'},
                                 {'Prediction': 'R$ 250,241.92',
                                  'Real': 'R$ 244,999.00'},
                                 {'Prediction': 'R$ 276,456.31', 'Real': 'R$ 261,099.00'}])

        st.table(df_preds)

    st.markdown("""
    ### Price range score

    Como explicado acima, usamos a `price_range_score()` como uma métrica de negócio.

    No modelo otimizado, obtivemos um score de **82,83%**, nós temos uma estimativa próxima do valor real do imóvel.

    ### Faixas de preços
    
    Pelo que podemos perceber no gráfico do R² temos algumas faixas de preço que precisam de atenção: 224k~409k e 409k~770k.
    
    ---

    ## Reprodutibilidade
    
    Em **modeling.ipynb** foi definido o `seed` como `1993`.

    Também foram colocadas as versões dos pacotes no `requirements.txt`, pois podem existir alterações nos resultados obtidos de acordo com as versões usadas.
    """)
