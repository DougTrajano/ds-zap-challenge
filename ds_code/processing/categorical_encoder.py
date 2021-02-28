import json
import pandas as pd


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
            if self.codec[feature_name][key] == value:
                return key
    
    def add_value(self, feature_name: str, value: str):
        """Add a new value to codec."""
        last_value = max(self.codec[feature_name].values())
        i = last_value + 1
        self.codec[feature_name][value] = i
        
        with open(self.path, 'w') as outfile:
            json.dump(self.codec, outfile)
            
        return i