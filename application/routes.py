
"""Routes for core Flask app."""
import os
import sys
import json
import codecs
import pandas as pd
import sqlite3
from dateutil.relativedelta import relativedelta
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

def add_sqlite_date_filter(query, date, since_month=True, since_day=False):
    '''
    adds a date filter to a query against the sms database
    params:
     query: sqlite query
     date: expected format is %y-%B-%d 
    TODO function does not really work with string months need to
    add month in int format to get this to work
    '''
    date_parts = date.split('-')
    year = date_parts[0]
    month = date_parts[1]
    day = date_parts[2]

    if "WHERE" in query:
        date_filter = f"""
        AND year = {year}
        """
    else:
        date_filter = f"""
         WHERE year = {year}
        """
    
    if since_month:
        date_filter = date_filter + f' AND month_name = "{month}" '
    if since_day:
        date_filter = date_filter + f' AND day >= {day}'
    return query + date_filter



def fetch_data(author=None, source='sqlite', tail_int=10,
               date_filter=dt.now().strftime('%Y-%B-%d'), sort_by_date=True):
    '''
    default source is sqlite else old csv file
    '''

    if source == 'sqlite':
        conn = sqlite3.connect('./etl/sms.db')
        if author is not None:
            query = f'SELECT * FROM sms WHERE Sender = "{author}"'
        else:
            query = "SELECT * FROM sms"
        print(f"executing query: {query}")
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
        df['timestamp'] = pd.to_datetime(df['timestamp'])
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
    three_months_ago = dt.today() - relativedelta(months=3)
    data = fetch_data(tail_int=100, date_filter=three_months_ago.strftime('%Y-%B-%d'))
    return render_template('index.html', data=data, author="from Everyone")

@main_bp.route('/data-table', methods=['GET', 'POST'])
def data_table():
    """
    Home Route
    """
    data = fetch_data(tail_int=None, sort_by_date=True)
    return render_template('data_table.html', data=data)

@main_bp.route('/<sender>')
def page(sender):
    author = sender.replace('_', ' ') 
    data = fetch_data(author=author, tail_int=100)
    return render_template('index.html', data=data, author=sender)
