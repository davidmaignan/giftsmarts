from builtins import classmethod, Exception
import bcrypt
import re
import datetime
from app.config.config import db
from app.config.config import app
from app.constants import *
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import exists
from sqlalchemy.orm import relationship
from app.models.category import Category, user_categories
from app.models.amazon import UserProduct


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
    categories = relationship("Category", secondary=user_categories)
    products = relationship("UserProduct", back_populates="user")


class FriendRelationship(db.Model):
    __tablename__ = 'friend_relationships'
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.String, db.ForeignKey('user.id'))
    friend_id = db.Column(db.String, db.ForeignKey('user.id'))
    relation_type = db.Column(db.Integer, db.ForeignKey('friend_relationship_type.id'), nullable=True)
    active = db.Column(db.Boolean, default=True)
    relationship = db.relationship(FriendRelationshipType)
    from_owner = db.relationship(User, primaryjoin=(owner_id == User.id), backref='to_relations')
    to_friend = db.relationship(User, primaryjoin=(friend_id == User.id), backref='from_relations')


class FriendRelationshipActions:
    model = FriendRelationship

    @classmethod
    def filter(cls, user, **kwargs):
        if kwargs['id'] is not None:
            return cls.model.query.filter_by(owner_id=user.id, id=kwargs['id']).all()
        else:
            return cls.model.query.filter_by(owner_id=user.id).all()


    @classmethod
    def find_by_user(cls, user):
        return cls.model.query.filter_by(owner_id=user.id).all()

    @classmethod
    def create(cls, user, friend, relation_type=None):
        if db.session.query(exists().where(FriendRelationship.owner_id == user.id)
                                    .where(FriendRelationship.friend_id == friend.id)).scalar() is not True:
            rel = FriendRelationship(owner_id=user.id, friend_id=friend.id)
            rel.from_owner = user
            rel.to_friend = friend
            if relation_type is not None:
                rel.relation_type=relation_type.id
                rel.relationship = relation_type
            db.session.add(rel)
            db.session.commit()
            return rel

    @classmethod
    def create_from_csv(cls, row):
        rel = FriendRelationship(owner_id=row[0], friend_id=row[1], relation_type=row[2])
        db.session.add(rel)
        db.session.commit()

    @classmethod
    def put(cls, data):
        relation = cls.model.query.filter_by(id=data['id'],
                                             owner_id=data['owner_id'],
                                             friend_id=data['friend_id']).one()
        relation.relation_type = data['relation_type']
        relation.active = data['active'] == '1'
        db.session.commit()
        return relation


class FriendRelationShipTypeActions:
    model = FriendRelationshipType

    @classmethod
    def find_by_name(cls, name):
        return cls.model.query.filter_by(name=name).one()

    @classmethod
    def create(cls, name):
        try:
            new_rel = cls.model(name=name)
            db.session.add(new_rel)
            db.session.merge()
        except Exception as e:
            return None


class UserActions:
    model = User

    @classmethod
    def filter(cls, user, **kwargs):
        if kwargs['id'] is None:
            return cls.model.query.all()
        else:
            return cls.model.query.filter_by(id=kwargs['id']).all()

    @classmethod
    def add_product(cls, user, product):
        user.products.append(product)
        db.session.commit()

    @classmethod
    def add_category(cls, user, category):
        user.categories.append(category)
        db.session.commit()

    @classmethod
    def find_all(cls):
        return cls.model.query.all()

    @classmethod
    def find_by_id(cls, user_id):
        try:
            user = cls.model.query.filter_by(id=user_id).one()
            return user
        except NoResultFound:
            return None

    @classmethod
    def create_user_from_csv(cls, row):
        birthday = datetime.datetime.strptime(row[4], '%Y-%m-%d').date()

        new_user = cls.model(id=row[0],
                             name=row[1],
                             profile_url=row[2],
                             access_token=row[3],
                             birthday=birthday)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @classmethod
    def new_facebook_user(cls, profile, result):
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
    def new(cls, user):
        if db.session.query(exists().where(User.id == user['id'])).scalar() is not True:
            birthday = datetime.datetime.strptime(user['birthday'], '%m/%d/%Y').date()
            new_user = cls.model(id=user['id'],
                                 name=user['name'],
                                 profile_url="",
                                 birthday=birthday,
                                 access_token="")
            db.session.add(new_user)
            db.session.commit()
            return new_user
        else:
            return UserActions.find_by_id(user['id'])

    @classmethod
    def get_username(cls, user_id):
        try:
            user = cls.model.query.filter_by(id=user_id).one()
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
