import sqlite3
import datetime as dt
import re
from dotenv import load_dotenv
from textblob import TextBlob
import nltk
import pandas as pd
from dateutil import parser
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import os 

load_dotenv('../env')
receiver_name = os.environ.get('RECIPIENT_NAME')

analyzer = SentimentIntensityAnalyzer()

pdf = pd.read_csv('PoliticalTexts.csv', index_col='ROWID')
df['text'] = [x.replace(reciever_name, '<recipient name>', 5) for x in df['text']]

# parse times
df['timestamp'] = pd.to_datetime(df['date'], infer_datetime_format=True) + pd.offsets.DateOffset(years=31)
df['text'] = df['text'].replace('\\n', ' ')
df['month_name'] = df['timestamp'].dt.month_name()
df['day_name'] = df['timestamp'].dt.day_name()
df['day'] = df['timestamp'].dt.day
df['hour'] = df['timestamp'].dt.hour
df['weekday'] = df['timestamp'].dt.weekday
df['week'] = df['timestamp'].dt.isocalendar().week
df['year'] = df['timestamp'].dt.isocalendar().year

# hardcoded drop of certain records
df = df.drop(index=[134844,134845,135206,135207,135264,135265,138476,
                   138477,138478,138479,138480,138482,138483,142979,
                   142980,144198,144199,144200])

# Calculate NLP values
df['polarity'] = [TextBlob(sms).sentiment.polarity for sms in df['text']]
df['subjectivity'] = [TextBlob(sms).sentiment.subjectivity for sms in df['text']]
df['negativity'] = [analyzer.polarity_scores(sms)['neg'] for sms in df['text']]
df['neutrality'] = [analyzer.polarity_scores(sms)['neu'] for sms in df['text']]
df['positivity'] = [analyzer.polarity_scores(sms)['pos'] for sms in df['text']]
df['compound'] = [analyzer.polarity_scores(sms)['compound'] for sms in df['text']]
df['nouns'] = [TextBlob(sms).noun_phrases for sms in df['text']]
df['tags'] = [TextBlob(sms).tags for sms in df['text']]
df['word_count'] = [len(TextBlob(sms).split()) for sms in df['text']]


# find nouns / purge name
def get_nouns():
    nouns = []

    for text in df['nouns']:
        for noun in text:
            if noun == RECIPIENT_NAME:
                nouns.append('<recipient name>')
            elif noun == 'stop2end':
                pass 
            else:
                nouns.append(noun)

def impact_detector(text):
    impact_parser = re.compile('(\d\d\d.(?<=%)|\d\d\d\d.(?<=%))|(\dX(?<=X))', re.IGNORECASE)


df.to_csv('data/ProcessedTexts.csv')
