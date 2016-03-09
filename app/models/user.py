import bcrypt
import re
import datetime
import pprint
from app.config.config import db
from app.config.config import app
from app.constants import *
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm.exc import NoResultFound


class FriendRelationshipType(db.Model):
    __tablename__ = 'friend_relationship_type'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    profile_url = db.Column(db.String, nullable=False)
    access_token = db.Column(db.String, nullable=False)
    birthday = db.Column(db.Date, nullable=False)
    posts = db.relationship('Post', backref='user_post',
                            lazy='dynamic')
    events = db.relationship('Event', backref='user_event',
                             lazy='dynamic')

    to_friends = association_proxy('to_relations', 'to_friend')
    from_owners = association_proxy('from_relations', 'from_owner')


class FriendRelationship(db.Model):
    __tablename__ = 'friend_relationships'
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.String, db.ForeignKey('user.id'))
    friend_id = db.Column(db.String, db.ForeignKey('user.id'))
    relation_type = db.Column(db.Integer, db.ForeignKey('friend_relationship_type.id'), nullable=True)
    active = db.Column(db.Boolean, default=True)
    from_owner = db.relationship(User, primaryjoin=(owner_id == User.id), backref='to_relations')
    to_friend = db.relationship(User, primaryjoin=(friend_id == User.id), backref='from_relations')


class FriendRelationshipActions:
    model = FriendRelationship

    @classmethod
    def create(cls, user, friend):
        relationship = FriendRelationship();
        relationship.from_owner = user;
        relationship.to_friend = friend;
        db.session.add(relationship)
        return relationship

    @classmethod
    def put(cls, data):
        relation = cls.model.query.filter_by(id=data['id'], owner_id=data['owner_id'], friend_id=data['friend_id']).one()
        relation.relation_type = data['relation_type']
        relation.active = data['active'] == '1'

        db.session.commit()

        return relation


class FriendRelationShipTypeActions:
    model = FriendRelationshipType

    @classmethod
    def create(cls, name):
        try:
            new_user = cls.model(name=name)
            db.session.add(new_user)
            db.session.merge()
        except Exception as e:
            return None


class UserActions:
    model = User

    @classmethod
    def find_all(cls):
        return cls.model.query.all()

    @classmethod
    def find_by_id(cls, user_id):
        try:
            user = cls.model.query.filter_by(id=user_id).one()
            return user
        except Exception:
            return None

    @classmethod
    def create_user_from_csv(cls, row):
        try:
            # id,name,profile_url,access_token,birthday
            birthday = datetime.datetime.strptime(row[4], '%Y-%m-%d').date()

            new_user = cls.model(id=row[0],
                                 name=row[1],
                                 profile_url=row[2],
                                 access_token=row[3],
                                 birthday=birthday)
            db.session.add(new_user)
            db.session.commit()
            return new_user
        except Exception as e:
            pprint.pprint(e)
            return None

    @classmethod
    def create(cls, profile):
        birthday = datetime.datetime.strptime(profile['birthday'], '%m/%d/%Y').date()

        new_user = cls.model(id=profile['id'],
                             name=profile['name'],
                             profile_url="",
                             birthday=birthday,
                             access_token="")
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @classmethod
    def create_user(cls, profile, result):
        birthday = datetime.datetime.strptime(profile['birthday'], '%m/%d/%Y').date()

        new_user = cls.model(id=profile['id'],
                             name=profile['name'],
                             profile_url="",
                             birthday=birthday,
                             access_token=result['access_token'])
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @classmethod
    def add_friends(cls, user, friends):
        user = UserActions.find_by_id(user['id'])

        for friend in friends:

            try:
                friend_entity = cls.model.query.filter_by(id=friend['id']).one()
                relationship = FriendRelationshipActions.create(user, friend_entity)
            except NoResultFound:
                birthday = datetime.datetime.strptime(friend['birthday'], '%m/%d/%Y').date()
                friend_entity = cls.model(id=friend['id'], name=friend['name'], profile_url="",
                                   birthday=birthday, access_token="")
                relationship = FriendRelationshipActions.create(user, friend_entity)



            db.session.commit()

            # ret = db.session.query(exists().where(User.id==friend['id'])).scalar()
            #
            # if ret is not True:
            #     birthday = datetime.datetime.strptime(friend['birthday'], '%m/%d/%Y').date()
            #
            #     new_user = cls.model(id=friend['id'],
            #                          name=friend['name'],
            #                          profile_url="",
            #                          birthday=birthday,
            #                          access_token="")
            #     user.friends.append(new_user)
            #     db.session.commit()

    @classmethod
    def add_friends_from_csv(cls, row):
        try:
            user = UserActions.find_by_id(row[0])
            friend = UserActions.find_by_id(row[1])

            user.friends.append(friend)
            db.session.commit()
        except Exception as e:
            print(e)

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
