import json
import urllib.request
import geohash2
import string
import unidecode
import os
from shapely.geometry import Point
from zipfile import ZipFile
from tqdm import tqdm

# Custom scripts
from censo_ibge import CensoData
from data_models import *


def processing(raw, converted_features=None, ibge_paths=None, shapefile_path=None, censo_config=None):
    """
    This function apply all processing steps in dataset.
    
    Arguments:
    - raw (list): dataset as list with dict elements.
    - converted_features (dict, optional): Dictionary with features in raw list to be converted
    - ibge_paths (dict, optional): Dictionary with IBGE file paths.
    - shapefile_path (str, optional): Location of shapefile
    - censo_config (dict, optional): Dictionary with files and variables maps for IBGE Censo Data.

    Output:
    - List with dict using Imovel (data_models.py)
    """
    
    processed = []

    # inst ibge class
    if isinstance(ibge_paths, dict) and isinstance(censo_config, dict) and isinstance(shapefile_path, str):
        censo = CensoData(ibge_paths, shapefile_path)

    with tqdm(total=len(raw)) as pbar:
        pbar.set_description("Processing")
        for item in raw:
            # Add geohashes and point
            if item.get("address_geoLocation_location_lat") != None and item.get("address_geoLocation_location_lon") != None:
                item["geohash"] = get_geohash(lat=item.get("address_geoLocation_location_lat"),
                                            lon=item.get("address_geoLocation_location_lon"),
                                            delimiter=7)
                
                item["geopoint"] = Point(item.get("address_geoLocation_location_lon"),
                                        item.get("address_geoLocation_location_lat"))
                
            # Add images_qty
            item["image_qty"] = get_images_qty(item)
            
            # Features from description
            if isinstance(item.get("description"), str):
                features_desc = t = DescriptionFeatures(item["description"]).get_features()
                item = {**item, **features_desc}
                
            # Add IBGE Censo 2010
            if isinstance(ibge_paths, dict) and isinstance(censo_config, dict) and isinstance(shapefile_path, str):
                item["census_code"] = censo.get_censo_code(item["geopoint"])
                censo_features = censo.get_censo_features(item["census_code"], censo_config)
                item = {**item, **censo_features}
            
            # Converting features names
            if isinstance(converted_features, dict):
                for key in converted_features.keys():
                    if item.get(key) != None:
                        item[converted_features[key]] = item[key]
                    
            new_item = Imovel(**item)
            
            processed.append(new_item.dict())
            pbar.update(1)
        
    return processed

def extract_zip(file_path, to_path=None):
    """
    Extract zip files.

    Arguments:
    - file_path (str): The file path of zip file.
    - to_path (str): The path to extracted files.

    Output:
    - This function has no return.
    """
    with ZipFile(file_path) as zip:
        if isinstance(to_path, str):
            # define best path to save it.
            zip.extractall(to_path)
        else:
            # save on application folder
            zip.extractall()


def download_url(url, file_name, to_path=None):
    """
    Function to download file.

    Arguments:
    - url (str): Direct url to download file.
    - file_name (str): The file name to downloaded file.
    - to_path (str, default is None): The path to save downloaded file.

    Output:
    - This function has no return.
    """
    if isinstance(to_path, str):
        path = to_path + file_name
    else:
        path = file_name

    with urllib.request.urlopen(url) as req_file:
        with open(path, 'wb') as out_file:
            out_file.write(req_file.read())

def get_files_path(path, file_extension=".csv", verbose=False):
    """
    A function that can provide the path for all csv files inside a folder.

    Input:
    path (str, required): A path to check files.
    file_extension (str, optional): A extension file to check for.

    Output:
    - A dict with file_name and pathes.
    """
    implemented_file_extension = [".csv", ".xls"]
    if file_extension not in implemented_file_extension:
        raise ValueError("This file extension isn't implemented")

    files = os.listdir(path)

    result = {}
    for file in files:
        if file_extension in file:
            file_path = path + "/" + file
            if file_extension == ".csv":
                result[file] = file_path
            elif file_extension == ".xls":
                result[file] = file_path

    return result

def load_json(file_path):
    """
    Load JSON file as dict.

    Arguments:
    - file_path (str): Path to find JSON file.

    Output:
    - List of dict structures for each line of JSON file.
    """
    with open(file_path, encoding="utf-8") as file:
        file = file.readlines()
        raw = [json.loads(each) for each in file]

    return raw


def flatten_dict(dd, separator='_', prefix=''):
    """
    Convert nested dict to flattened dict.
    https://www.geeksforgeeks.org/python-convert-nested-dictionary-into-flattened-dictionary/

    Arguments:
    - dd (dict):
    - separator (str, default is "_"):
    - prefix (str, default is ")

    Output:
    - Flattened dictionary
    """
    return {prefix + separator + k if prefix else k: v
            for kk, vv in dd.items()
            for k, v in flatten_dict(vv, separator, kk).items()
            } if isinstance(dd, dict) else {prefix: dd}

       
def get_geohash(lat, lon, delimiter=7):
    """
    Geohash it's a way to agreggate geolocation codes (lat, lon)
    
    Arguments:
    - lat (float, required):
    - lon (float, required):
    
    Output:
    - Geohash code    
    """
    geohash = geohash2.encode(lat, lon)
    return geohash[:delimiter]

def get_images_qty(item):
    """
    This function provide an int value for quantity images available.

    Arguments:
    - item (dict): Item variables for each row on dataset.

    Output:
    - Integer value representing the quantity of images available on each item.
    """
    if isinstance(item.get("images"), list):
        return len(item.get("images"))
    else:
        return 0

class DescriptionFeatures:
    def __init__(self, description):
        self.description = self.normalize(description)
        self.features = {}
        
    def normalize(self, text):
        # lower
        text = text.lower()
        
        # remove punctuation
        exclude = set(string.punctuation)
        text = ''.join([ch if ch not in exclude else ' ' for ch in text])
        
        # remove accents
        text = unidecode.unidecode(text)
        
        # remove newlines
        text = text.replace("\n", " ")
        
        text = [ch.strip() for ch in text.split()]
        
        return ' '.join(text)
    
    def get_features(self):
        # gym
        words = ["academia", "fitness", "gym", "bicicletario", "bike"]
        self.features["has_gym"] = self._gen_feat_by_words(words)
        
        # garden
        words = ["jardim", "jardinado"]
        self.features["has_garden"] = self._gen_feat_by_words(words)
        
        # pool
        words = ["piscina"]
        self.features["has_pool"] = self._gen_feat_by_words(words)

        # sauna
        words = ["sauna"]
        self.features["has_sauna"] = self._gen_feat_by_words(words)

        # lobby
        words = ["lobby", "lounge"]
        self.features["has_lobby"] = self._gen_feat_by_words(words)
        
        # party room
        words = ["salao de festa", "espaco de festa", "clube"]
        self.features["has_partyRoom"] = self._gen_feat_by_words(words)
        
        # balcony
        words = ["varanda", "sacada"]
        self.features["has_balcony"] = self._gen_feat_by_words(words)
        
        # playground
        words = ["infantil", "playground", "brinquedoteca", "recreacao"]
        self.features["has_playground"] = self._gen_feat_by_words(words)
        
        # grill
        words = ["churrasqueira", "grill"]
        self.features["has_grill"] = self._gen_feat_by_words(words)
        
        # games
        words = ["jogos", "quadra", "futebol", "esporte", "poliesportiva"]
        self.features["has_games"] = self._gen_feat_by_words(words)
        
        # closet
        words = ["closet"]
        self.features["has_closet"] = self._gen_feat_by_words(words)
        
        # elevator
        words = ["elevator"]
        self.features["has_elevator"] = self._gen_feat_by_words(words)

        # furnitures
        words = ["planejado", "decorado"]
        self.features["has_furnitures"] = self._gen_feat_by_words(words)

        # toilet
        words = ["lavabo"]
        self.features["has_toilet"] = self._gen_feat_by_words(words)
        
        return self.features
    
    def _gen_feat_by_words(self, words):
        have_words = False
        for word in words:
            if word in self.description:
                have_words = True
        return have_words