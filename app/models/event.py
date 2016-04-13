import arrow
from app.config.config import db


class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.String, db.ForeignKey('user.id'))


class EventActions:
    model = Event

    @classmethod
    def create(cls, event, user_id):
        try:
            start_time = arrow.get(event['start_time']).datetime
            new_event = cls.model(id=event['id'],
                                  name=event['name'],
                                  description=event['description'],
                                  start_time=start_time,
                                  user_id=user_id
                                  )
            db.session.add(new_event)
            db.session.commit()
            return new_event
        except Exception as detail:
            return None

    @classmethod
    def create_from_csv(cls, row):
        event = Event(id=row[0], name=row[1], description=row[2], start_time=arrow.get(row[3]).datetime, user_id=row[4])
        db.session.add(event)
        db.session.commit()
