# from app.models.relationships import roles_users
from app.constants import ROLES
import bcrypt
import re
import datetime
from app.config.config import db
from app.config.config import app
from app.constants import *


class User(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    profile_url = db.Column(db.String, nullable=False)
    access_token = db.Column(db.String, nullable=False)
    birthday = db.Column(db.Date, nullable=False)

class UserActions():
    model = User

    @classmethod
    def find_by_id(cls, user_id):
        try:
            user = cls.model.query.filter_by(id=user_id).one()
            return user
        except Exception:
            return None

    @classmethod
    def create_user(cls, profile, result):
        try:
            birthday = datetime.datetime.strptime(profile['birthday'], '%m/%d/%Y').date()

            new_user = cls.model(id=profile['id'], name=profile['name'], profile_url="", birthday=birthday, access_token=result['access_token'])
            db.session.add(new_user)
            db.session.commit()
            return user
        except Exception:
            return None

    @classmethod
    def get_username(cls, user_id):
        try:
            user = cls.model.query.filter_by(id=user_id).one()
            print(user.username)
            return user.username
        except Exception:
            return None

    @classmethod
    def add_role(cls, user_id, role_name=None, role_id=None):
        try:
            user = cls.model.query.filter_by(id=user_id).one()
            if role_name is not None:
                user.role = ROLES[role_name]
                return True
            elif role_id is not None:
                user.role = role_id
                return True
            else:
                return None
        except Exception:
            return None

    @classmethod
    def add_user(cls, username, password, active=False):
        if cls._check_valid_add_user(username, password):
            new_user = cls.model(username=username, password=cls.hash_password(password), active=active)
            db.session.add(new_user)
            db.session.commit()

    @classmethod
    def _check_valid_add_user(cls, username, password):
        if cls.check_username_exists(username):
            raise Exception(USERNAME_EXISTS_MSG)

        if not cls.check_valid_username(username):
            raise Exception(INVALID_USERNAME_MSG)

        if not cls.check_valid_password(password):
            raise Exception(INVALID_PASSWORD_MSG)

        return True

    @classmethod
    def check_username_exists(cls, username):
        if cls.model.query.filter_by(username=username).count() > 0:
            return True
        return False

    @classmethod
    def check_valid_username(cls, username):
        return re.match(USERNAME_REGEX, username)

    @classmethod
    def check_valid_password(cls, password):
        return re.match(PASSWORD_REGEX, password)

    @classmethod
    def hash_password(cls, string_password, salt=bcrypt.gensalt(app.config["BCRYPT_ROUNDS"])):
        return bcrypt.hashpw(string_password.encode("UTF-8"), salt)

    @classmethod
    def match_credentials(cls, username, password):
        if not cls.check_valid_username(username) or not cls.check_valid_password(password):
            return False

        try:
            user = cls.model.query.filter_by(username=username).one()
        except Exception:
            return False

        if user:
            if cls.hash_password(password, user.password) == user.password:
                return user
        return False
