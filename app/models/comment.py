import arrow
import datetime
import pprint
from app.config.config import db


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.String, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey('user.id'))
    feedback = db.Column(db.String, nullable=False)
    created = db.Column(db.DateTime, nullable=False)
    is_contacted = db.Column(db.String, nullable=False )


class ContactActions:
    model =Comment

    @classmethod
    def create(cls, comment, user):
        try:
            created = arrow.get(comment['created_time']).datetime
            story = comment['feedback'] if ('comment' in post.keys()) else post['message']

            new_comment = cls.model(id=comment['id'],
                                 user_id=user['id'],
                                 feedback=feedback,
                                 created=created,
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
