from database import db

class Song(db.Model):
    __tablename__ = 'Songs'
    SongId = db.Column(db.Integer, primary_key=True)
    SongTitle = db.Column(db.String(255), nullable=False)
    Artist = db.Column(db.String(255), nullable=False)
    Length = db.Column(db.String(255), nullable=False)
