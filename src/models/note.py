from sqlalchemy import func
from database import db

class Note(db.Model):
    __tablename__ = 'Notes'
    NoteId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    SpUserId = db.Column(db.Integer, primary_key=False)
    SnWorkoutId = db.Column(db.Integer, primary_key=False)
    SnTrackId = db.Column(db.Integer, nullable=False)
    Content = db.Column(db.String(255), nullable=False)
    Created = db.Column(db.TIMESTAMP(timezone=False), nullable=False, default=func.now())
