from app.config.config import db


class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(64), unique=True)
    lastname = db.Column(db.String(64), unique=True)
