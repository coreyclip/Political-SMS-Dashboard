from textblob import TextBlob
import nltk
import datetime as dt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import os 
import json 

with open('etl/SenderMap.json') as sender_map_file:
    sender_map = json.load(sender_map_file)


class sms_features:
    def __init__(self, text, timestamp, sender):
        self.text = str(text).replace('corey', "<recipient name>")
        if isinstance(timestamp, str):
            self.received = dt.datetime.strptime(timestamp, "%a, %d %b %Y %H:%M:%S %z")
        else:
            self.received = timestamp
        self.sender_phone = sender
        self.sender_map = sender_map
        self.sender_name = self.sender_map[self.sender_phone]
        self.parse_dates()
        self.remove_gvoice_footer()
        self.parse_sentiment()
    def remove_gvoice_footer(self):
        footer_lines = ['Stop2End'
                        ,'To respond to this text message, reply to this email or visit Google Voice.']
        for line in footer_lines:
            self.text = self.text.replace(line, '')    
    def parse_dates(self):
        ts = self.received
        self.month_name = ts.strftime("%B") #September
        self.day_name = ts.strftime("%A")#Tuesday
        self.day = ts.strftime('%d') #15
        self.hour = ts.strftime('%H') #13
        self.weekday = ts.strftime('%w')#4
        self.week = ts.strftime('%W') #38
        self.year = ts.strftime('%Y') #2020
    def parse_sentiment(self):
        blob = TextBlob(self.text)
        analyzer = SentimentIntensityAnalyzer()
        polarity_scores = analyzer.polarity_scores(self.text)
        self.polarity = blob.sentiment.polarity
        self.subjectivity = blob.sentiment.subjectivity
        self.nouns = blob.noun_phrases
        self.tags = blob.tags
        self.word_count = len(blob.split())
        self.negativity = polarity_scores['neg']
        self.neutrality = polarity_scores['neu']
        self.positivity = polarity_scores['pos']
        self.compound = polarity_scores['compound']





