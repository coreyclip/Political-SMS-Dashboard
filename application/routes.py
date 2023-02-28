
"""Routes for core Flask app."""
import os
import sys
import json
import codecs
from dateutil.relativedelta import relativedelta
from datetime import datetime as dt
from flask import Blueprint, render_template, flash, redirect, url_for, g, request, current_app
from flask_assets import Environment, Bundle
from flask import current_app as app
from application.forms import SearchForm
from application.controller import add_sqlite_date_filter, fetch_data

main_bp = Blueprint('main_bp', __name__,
                    template_folder='templates',
                    static_folder='static')

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
    form = SearchForm()
    if form.validate_on_submit():
        author = form.author.data
        search_text = form.search.data
        print(f"form submited for {author}")
        if search_text:
            print(f"search performed for {search_text}")
        author = author.replace('_', ' ')
        # if author == 'Everyone':
        #     return redirect('/')
        # else:
        #     return redirect(f'/{author}')
    else:
        author = 'Everyone'
        search_text = None
    three_months_ago = dt.today() - relativedelta(months=3)
    data = fetch_data(top=50, author=author,  date_filter=three_months_ago.strftime('%Y-%B-%d'), search_text=search_text)
    return render_template('index.html', data=data, author=author, form=form)

@main_bp.route('/data-table', methods=['GET', 'POST'])
def data_table():
    """
    Home Route
    """
    data = fetch_data(top=None, sort_by_date=True)
    return render_template('data_table.html', data=data)

@main_bp.route('/<sender>', methods=['GET', 'POST'])
def page(sender):
    form = SearchForm()
    if form.validate_on_submit():
        author = form.author.data
        print(f"form submited for {author}")
        if author == 'Everyone':
            return redirect('/')
        else:
            return redirect(f'/{author}')
    else:
        print(form.validate_on_submit())
    author = sender.replace('_', ' ') 
    data = fetch_data(author=author, top=100)
    return render_template('index.html', data=data, author=author, form=form)

@main_bp.route('/about')
def about():
    return render_template('about.html')
