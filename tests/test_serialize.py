import unittest, json
from run_tests import addTestCase
from flask import jsonify
from app.config.config import db, app
from app.models.user import UserActions, FriendRelationshipActions
from app.models.schema import *
from app.models.user import FriendRelationShipTypeActions
from app.models.category import CategoryActions
from app.models.post import PostActions
from app.models.event import EventActions
from app.models.amazon import ProductActions, UserProductActions


class SerializeTest(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://test:Devpass123@localhost/giftsmarts_test"
        db.session.close()
        db.drop_all()
        db.create_all()

        self.profile_1 = ['118600698523151', 'Luke Skywalker Alaaaiffajfch Occhinosky', '', '', '1980-01-30']
        profile_2 = {'id': '118600698523152', 'name': 'Han Solo Alaaaiffajfch Occhinosky', 'birthday': '01/30/1979'}
        profile_3 = {'id': '118600698523153', 'name': 'Padme  Alaaaiffajfch Occhinosky', 'birthday': '01/30/1979'}

        family_rel_name = "family"
        friend_rel_name = "friend"

        FriendRelationShipTypeActions.create(family_rel_name)
        FriendRelationShipTypeActions.create(friend_rel_name)
        FriendRelationShipTypeActions.create("acquaintance")

        rel_family = FriendRelationShipTypeActions.find_by_name(family_rel_name)
        rel_friend = FriendRelationShipTypeActions.find_by_name(friend_rel_name)

        self.user_1 = UserActions.create_user_from_csv(self.profile_1)
        user_2 = UserActions.new_facebook_user(profile_2, {'access_token': 'mock access token'})
        user_3 = UserActions.new_facebook_user(profile_3, {'access_token': 'mock access token'})
        FriendRelationshipActions.create(self.user_1, user_2, rel_family)
        FriendRelationshipActions.create(self.user_1, user_3, rel_friend)

    def tearDown(self):
        db.session.close()

    # User
    def test_user_serialize(self):
        user_schema = UserSchema(many=True)
        users = UserActions.find_all()
        user_result = user_schema.dump(users)
        user_result_json = json.dumps(user_result.data)
        user_expected_json = '[{"id": 118600698523151, "name": "Luke Skywalker Alaaaiffajfch Occhinosky",' \
                             ' "profile_url": "", "birthday": "1980-01-30"}, {"id": 118600698523152, "name": ' \
                             '"Han Solo Alaaaiffajfch Occhinosky", "profile_url": "", "birthday": "1979-01-30"}, ' \
                             '{"id": 118600698523153, "name": "Padme  Alaaaiffajfch Occhinosky", ' \
                             '"profile_url": "", "birthday": "1979-01-30"}]'

        self.assertEqual(user_expected_json, user_result_json)
        pass

    def test_friend_relationship_serialize(self):
        relationships = FriendRelationshipActions.find_by_user(self.user_1)
        friend_relationship_schema = FriendRelationshipSchema(many=True)
        friend_relationship_result = friend_relationship_schema.dump(relationships)
        relationships_result_json = json.dumps(friend_relationship_result.data)
        relationships_expected_json = '[{"id": 1, "owner_id": "118600698523151", "friend_id": "118600698523152", ' \
                                      '"relation_type": 1, "from_owner": {"id": 118600698523151,' \
                                      ' "name": "Luke Skywalker Alaaaiffajfch Occhinosky", "profile_url": "", ' \
                                      '"birthday": "1980-01-30"}, "to_friend": {"id": 118600698523152, ' \
                                      '"name": "Han Solo Alaaaiffajfch Occhinosky", "profile_url": "", ' \
                                      '"birthday": "1979-01-30"}, "relationship": {"id": 1, "name": "family"}}, ' \
                                      '{"id": 2, "owner_id": "118600698523151", "friend_id": "118600698523153", ' \
                                      '"relation_type": 2, "from_owner": {"id": 118600698523151, ' \
                                      '"name": "Luke Skywalker Alaaaiffajfch Occhinosky", "profile_url": "", ' \
                                      '"birthday": "1980-01-30"}, "to_friend": {"id": 118600698523153, ' \
                                      '"name": "Padme  Alaaaiffajfch Occhinosky", "profile_url": "", ' \
                                      '"birthday": "1979-01-30"}, "relationship": {"id": 2, "name": "friend"}}]'

        self.assertEqual(relationships_expected_json, relationships_result_json)
        pass

    def test_user_product(self):
        product_1 = ProductActions.create("1")
        product_2 = ProductActions.create("2")
        category = CategoryActions.create("Book")
        UserProductActions.create(self.user_1, product_1, category)
        UserProductActions.create(self.user_1, product_2, category)

        products = UserProductActions.find_by_user(self.user_1)

        user_product_schema = UserProductSchema(many=True)
        user_product_result = user_product_schema.dump(products)
        user_product_json = json.dumps(user_product_result.data)

        expected = '[{"user_id": "118600698523151", "product_id": "1", "category_id": 1, "product": {"id": 1}, ' \
                   '"user": {"id": 118600698523151, "name": "Luke Skywalker Alaaaiffajfch Occhinosky",' \
                   ' "profile_url": "", "birthday": "1980-01-30"}}, ' \
                   '{"user_id": "118600698523151", "product_id": "2", "category_id": 1, "product": {"id": 2}, ' \
                   '"user": {"id": 118600698523151, "name": "Luke Skywalker Alaaaiffajfch Occhinosky", ' \
                   '"profile_url": "", "birthday": "1980-01-30"}}]'

        self.assertEqual(expected, user_product_json)

        pass
