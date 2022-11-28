import os
from dotenv import load_dotenv, find_dotenv

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, func

db = SQLAlchemy()

load_dotenv(find_dotenv())
DATABASE_URI = os.getenv('DATABASE_URI')
engine = create_engine(DATABASE_URI, echo=True)

class Note(db.Model):
    __tablename__ = 'Notes'
    NoteId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    SpUserId = db.Column(db.Integer, primary_key=False)
    SnWorkoutId = db.Column(db.Integer, primary_key=False)
    SnTrackId = db.Column(db.Integer, nullable=False)
    Content = db.Column(db.String(255), nullable=False)
    Created = db.Column(db.TIMESTAMP(timezone=False), nullable=False, default=func.now())
