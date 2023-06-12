import praw
from datetime import datetime, timedelta
from pathlib import Path
import os
import pandas as pd
import openai
from utils import clean_data
from data import get_data_with_cache, load_data_to_bq

class Sentimental:
    columns = ['symbol', 'content', 'created_at', 'score']

    def __init__(self):
        self.gcp_project = os.environ['GCP_PROJECT']
        self.dataset = 'sma'
        self.table = 'sma'
        client_id = os.environ['RD_CLIENT_ID']
        client_secret = os.environ['RD_CLIENT_SECRET']
        user_agent = os.environ['RD_USER_AGENT']
        username = os.environ['RD_USERNAME']
        password = os.environ['RD_PASSWORD']

        self.reddit = praw.Reddit(
            client_id=client_id, 
            client_secret=client_secret, 
            user_agent=user_agent, 
            username=username,
            password=password
        )

        openai.api_key = os.environ['API_KEY']

    def get_subreddit_by_name(self, reddit_name, subreddit_name):
        messages = pd.DataFrame(columns=self.columns)
        subreddit = self.reddit.subreddit(reddit_name)
        for message in subreddit.search(subreddit_name, limit=1500 ):
            messages.loc[len(messages)] = [
                subreddit_name,
                clean_data(f'{message.title} {message.selftext}'), 
                datetime.fromtimestamp(message.created_utc).strftime("%Y-%m-%d"), 
                message.score
            ]
        return messages

    def get_data_from_sm(self, symbol):
        result = pd.DataFrame()
        i = 0
        for subreddit in ['stockmarket', 'all', 'wallstreetbets', symbol]:
            print(f'{subreddit} {i}')
            partial = self.get_subreddit_by_name(subreddit, symbol)
            result = pd.concat([result, partial])
            i += 1 
        result = result.drop_duplicates('content').sort_values('score', ascending=False).reset_index()
        result = result[result.score > 100][['symbol', 'content', 'created_at', 'score']]
        return result

    def get_sentiment(self, text):
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Perform sentiment analysis on the following text:\n{text}\n respond with a single value between -1 and 1. I.e. if the sentiment is extremely positive, respond with a value such as 0.99. If somewhat negative respond with a value such as -0.63. Only respond with a single value.",
            temperature=0,
            max_tokens=7
        )
        sentiment = response.choices[0].text.strip()
        return sentiment

    def set_sentiment_data(self, dataset):
        dataset['sentiment'] = dataset['content'].apply(lambda x: self.get_sentiment(x))
        return dataset

    def initial_data(self):
        query = f"""
            SELECT {','.join(self.columns)} 
            FROM {self.gcp_project}.{self.dataset}.{self.table}
            WHERE symbol = 'APPL'
        """
        return get_data_with_cache(self.gcp_project, query=query, cache_path=Path('raw_data/reddit_sentimental_AAPL.csv'))

    def update_data_bq(self, data):
        load_data_to_bq(
                data,
                self.gcp_project,
                self.dataset,
                self.table,
                True
                )
