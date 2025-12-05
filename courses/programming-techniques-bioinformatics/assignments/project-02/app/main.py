import joblib
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Load models
lr = joblib.load("models/lr_model.pkl")
poly = joblib.load("models/poly_model.pkl")
pt = joblib.load("models/pt_transform.pkl")
scaler = joblib.load("models/scaler.pkl")
pls = joblib.load("models/pls.pkl")

# Structure of the data in request
class WeatherFeatures(BaseModel):
    temperature_2m: float
    relativehumidity_2m: float
    dewpoint_2m: float
    apparent_temperature: float
    cloudcover: float
    cloudcover_low: float
    cloudcover_mid: float
    cloudcover_high: float
    windspeed_10m: float
    windgusts_10m: float
    shortwave_radiation: float
    direct_radiation: float
    diffuse_radiation: float
    vapor_pressure_deficit: float
    precipitation: float
    weathercode: float
    snowfall: float


@app.get("/")
def home():
    return {"status": "server running"}

@app.post("/predict-energy")
def predict_energy(features: WeatherFeatures):

    X_raw = [[
        features.temperature_2m,
        features.relativehumidity_2m,
        features.dewpoint_2m,
        features.apparent_temperature,
        features.cloudcover,
        features.cloudcover_low,
        features.cloudcover_mid,
        features.cloudcover_high,
        features.windspeed_10m,
        features.windgusts_10m,
        features.shortwave_radiation,
        features.direct_radiation,
        features.diffuse_radiation,
        features.vapor_pressure_deficit,
        features.precipitation,
        features.weathercode,
        features.snowfall
    ]]

    # Preprocess the data
    X_scaled = scaler.transform(X_raw)
    X_reduced = pls.transform(X_scaled)

    # Predictions
    pred_lr = pt.inverse_transform(lr.predict(X_reduced).reshape(-1, 1))[0][0]
    pred_poly = pt.inverse_transform(poly.predict(X_reduced).reshape(-1, 1))[0][0]

    return {
        "lr_model_prediction": pred_lr,
        "poly_model_prediction": pred_poly
    }
