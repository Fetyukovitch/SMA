import re

def clean_data(text):
    cleanr = re.compile('<.*?>')
    text = re.sub('[0-9]+', '', re.sub(r'http\S+', '', re.sub(cleanr, '', text)))
    text = text.lower().replace('\n', ' ').strip()
    text = text[0:512]
    return text
