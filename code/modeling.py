import json
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import KNNImputer
from sklearn.model_selection import train_test_split

class CategoricalEncoder:
    def __init__(self, path: str = "categorical_features.json"):
        self.codec = None
        self.path = path
        
    def load(self):
        """Carrega um JSON."""
        with open(self.path) as json_file:
            self.codec = json.load(json_file)
            
    def generate(self, df: pd.DataFrame, cat_features: list):
        """Cria um JSON"""
        cat_encoding = {}
        for col in cat_features:
            cat_encoding[col] = self.encode(df[col])
        
        self.codec = cat_encoding
        
        with open(self.path, 'w') as outfile:
            json.dump(cat_encoding, outfile)
        
    def encode(self, series: pd.Series, n_start: int = 1):
        """Faz o encoding para uma pd.Series."""
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
        """Transforma um valor categórico em numérico."""
        if not isinstance(self.codec, dict):
            raise ValueError("CategoricalEncoder not loaded.")
        
        if not value in self.codec[feature_name].keys():
            value = self.add_value(feature_name, value)
        else:
            value = self.codec[feature_name][value]
            
        return value
    
    def transform(self, df: pd.DataFrame, cat_features: list):
        """CatEncoder para todo um pd.DataFrame."""
        for col in cat_features:
            if col in df.columns:
                u_values = df[col].unique()
                for value in u_values:
                    cat_value = self._transform(col, value)
                    df[col].replace(value, cat_value, inplace=True)
                    
        return df
    
    def decode(self, feature_name: str, value: str):
        """Transforma um valor numérico em categórico."""
        for key in self.codec[feature_name].keys():
            if cat.codec[feature_name][key] == value:
                return key
    
    def add_value(self, feature_name: str, value: str):
        """Adiciona um valor desconhecido no codec"""
        last_value = max(self.codec[feature_name].values())
        i = last_value + 1
        self.codec[feature_name][value] = i
        
        with open(self.path, 'w') as outfile:
            json.dump(self.codec, outfile)
            
        return i

def split_dataset(X, n_range=20000):
    datasets = [X[x:x+n_range] for x in range(0, len(X), n_range)]
    
    return datasets

def prep_modeling(X, invalid_cols=None, large_dataset=True, seed=1993):
    """Prepare dataset to modeling.
    
    Arguments:
    X (pd.DataFrame, required): Dataset
    invalid_cols (list, optional): Invalid columns to be removed.
    large_dataset (bool, default=True): If working with a large dataset, we need to split the dataset to KNNImputer.
    seed (int, default=1993): Random seed
    
    """

    # Remove invalid columns
    if isinstance(invalid_cols, list):
        X.drop(columns=invalid_cols, inplace=True, errors="ignore")

    # Categorical encoding
    cat_features = X.select_dtypes(include=['object']).columns.tolist()

    encoder = CategoricalEncoder()
    encoder.generate(X, cat_features)
    X = encoder.transform(X, cat_features)

    # Missing values
    imputer = KNNImputer(n_neighbors=5)
    
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

def remove_outliers(X, y, lower=5000, higher=5000000):
    """
    Remove outliers based on y lower and higher.
    
    Arguments
    - X (pd.DataFrame): X values
    - y (numpy.array): y values
    - lower (int): Remove lower than this value.
    - higher (int): Remove higher than this value.
    
    Output
    X, y
    """
    y = pd.DataFrame(y)
    idx = y[~(y[0] <= lower) & ~(y[0] >= higher)].index.tolist()
    
    X = X.iloc[idx].reset_index(drop=True)
    y = y.iloc[idx].reset_index(drop=True)
    return X, y.values

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