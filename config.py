import os
import click
from flask import Flask
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

class Config(object):

    FLASK_APP = 'wsgi.py'
    FLASK_ENV = os.environ.get('FLASK_ENV')

    SECRET_KEY = os.urandom(64)
    DEBUG = True
    HOST = "0.0.0.0"
    PORT = 8580

    # Flask-Assets
    LESS_BIN = os.environ.get('LESS_BIN')
    ASSETS_DEBUG = os.environ.get('ASSETS_DEBUG')
    LESS_RUN_IN_DEBUG = os.environ.get('LESS_RUN_IN_DEBUG')

    # Static Assets
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    COMPRESSOR_DEBUG = os.environ.get('COMPRESSOR_DEBUG')


    #SQLite3
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + BASE_DIR + "/radiobeaconv3.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    FLASK_ADMIN_SWATCH = "flatly"
    SQLALCHEMY_ECHO = False

class DevelopmentConfig(Config):
    pass

class ProductionConfig(Config):
    DEBUG = False
    pass

config = {
#lets you do config.development
    "development": DevelopmentConfig(),
    "production": ProductionConfig()

}