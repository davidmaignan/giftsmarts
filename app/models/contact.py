mport arrow
import datetime
import pprint
from app.config.config import db


class Contact(db.Model):
    __tablename__ = 'contact'
    id = db.Column(db.String, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey('user.id'))
    feedback = db.Column(db.String, nullable=False)
    created = db.Column(db.DateTime, nullable=False)
    is_contacted = db.Column(db.String, nullable=False )


class ContactActions:
    model = Contact

    @classmethod
    def create(cls, contact, user):
        try:
            created = arrow.get(contact['created_time']).datetime
            story = contact['feedback'] if ('contact' in post.keys()) else post['message']

            new_feedback = cls.model(id=contact['id'],
                                 user_id=user['id'],
                                 feedback=feedback,
                                 created=created,
                                 is_contacted=0
                                 )
            db.session.add(new_feedback)
            db.session.commit()
            return new_feedback
        except Exception:
            return None

    @classmethod
    def create_from_csv(cls, row):
        contact = Contact(id=row[0], user_id=row[1], feedback=row[2], created=arrow.get(row[3]).datetime, is_contacted=row[4])
        db.session.add(contact)
        db.session.commit()
