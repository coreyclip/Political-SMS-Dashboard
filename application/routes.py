
"""Routes for core Flask app."""
import os
import sys
import json
import codecs
import pandas as pd
import sqlite3
from datetime import datetime as dt
from flask import Blueprint, render_template, flash, redirect, url_for, g, request, current_app
from flask_assets import Environment, Bundle
from flask import current_app as app

main_bp = Blueprint('main_bp', __name__,
                    template_folder='templates',
                    static_folder='static')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

def fetch_data(author=None, source='sqlite', tail_int=10, sort_by_date=True):
    '''
    default source is sqlite else old csv file
    '''

    if source == 'sqlite':
        conn = sqlite3.connect('./etl/sms.db')
        if author is not None:
            query = f"SELECT * FROM sms WHERE Sender = {author}"
        else:
            query = "SELECT * FROM sms"
        df = pd.read_sql(query, conn)

    else:
        df = pd.read_csv('./application/data/ProcessedTexts.csv', index_col='ROWID',
                        usecols=['ROWID','SenderPhoneNumber', 'Sender', 'text', 'month_name',
                                 'day','year', 'polarity','subjectivity', 'negativity', 'neutrality',
                                 'positivity', 'compound', 'date', 'word_count', 'timestamp'
                                 ]
                        )
        if author != None:
            df = df[df['author'] == author]

    if sort_by_date is True:
        df = df.sort_values('timestamp', ascending=True)

    if tail_int == None:
        return df.to_dict(orient='records')
    else:
        return df.tail(tail_int).to_dict(orient='records')

@main_bp.route('/', methods=['GET', 'POST'])
@main_bp.route('/index', methods=['GET', 'POST'])
def home():
    """
    Home Route
    """
    data = fetch_data(tail_int=100)
    return render_template('index.html', data=data, author="Everyone")

@main_bp.route('/data-table', methods=['GET', 'POST'])
def data_table():
    """
    Home Route
    """
    data = fetch_data(tail_int=None, sort_by_date=True)
    return render_template('data_table.html', data=data)

@main_bp.route('/{sender}')
def page(author, page):
    author = sender.replace('_', ' ') 
    data = fetch_data(author=author, tail_int=100)
    return render_template('index.html', data=data, author=sender)
