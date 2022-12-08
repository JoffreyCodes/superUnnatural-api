from database import db


class Intensity(db.Model):
    __tablename__ = 'Intensities'
    IntensityId = db.Column(db.Integer, primary_key=True)
    Intensity = db.Column(db.String(255), nullable=False)
