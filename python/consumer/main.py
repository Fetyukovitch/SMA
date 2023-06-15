from cemail import Email
from fastapi import FastAPI
from data import Data
import requests
from predict import predictor
from datetime import date 

app = FastAPI()

def donwload_model():
    pass

def model_predict():
    pass

@app.post('/email')
def send_email():
    today = date.today().strftime('%Y-%m-%d')
    data = Data()
    result = data.get_emails()
    data_predicted = predictor(today)
    prediction = data_predicted[0]

    for email_address in result:
        print(email_address)
        mail = Email()
        mail.send(email_address, 'APPL recomendation', prediction)
    return {'status': 'ok'}

@app.post('/emails')
def add_email(new_email):
    data.insert_email(new_email)
    return {'status': 'ok'}
