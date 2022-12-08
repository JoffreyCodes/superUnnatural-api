from database import db

class Location(db.Model):
    __tablename__ = 'Locations'
    Location = db.Column(db.String(255), nullable=False)
    ScreenshotUrl = db.Column(db.String(255), nullable=False)
    LocationId = db.Column(db.Integer, primary_key=True)
    NearGround = db.Column(db.Boolean, default=False, nullable=False)
