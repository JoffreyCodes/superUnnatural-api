import os
from dotenv import load_dotenv, find_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_migrate import Migrate
from sqlalchemy.ext.declarative import declarative_base

load_dotenv(find_dotenv())

DATABASE_URI = os.getenv('DATABASE_URI')
engine = create_engine(DATABASE_URI, echo=True)
base = declarative_base()
db = SQLAlchemy(engine_options={'url': os.getenv('DATABASE_URI')})

def initialize(app):
    db.init_app(app)
    
def migrate(app):
    return Migrate(app, db)
