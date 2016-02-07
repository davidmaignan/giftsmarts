from app.config.config import db
from datetime import datetime, timedelta


class AuthToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(128), unique=False, nullable=False)
    expiration = db.Column(db.DateTime, default=(datetime.now() + timedelta(minutes=15)))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class AuthTokenActions():
    model = AuthToken

    @classmethod
    def add_token(cls, token_payload):
        auth_token = cls.model(token=token_payload["token"], user_id=token_payload["sub"])
        db.session.add(auth_token)
        db.session.commit()

    @classmethod
    def token_expired(cls, token_payload):
        try:
            cls.model.query.filter(user_id=token_payload["sub"], token=token_payload["token"]).one()
        except Exception:
            return True
