import os
from dotenv import load_dotenv, find_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_migrate import Migrate

load_dotenv(find_dotenv())

DATABASE_URI = os.getenv('DATABASE_URI')
engine = create_engine(DATABASE_URI, echo=True)
db = SQLAlchemy()

def initialize(app):
    db.init_app(app)
    
def migrate(app):
    return Migrate(app, db)
