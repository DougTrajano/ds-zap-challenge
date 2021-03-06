# Reports pt_BR

## Predição na base de teste

O arquivo com as predições na base de teste está na raiz do projeto: **predictions.csv**

## Explicação da solução

A solução implementada basicamente possui três partes.

processing
> Download, extração e processamento dos dados.

exploratory_analysis
> Análise exploratória e recomendações para refinamento do dataset.

modeling
> Refinamento do dataset, treinamento do modelo.

Mais informações podem ser obtidas nas páginas: **Features selection** e **Modeling**.

## Código fonte da solução

> https://github.com/DougTrajano/ds-zap-challenge

## Perguntas finais

Você utilizaria a métrica escolhida para seleção de modelo também para comunicar os resultados para usuários e stakeholders internos? Em caso negativo, qual outra métrica você utilizaria? Por quê?

> No treinamento e avaliação do modelo nós usamos duas métricas **MSE** e **R²**.
> 
> O MSE é útil apenas para otimização do modelo, enquanto o R² nos ajudou a comparar a evolução e quais modelos performaram melhor.
>
> Para comunicar os resultado aos stakeholders, eu utilizaria o R² em conjunto com outras duas métricas de negócio:
> - Um score binário baseado em ranges de preço em que o modelo pode estimar o preço do imóvel. Ex: Se o imóvel custar **R$ 150.000,00** e o modelo estimar entre **R$ 125.000,00** e **R$ 175.000,00**, ele foi assertivo neste sentido.
> - Métrica de utilização do modelo. Provavelmente ele seria disponibilizado como recomendação para os usuários do ZAP, sendo assim, uma métrica de sucesso seria acompanhar quantos usuários utilizaram a recomendação de preço fornecida pelo modelo.

Em quais bairros ou em quais faixas de preço o seu modelo performa melhor? Deixe claro como chegou a esse resultado.

> Como pode ser visto na página **Modeling**, criei uma métrica binária que avalia se o preço predito está entre 75% e 125% do valor real do imóvel.
> 
> Com isso, analisamos a divisão do preço do imóvel onde foi possível perceber uma maior dificuldade do modelo em estimar os preços dos imóveis entre R$ 409.045,00 e R$ 770.000,00.
>
> A tabela completa está disponível em **Modeling**.

Se você tivesse que estimar o valor dos imóveis com apenas 3 campos, quais seriam eles? Como chegou a esses campos?

> Eu usaria os campos abaixo, pois são 2 campos bem descritivos do imóvel e uma referente a localização do imóvel.
> - `usableAreas`
> - `geohash_5`
> - `monthlyCondoFee`

Entre os clientes do Grupo ZAP temos pessoas que anunciam imóveis e pessoas que buscam imóveis. Como a sua solução poderia auxiliar cada tipo de cliente?

> Para os clientes que anunciam imóveis, podemos recomendar um **preço sugerido**.
> 
> Para os clientes que buscam imóveis, podemos informá-los sobre possíveis preços elevados para determinado tipo de imóvel ou sugerir imóveis que estejam abaixo do preço estimado pelo modelo.