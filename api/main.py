from fastapi import FastAPI, HTTPException, Query
import pandas as pd
import pickle
import logging
from api.schemas import HouseFeatures, PredictResponse
from api.db import query_filtered

logging.basicConfig(level=logging.INFO)
app = FastAPI(title="House Price Prediction API")

try:
    with open("api/best_model.pkl", "rb") as f:
        model = pickle.load(f)
except FileNotFoundError:
    model = None
    logging.error("Model not found — run api/model.py first")

@app.get("/health")
def health():
    return {"status": "ok" if model else "degraded"}

@app.post("/predict", response_model=PredictResponse)
def predict(house: HouseFeatures):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    df = pd.DataFrame([house.model_dump()])
    try:
        price = model.predict(df)[0]
    except Exception as e:
        logging.exception("Prediction failed")
        raise HTTPException(status_code=500, detail=str(e))
    return {"predicted_price": round(float(price), 2)}

@app.get("/listings")
def listings(min_price: float = Query(default=None), max_bedrooms: int = Query(default=None)):
    df = query_filtered(min_price, max_bedrooms)
    return df.to_dict(orient="records")
