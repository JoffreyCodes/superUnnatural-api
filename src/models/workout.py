from database import db
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.mysql import (MEDIUMTEXT)



class Workout(db.Model):
    __tablename__ = 'Workouts'
    WorkoutId = db.Column(db.Integer, primary_key=True, nullable=False)
    Name = db.Column(db.String(255), nullable=False)
    Description = db.Column(MEDIUMTEXT(charset='utf8mb4'), nullable=False)
    Length = db.Column(db.String(255), nullable=False)
    Date = db.Column(db.TIMESTAMP(timezone=False), nullable=False)
    WorkoutType = db.Column(db.String(255), nullable=False)
    SpotifyUrl = db.Column(db.String(255), nullable=False)
    CoachId = db.Column(db.Integer, nullable=False)
    IntensityId = db.Column(db.Integer, nullable=False)


    __mapper_args__ = {
        'polymorphic_identity': 'Workouts',
        'polymorphic_on': WorkoutType,
    }

class Stretch(Workout):
    __tablename__ = 'stretch'
    WorkoutId = db.Column(db.Integer, 
                        ForeignKey("Workouts.WorkoutId", 
                            onupdate='CASCADE', 
                            ondelete='CASCADE'), 
                        primary_key=True)
    
    __mapper_args__ = {
        'polymorphic_identity': 'stretch',
    }


class Meditation(Workout):
    __tablename__ = 'meditation'
    WorkoutId = db.Column(db.Integer, 
                        ForeignKey("Workouts.WorkoutId", 
                            onupdate='CASCADE', 
                            ondelete='CASCADE'), 
                        primary_key=True)
    
    __mapper_args__ = {
        'polymorphic_identity': 'meditation',
    }

class Boxing(Workout):
    __tablename__ = 'boxing'
    WorkoutId = db.Column(db.Integer, 
                    ForeignKey("Workouts.WorkoutId", 
                        onupdate='CASCADE', 
                        ondelete='CASCADE'), 
                    primary_key=True)
    MaxTargets = db.Column(db.Integer, nullable=False)
    MaxDodges = db.Column(db.Integer, nullable=False)
    MaxKneeStrikes = db.Column(db.Integer, nullable=False)
    MaxScore = db.Column(db.Integer, nullable=False)
    PointsPerMin = db.Column(db.Integer, nullable=False)
    TargetsPerMin = db.Column(db.Integer, nullable=False)
    
    __mapper_args__ = {
        'polymorphic_identity': 'boxing',
    }

class Classic(Workout):
    __tablename__ = 'classic'
    WorkoutId = db.Column(db.Integer, 
                        ForeignKey("Workouts.WorkoutId", 
                            onupdate='CASCADE', 
                            ondelete='CASCADE'), 
                        primary_key=True)
    MaxTargets = db.Column(db.Integer, nullable=False)
    Triangles = db.Column(db.Integer, nullable=False)
    MaxKneeStrikes = db.Column(db.Integer, nullable=False)
    MaxScore = db.Column(db.Integer, nullable=False)
    PointsPerMin = db.Column(db.Integer, nullable=False)
    TargetsPerMin = db.Column(db.Integer, nullable=False)
    
    __mapper_args__ = {
        'polymorphic_identity': 'classic',
    }