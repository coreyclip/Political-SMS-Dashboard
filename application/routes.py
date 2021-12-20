
"""Routes for core Flask app."""
import os
import sys
import json
import codecs
import pandas as pd
from datetime import datetime as dt
from flask import Blueprint, render_template, flash, redirect, url_for, g, request, current_app
from flask_assets import Environment, Bundle
from flask import current_app as app

main_bp = Blueprint('main_bp', __name__,
                    template_folder='templates',
                    static_folder='static')

sys.path.append('./application/data')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500


@main_bp.route('/', methods=['GET', 'POST'])
@main_bp.route('/index', methods=['GET', 'POST'])
def home():
    """
    Home Route
    """
    df = pd.read_csv('ProcessedTexts.csv', index_col='ROWID',
                     usecols=['ROWID','SenderPhone', 'Sender', 'text', 'month_name', 'day', 'year', 'polarity',
                              'subjectivity', 'negativity', 'neutrality', 'positivity', 'compound'])
    sdf = df[df['Sender'] == 'Trump'].tail(10)
    data = sdf.to_dict(orient='records')
    return render_template('index.html', data=data)

@main_bp.route('/sms/{author}/{page}')
def page(author, page):
    payload = f'{author}/{page}'
    return render_template('sms.html', payload=payload)
