import arrow
import datetime
import pprint
from app.config.config import db
from flask import g

i = 0
def mydefault():
    global i
    i += 1
    return i

class Comment(db.Model):
    __tablename__ = 'comment'
    comment_id = db.Column(db.String, primary_key=True, default=mydefault)
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

    @classmethod
    def create_2(cls, comment, user):
        try:
            new_comment = cls.model(user_id=user,
                                    subject=comment['subject'],
                                    feedback=comment['feedback'],
                                    created=db.func.current_timestamp(),
                                    is_contacted=0
                                    )
            db.session.add(new_comment)
            db.session.commit()
            return new_comment
        except Exception:
            return None


    @classmethod
    def create_from_csv(cls, row):
        comment = Comment(id=row[0], user_id=row[1], feedback=row[2], created=arrow.get(row[3]).datetime, is_contacted=row[4])
        db.session.add(comment)
        db.session.commit()
