import json
import warnings
warnings.filterwarnings("ignore")

import collections
import numpy as np
import pandas as pd
import xgboost as xgb
from typing import Tuple
from sklearn.impute import KNNImputer
from sklearn.metrics import mean_squared_error

from .categorical_encoder import CategoricalEncoder

def flatten(d, sep="."):

    obj = collections.OrderedDict()

    def recurse(t, parent_key=""):

        if isinstance(t, list):
            for i in range(len(t)):
                recurse(t[i], parent_key + sep + str(i)
                        if parent_key else str(i))
        elif isinstance(t, dict):
            for k, v in t.items():
                recurse(v, parent_key + sep + k if parent_key else k)
        else:
            obj[parent_key] = t

    recurse(d)

    return dict(obj)

def read_json(path):
    "Read a JSON file."
    with open(path) as json_file:
        data = json.load(json_file)
    return data

def split_dataset(X, n_range=20000):
    """
    Split X into smaller parts.
    
    Arguments:
    - X: dataset to be splitted.
    - n_range (int, optional): Lengh of each part.
    
    Output:
    - List with parts of X
    """
    datasets = [X[x:x+n_range] for x in range(0, len(X), n_range)]
    
    return datasets

def prep_modeling(X, invalid_cols=None, geohash=None, generate_encoder=True, catenc_path='categorical_features.json', large_dataset=True, knn_neighbors=5, seed=1993):
    """Prepare dataset to modeling.
    
    Arguments:
    X (pd.DataFrame): Dataset
    invalid_cols (list, optional): Invalid columns to be removed.
    geohash (list or int, optional): Reduce geohash delimiter.
    generate_encoder (bool): If True, generate_encoder, If False, load encoder.
    catenc_path (str): Path to save a JSON file used by CategoricalEncoder().
    large_dataset (bool, optional): If working with a large dataset, we need to split the dataset to KNNImputer.
    knn_neighbors (int): Number of neighboring samples to use for imputation.
    seed (int, optional): Random seed
    """

    # Geohash
    if isinstance(geohash, list):
        for i in geohash:            
            key = "geohash_{}".format(i)
            X[key] = [str(g)[:i] for g in X["geohash"]]
        X.drop(columns=["geohash"], inplace=True, errors="ignore")
    elif isinstance(geohash, int):
        X["geohash"] = [str(g)[:geohash] for g in X["geohash"]]
        
    # Remove invalid columns
    if isinstance(invalid_cols, list):
        X.drop(columns=invalid_cols, inplace=True, errors="ignore")

    # Categorical encoding
    cat_features = X.select_dtypes(include=['object']).columns.tolist()

    encoder = CategoricalEncoder(catenc_path)
    
    if generate_encoder:
        encoder.generate(X, cat_features)
    else:
        encoder.load()
        
    X = encoder.transform(X, cat_features)

    # Missing values
    imputer = KNNImputer(n_neighbors=knn_neighbors)
    
    if large_dataset:
        Xs = split_dataset(X)
        X_new = []
        
        for x in Xs:
            x = imputer.fit_transform(x)
            X_new = X_new + list(x)
            X = pd.DataFrame(data=X_new, columns=X.columns)
            
    else:
        X = imputer.fit_transform(X)
    
    return X

def check_prediction(model, X, y, verbose=False):
    """
    Compare real and prediction values.
    
    Arguments:
    - model: model with .predict() function.
    - X: X values
    - y: y values
    
    Output:
    Nothing, it'll print on console
    """
    if isinstance(X, pd.Series):
        X = pd.DataFrame(X).transpose()
        
    pred = model.predict(X)
    
    if verbose:
        print("Prediction:", 'R$ {:,.2f}'.format(pred[0]))
        print("Real:", 'R$ {:,.2f}'.format(y))
    
    return {"Prediction": 'R$ {:,.2f}'.format(pred[0]), "Real": 'R$ {:,.2f}'.format(y)}

def test_prediction(test, ids, model):
    """
    Function to apply predict on test dataset.
    
    Arguments:
    - test (pd.DataFrame): Test dataset.
    - ids (list): ID for each row in test dataset.
    - model (XGBRegressor model): Trained model.
    
    Output:
    List of dicts like {"id": "X", "price": 100.0}
    """
    result = []
    for i in range(len(test)):
        pred = model.predict(test.iloc[[i]])[0]
        result.append({"id": ids[i], "price": pred})
        
    return result

def mse_score(predt: np.ndarray, dtrain: xgb.DMatrix) -> Tuple[str, float]:
    """Mean Squared Error - MSE for XGBRegressor algorithm."""
    y = dtrain.get_label()
    predt[predt < -1] = -1 + 1e-6
    return 'mse', mean_squared_error(y, predt)