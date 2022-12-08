from database import db

class Coach(db.Model):
    __tablename__ = 'Coaches'
    CoachId = db.Column(db.Integer, primary_key=True)
    Coach = db.Column(db.String(255), nullable=False)
