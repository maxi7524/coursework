from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

data_path = 'trained_models'
model_path = data_path + '/random_forest_100'

# ładowanie modelu 
model = joblib.load(model_path)
target_names = ["setosa", "versicolor", "virginica"]

# FastAPI odpowiada za OBSŁUGĘ STRONY - walidacje inputów, generowanie dokumentacji interaktywnej, /docs /redoc, i json'em jako formatem komunikacji się posługuję
app = FastAPI(title="My API")

# model danych wejściowych 
#TODO - sprawdzić czym jest BaseModel i w jaki sposób jest potrzebny do załadowania tych danych 
# to służy sprawdzania walidacji, pydantic, zawiera już gotowe biblioteki które to obsługują
class IrisFeatures(BaseModel):
    #TODO - co jak byśmy mieli bardzo dużo cech ??? 
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

# Stawianie aplikacji 
@app.post("/predict") # tutaj dajemy sobie zatem jest nasza stron http://adres/predict - i zacznie nam wykonywać predykcje 
def predykcja_gatunków(features: IrisFeatures):
    # TODO - na czym polega ta konstrukcja 
    data = np.array([[features.sepal_length,
                      features.sepal_width,
                      features.petal_length,
                      features.petal_width]])
    pred = model.predict(data)[0]
    # 
    
    species = target_names[pred]
    return {"Predykcja": species}