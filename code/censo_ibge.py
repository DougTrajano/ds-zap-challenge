import pandas as pd
import geopandas as gpd
import os

class CensoData:
    def __init__(self, censo_paths: dict, shapefile_path: str):
        self.censo_paths = censo_paths
        self.shapefile_path = shapefile_path
        self.shapefile = None
        
        self.load_shapefile(self.shapefile_path)

    def get_censo_features(self, censo_code, censo_config):
        features = {}

        for file in censo_config.keys():
            if file in self.censo_paths.keys():
                df = self.load_csv(self.censo_paths[file])
                data = df[df["Cod_setor"] == censo_code].to_dict(orient="records")
                
                if len(data) > 0:
                    data = data[0]
                    for var in censo_config[file].keys():
                        if var in data.keys():
                            features[censo_config[file][var]] = data[var]
        return features

    def get_censo_code(self, coordinate_point):
        df = pd.DataFrame({"coordinate_point": [coordinate_point]})
        df['census_code'] = df['coordinate_point'].map(lambda x: self.shapefile.loc[self.shapefile.contains(x), 'CD_GEOCODI'].values).str[0].astype('int64')
        return df["census_code"].values[0]

    def load_csv(self, path):
        df = pd.read_csv(path, encoding="iso8859_15", sep=";", low_memory=False)
        return df

    def load_shapefile(self, path):
        self.shapefile = gpd.read_file(path)