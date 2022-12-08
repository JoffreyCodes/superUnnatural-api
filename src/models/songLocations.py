from database import db
from sqlalchemy import ForeignKey

class SongLocation(db.Model):
    __tablename__ = 'SongLocations'
    __autoId__ = db.Column(db.Integer, primary_key=True, autoincrement=True)
    WorkoutId = db.Column(db.Integer, 
                        ForeignKey('Workouts.WorkoutId', 
                                    onupdate='CASCADE', 
                                    ondelete='CASCADE'), 
                        nullable=False)
    SongId = db.Column(db.Integer, 
                        ForeignKey('Songs.SongId', 
                                    onupdate='CASCADE', 
                                    ondelete='CASCADE'), 
                        nullable=False)
    LocationId = db.Column(db.Integer, 
                        ForeignKey('Locations.LocationId', 
                                    onupdate='CASCADE', 
                                    ondelete='CASCADE'), 
                        nullable=False)


class Song(db.Model):
    __tablename__ = 'Songs'
    SongId = db.Column(db.Integer, primary_key=True)
    SongTitle = db.Column(db.String(255), nullable=False)
    Artist = db.Column(db.String(255), nullable=False)
    Length = db.Column(db.String(255), nullable=False)

    
class Location(db.Model):
    __tablename__ = 'Locations'
    Location = db.Column(db.String(255), nullable=False)
    ScreenshotUrl = db.Column(db.String(255), nullable=False)
    LocationId = db.Column(db.Integer, primary_key=True)
    NearGround = db.Column(db.Boolean, default=False, nullable=False)