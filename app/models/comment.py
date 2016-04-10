import arrow
import datetime
import pprint
from app.config.config import db
from flask import g


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, default=mydefault)
    user_id = db.Column(db.String, db.ForeignKey('user.id'))
    subject = db.Column(db.String, nullable=False)
    feedback = db.Column(db.String, nullable=False)
    created = db.Column(db.DateTime, default=db.func.now())
    is_contacted = db.Column(db.String, nullable=False )


class CommentActions:
    model = Comment

    @classmethod
    def create(cls, user, subject, feedback):
        try:
            new_comment = cls.model(user_id= g.user['id'],
                                subject=subject,
                                feedback=feedback,
                                is_contacted=0
                                )
            db.session.add(new_comment)
            db.session.commit()
            return new_comment
        except Exception:
            return None
