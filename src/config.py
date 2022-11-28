import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DB = os.getenv('MYSQL_DB')
MYSQL_CURSORCLASS = 'DictCursor'

basedir = os.path.abspath(os.path.dirname(__file__))

# Connect to the MYSQL database
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')

# Turn off the Flask-SQLAlchemy event system and warning
SQLALCHEMY_TRACK_MODIFICATIONS = False