import logging
import mlflow
import pandas as pd
from fastapi import FastAPI
from ds_code.processing.helper_functions import read_json
from .data_models import Apartment

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s :: %(levelname)s :: %(module)s :: %(funcName)s :: %(message)s')

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

params = read_json("properties/application.json")

# Load model as a PyFuncModel.
logger.info({"message": "Loading MLflow model."})
loaded_model = mlflow.pyfunc.load_model(params["fastapi"]["model_path"])

logger.info({"message": "Starting FastAPI."})
app = FastAPI(title=params["fastapi"]["title"],
              description=params["fastapi"]["description"],
              version=params["fastapi"]["version"])

@app.get('/health', summary="Health check endpoint.")
def health():
    logger.info({"message": "Get health check"})
    return {"status": "UP"}

@app.get('/predict', summary="Get sales price from machine learning model.")
def predict(apartment: Apartment):
    
    logger.info({"message": "Get /predict", "apartment": apartment.dict()})

    # Predict on a Pandas DataFrame.
    pred = loaded_model.predict(pd.DataFrame([apartment.dict()]))
    
    logger.info({"message": "Return /predict", "price": pred[0]})

    return {"price": pred}