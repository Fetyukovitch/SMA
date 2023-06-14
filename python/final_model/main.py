from typing import Union
from fastapi import FastAPI
import pandas as pd
from predict import predictor

app = FastAPI()

@app.post('/predict')
def generate_sentimental_data(date): 
    data = predictor(date)
    return {
            'recomendation': data[0],
#            'probability': round(data[1], 2),
#            'price_day_before': round(data[2], 2)
            }

