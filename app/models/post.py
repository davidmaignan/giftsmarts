from app.config.config import db
from app.config.config import app
from app.constants import *
from sqlalchemy.orm import relationship


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.String, primary_key=True)
    story = db.Column(db.String, nullable=False)
    created = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.String, db.ForeignKey('user.id'))

