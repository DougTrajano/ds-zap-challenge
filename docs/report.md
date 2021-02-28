# Report

The model developed in this project predicts sales prices for apartments based on ads at [www.zapimoveis.com.br](https://www.zapimoveis.com.br/).

On this page, you can learn more about how the model performs on different aspects of your training dataset, and what kinds of apartments you should expect the model to perform well or poorly on.

---

## Model description

### Input

| Variable | Type |
| - | - |
| usableAreas | long |
| parkingSpaces | long |
| suites | long |
| bathrooms | long |
| totalAreas | double |
| bedrooms | long |
| publicationType | long |
| businessType | long |
| yearlyIptu | long |
| monthlyCondoFee | long |
| has_gym | boolean |
| has_garden | boolean |
| has_pool | boolean |
| has_lobby | boolean |
| has_partyRoom | boolean |
| has_balcony | boolean |
| has_playground | boolean |
| has_grill | boolean |
| has_games | boolean |
| has_closet | boolean |
| has_furnitures | boolean |
| has_toilet | boolean |
| total_dom_part_improvisados | long |
| renda_nom_dom_part | long |
| renda_nom_dom_part_perm | double |
| renda_nom_dom_part_imp | long |
| renda_nom_dom_sal_baixo1 | long |
| renda_nom_dom_sal_baixo2 | long |
| renda_nom_dom_sal_baixo3 | long |
| renda_nom_dom_sal_baixo4 | long |
| renda_nom_dom_sal_medio1 | long |
| renda_nom_dom_sal_medio2 | long |
| renda_nom_dom_sal_medio3 | long |
| renda_nom_dom_sal_alto1 | long |
| renda_nom_dom_sal_alto2 | long |
| renda_nom_dom_sem_rendimento | long |
| ident_logradouro_proprios | long |
| nao_ident_logradouro_proprios | long |
| ident_logradouro_alugados | long |
| nao_ident_logradouro_alugados | long |
| ilum_publica_proprios | long |
| nao_ilum_publica_proprios | long |
| ilum_publica_alugados | long |
| nao_ilum_publica_alugados | long |
| geohash_5 | long |

### Output

| Variable | Type |
| - | - |
| price | double |

### Model architecture

XGBoost regression

---

## Performance

Performance evaluated for sales price at training dataset.

Two performance metrics are reported:

- [Rª (coefficient of determination)](https://en.wikipedia.org/wiki/Coefficient_of_determination): 84.64% 
- [Explained variation](https://en.wikipedia.org/wiki/Explained_variation): Pending

Performance evaluated on 33% of training set that was not seen by the model.

---

## Limitations

Pending