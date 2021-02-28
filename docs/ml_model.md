# Machine Learning Model - [MLflow](https://www.mlflow.org/)

The last model (a XGBoost Regressor) was trained on **February 27 | 2021**.

## Scores

### Base model

| Name | Value |
| - | - |
| MSE | 176603598239.7 |
| R2 score (test set) | 0.814 |


### Optimized model

| Name | Value |
| - | - |
| MSE | 145975917532 |
| R2 score (test set) | 0.8464 |
| R2 score (cross-validation) | 0.8253 |

---

## Hyperparameters

| Hyperparameter | Value |
| - | - |
| objective | "reg:squarederror" |
| base_score | 0.5 |
| booster | "dart" |
| colsample_bylevel | 0.45089899886494966 |
| colsample_bynode | 1.0 |
| colsample_bytree | 0.8070554145088148 |
| gamma | 0 |
| gpu_id | -1 |
| importance_type | "gain" |
| interaction_constraints | "" |
| learning_rate | 0.1696738106834926 |
| max_delta_step | 0 |
| max_depth | 5 |
| min_child_weight | 1 |
| missing | nan |
| monotone_constraints | "()" |
| n_estimators | 1000 |
| n_jobs | 0 |
| num_parallel_tree | 1 |
| random_state | 1993 |
| reg_alpha | 0.21974995218922627 |
| reg_lambda | 1.2579087520356529 |
| scale_pos_weight | 1 |
| subsample | 1.0 |
| tree_method | "exact" |
| validate_parameters | 1 |
| verbosity | None |

---

## Machine Learning Lifecycle

[MLflow](https://www.mlflow.org/) is an open source platform for the machine learning lifecycle.

![](https://raw.githubusercontent.com/DougTrajano/ds-zap-challenge/main/docs/images/mlflow_detailed.png)

### Tracking experiments

The model(s) trained in this project was tracked with mlflow API.

The files involve with MLflow are in `/mlruns` folder.

### Viewing the Tracking UI

You can see all experiments in MLflow Tracking UI, just type this command in the terminal of the project directory.

```
mlflow ui
```