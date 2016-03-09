<<<<<<< HEAD
from app.config.config import db
from app.config.config import app
from app.constants import *
from sqlalchemy.orm import relationship
=======
import arrow
from app.config.config import db
>>>>>>> b82e2790df929b4ddf424b58a4b40a8593f5ad21


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.String, primary_key=True)
    story = db.Column(db.String, nullable=False)
    created = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.String, db.ForeignKey('user.id'))

<<<<<<< HEAD
=======

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
>>>>>>> b82e2790df929b4ddf424b58a4b40a8593f5ad21
