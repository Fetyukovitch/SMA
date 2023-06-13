from cemail import Email
from fastapi import FastAPI
from data import Data

data = Data()
app = FastAPI()

def donwload_model():
    pass

def model_predict():
    pass

@app.post('/email')
def send_email():
    result = data.get_emails()

    for email_address in result:
        print(email_address)
        mail = Email()
        mail.send(email_address, 'APPL recomendation', 'buy it!')
    return {'status': 'ok'}

@app.post('/emails')
def add_email(new_email):
    data.insert_email(new_email)
    return {'status': 'ok'}
