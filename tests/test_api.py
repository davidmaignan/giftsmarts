import unittest
from run_tests import addTestCase
from app.config.config import db, app
from app.models.user import UserActions, FriendRelationshipActions, FriendRelationShipTypeActions
from app.models.category import CategoryActions
from app.models.amazon import ProductActions, UserProductActions


class ApiTest(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://test:Devpass123@localhost/giftsmarts_test"
        db.session.close()
        db.drop_all()
        db.create_all()

        FriendRelationShipTypeActions.create("relationship 1")
        FriendRelationShipTypeActions.create("relationship 2")
        FriendRelationShipTypeActions.create("relationship 3")

        self.profile_1 = ['118600698523151', 'Luke Skywalker Alaaaiffajfch Occhinosky', '', '', '1980-01-30']
        profile_2 = {'id': '118600698523152', 'name': 'Han Solo Alaaaiffajfch Occhinosky', 'birthday': '01/30/1979'}
        profile_3 = {'id': '118600698523153', 'name': 'Padme  Alaaaiffajfch Occhinosky', 'birthday': '01/30/1979'}

        self.user_1 = UserActions.create_user_from_csv(self.profile_1)
        user_2 = UserActions.new_facebook_user(profile_2, {'access_token': 'mock access token'})
        user_3 = UserActions.new_facebook_user(profile_3, {'access_token': 'mock access token'})
        FriendRelationshipActions.create(self.user_1, user_2)
        FriendRelationshipActions.create(self.user_1, user_3)

        product_1 = ProductActions.create("1")
        product_2 = ProductActions.create("2")
        category = CategoryActions.create("Book")
        UserProductActions.create(self.user_1, product_1, category)
        UserProductActions.create(self.user_1, product_2, category)

    def tearDown(self):
        db.session.close()

    # User relationship
    def test_friend_relations_filter(self):
        result = FriendRelationshipActions.filter(self.user_1, id=None)
        self.assertEqual(2, len(result))

        result = FriendRelationshipActions.filter(self.user_1)
        self.assertEqual(2, len(result))

        result = FriendRelationshipActions.filter(self.user_1, id=1)
        self.assertEqual(1, len(result))

        result = FriendRelationshipActions.filter(self.user_1, id=3)
        self.assertEqual(0, len(result))
        pass

    # Relationship type
    def test_relation_type_filter(self):
        result = FriendRelationShipTypeActions.filter(self.user_1, id=None)
        self.assertEqual(3, len(result))

        result = FriendRelationShipTypeActions.filter(self.user_1)
        self.assertEqual(3, len(result))

        result = FriendRelationShipTypeActions.filter(self.user_1, id=1)
        self.assertEqual(1, len(result))

        result = FriendRelationshipActions.filter(self.user_1, id=4)
        self.assertEqual(0, len(result))
        pass
