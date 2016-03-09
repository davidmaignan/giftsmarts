import arrow
import datetime
import pprint
from app.config.config import db


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.String, primary_key=True)
    story = db.Column(db.String, nullable=False)
    created = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.String, db.ForeignKey('user.id'))


class PostActions:
    model = Post

    @classmethod
    def create(cls, post, user):
        try:
            created = arrow.get(post['created_time']).datetime
            story = post['story'] if ('story' in post.keys()) else post['message']

            new_post = cls.model(id=post['id'],
                                 story=story,
                                 created=created,
                                 user_id=user['id']
                                 )
            db.session.add(new_post)
            db.session.commit()
            return new_post
        except Exception:
            return None

    @classmethod
    def create_from_csv(cls, row):
        try:
            # "id","story","created","user_id"
            # created = arrow.get(row[2], 'YYYY-MM-DD HH:mm:ss').datetime

            new_post = cls.model(id=row[0],
                                 story=row[1],
                                 created=datetime.datetime.now(),
                                 user_id=row[3]
                                 )
            db.session.add(new_post)
            db.session.merge()
            return new_post
        except Exception as e:
            pprint.pprint(e)
            return None
