import json
import pandas as pd
import numpy as np
import warnings
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import KNNImputer
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

import xgboost as xgb
from typing import Tuple

warnings.filterwarnings("ignore")


class CategoricalEncoder:
    def __init__(self, path: str = "categorical_features.json"):
        self.codec = None
        self.path = path
        
    def load(self):
        """Load JSON file"""
        with open(self.path) as json_file:
            self.codec = json.load(json_file)
            
    def generate(self, df: pd.DataFrame, cat_features: list):
        """Generate codec and save JSON file."""
        cat_encoding = {}
        for col in cat_features:
            cat_encoding[col] = self.encode(df[col])
        
        self.codec = cat_encoding
        
        with open(self.path, 'w') as outfile:
            json.dump(cat_encoding, outfile)
        
    def encode(self, series: pd.Series, n_start: int = 1):
        """Encode a pd.Series."""
        if not isinstance(series, pd.Series):
            series = pd.Series(series)

        uniques = series.unique().tolist()

        encode = {}
        i = n_start
        for cat in uniques:
            encode[cat] = i
            i += 1

        return encode
    
    def _transform(self, feature_name: str, value: str):
        """Encode categorical feature in numeric."""
        if not isinstance(self.codec, dict):
            raise ValueError("CategoricalEncoder not loaded.")
        
        if not value in self.codec[feature_name].keys():
            value = self.add_value(feature_name, value)
        else:
            value = self.codec[feature_name][value]
            
        return value
    
    def transform(self, df: pd.DataFrame, cat_features: list):
        """Transform categorical features of a DataFrame in numeric."""
        for col in cat_features:
            if col in df.columns:
                u_values = df[col].unique()
                for value in u_values:
                    cat_value = self._transform(col, value)
                    df[col].replace(value, cat_value, inplace=True)
                    
        return df
    
    def decode(self, feature_name: str, value: str):
        """Decode numeric values to categorical features."""
        for key in self.codec[feature_name].keys():
            if cat.codec[feature_name][key] == value:
                return key
    
    def add_value(self, feature_name: str, value: str):
        """Add a new value to codec."""
        last_value = max(self.codec[feature_name].values())
        i = last_value + 1
        self.codec[feature_name][value] = i
        
        with open(self.path, 'w') as outfile:
            json.dump(self.codec, outfile)
            
        return i

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

def prep_modeling(X, invalid_cols=None, geohash=None, generate_encoder=True, large_dataset=True, knn_neighbors=5, seed=1993):
    """Prepare dataset to modeling.
    
    Arguments:
    X (pd.DataFrame): Dataset
    invalid_cols (list, optional): Invalid columns to be removed.
    geohash (list or int, optional): Reduce geohash delimiter.
    generate_encoder (bool): If True, generate_encoder, If False, load encoder.
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

    encoder = CategoricalEncoder()
    
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

def bins_y(y):
    """
    Function to create bins based on y_stats.
    
    Arguments:
    - y (array, list): target values
    
    Output:
    y_binned [0, 1, 2, 3]
    """
    y_binned = []
    
    for i in y:
        if i <= 224000:
            y_binned.append(0)
        elif i <= 409500:
            y_binned.append(1)
        elif i <= 770000:
            y_binned.append(2)
        else:
            y_binned.append(3)
    return y_binned

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

def test_prediction(test, model):
    """
    Function to apply predict on test dataset.
    
    Arguments:
    - test (pd.DataFrame):
    - model (XGBRegressor model): Trained model
    
    Output:
    List of dicts like {"id": "X", "price": 100.0}
    """
    result = []
    for i in range(len(test)):
        pred = model.predict(X_test.iloc[[i]])[0]
        result.append({"id": X_test.iloc[[i]]["_id"], "price": pred})
        
    return result

def price_range_score(y_pred, y_true, lower=0.75, higher=1.25):
    """
    Provide a binary metric based on lower and higher values.
    
    Arguments:
    - y_pred (): Predicted price
    - y_true (): Real price
    - lower (float, default=0.75):
    - higher (float, default=1.25):
    
    Output:
    Score (int): 1 or 0
    """
    y_l = y_true * 0.75
    y_h = y_true * 1.25
    
    if y_pred >= y_l and y_pred <= y_h:
        return 1
    else:
        return 0
    
def y_distrinutions(y_train, y_val):
    """Check y distributions.
    
    Arguments:
    y_train (array): target values for train dataset.
    y_val (array): target values for validation dataset.
    
    Output:
    pd.DataFrame with y_train and y_val distribution.
    """
    train = pd.Series(bins_y(y_train)).value_counts()
    val = pd.Series(bins_y(y_val)).value_counts()
    return pd.DataFrame({"y_train": train, "y_val": val}).sort_index()

def mse_score(predt: np.ndarray, dtrain: xgb.DMatrix) -> Tuple[str, float]:
    """Mean Squared Error - MSE for XGBRegressor algorithm."""
    y = dtrain.get_label()
    predt[predt < -1] = -1 + 1e-6
    return 'mse', mean_squared_error(y, predt)