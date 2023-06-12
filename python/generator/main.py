from typing import Union

from fastapi import FastAPI

app = FastAPI()

from sentimental import Sentimental
import pandas as pd

def get_sentimental_data(stock):
    
    sent_analysis = Sentimental()
    print('get data is running...')
    old_data = sent_analysis.initial_data()
    sm_data = sent_analysis.get_data_from_sm(stock)
    new_data = sm_data[~sm_data['content'].isin(old_data['content'])].copy()
    new_data['sentiment'] = 0
    new_data = sent_analysis.set_sentiment_data(new_data)
    result = pd.concat([old_data, new_data]).reset_index()[['symbol', 'content', 'created_at', 'score', 'sentiment']]
    if len(new_data) > 0:
        sent_analysis.update_data_bq(result)
    print(f'New semtimal data: {len(new_data)} elements')
    return result

def get_fundamental_data():
    pass

def get_historical_data():
    pass

@app.post('/sentimental')
def generate_sentimental_data(): 
    print(get_sentimental_data('AAPL'))
