import os


SECRET_KEY = os.urandom(64)
DEBUG = True
HOST = "0.0.0.0"
PORT = 8580


# SQLite3
SQLALCHEMY_DATABASE_URI = "sqlite:///radiobeaconv3.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False