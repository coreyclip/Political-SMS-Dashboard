'''initialize app'''
import os
import logging
from logging.handlers import SMTPHandler
from logging.handlers import RotatingFileHandler
from config import Config
from flask import Flask
from flask_dotenv import DotEnv
from dotenv import load_dotenv
load_dotenv('.env')


app = Flask(__name__,
            instance_relative_config=False)
env = DotEnv(app)
app.config.from_object(Config)


if not os.path.exists('logs'):
    os.mkdir('logs')
file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240,
                                   backupCount=10)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)

app.logger.setLevel(logging.INFO)
app.logger.info('Political SMS Campaign Startup')

with app.app_context():
    # Import main Blueprint
    from application import routes
    app.register_blueprint(routes.main_bp)
