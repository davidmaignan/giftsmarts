from app.config.config import db
from app.config.config import app
from app.constants import *
from sqlalchemy.orm import relationship


class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.String, db.ForeignKey('user.id'))

