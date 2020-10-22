# Modeling



## Métricas

Ao decidir qual métrica faria mais sentido para o modelo, analisei as seguintes métricas:

- Mean Squared Error - MSE
- Mean Absolute Error - MAE
- Mean Absolute Percentage Error - MAPE

Uma descrição que eu usei e que explica o objetivo de cada métrica pode ser vista [aqui](https://www.mariofilho.com/as-metricas-mais-populares-para-avaliar-modelos-de-machine-learning/)

Enfim, optei por usar a **Mean Squared Error - MSE**, pois no contexto de imóvel, grandes erros nas previsões irão gerar um impacto maior no negócio do que erros menores.

Exemplo:

Imagine um imóvel de R$ 500.000,00.
Se o modelo prever R$ 450.000,00, isto é melhor do que o modelo prever R$ 200.000,00.

Também será usado a função `score()` do próprio modelo de regressão.

## Treinamento do modelo