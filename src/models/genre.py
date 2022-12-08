from database import db
from sqlalchemy import ForeignKey


class Genre(db.Model):
    __tablename__ = 'Genres'
    GenreId = db.Column(db.Integer, primary_key=True)
    Genre = db.Column(db.String(255), nullable=False)

class GenreList(db.Model):
    __tablename__ = 'GenreList'
    __autoId__ = db.Column(db.Integer, primary_key=True, autoincrement=True)
    WorkoutId = db.Column(db.Integer, 
                        ForeignKey('Workouts.WorkoutId', 
                            onupdate='CASCADE', 
                            ondelete='CASCADE'), 
                        nullable=False)
    GenreId = db.Column(db.Integer, 
                        ForeignKey('Genres.GenreId', 
                            onupdate='CASCADE', 
                            ondelete='CASCADE'), 
                        nullable=True)