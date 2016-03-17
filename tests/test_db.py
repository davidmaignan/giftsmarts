import unittest
from run_tests import addTestCase
from app.config.config import db, app
from app.models.user import UserActions, FriendRelationshipActions
from app.models.category import CategoryActions
from app.models.post import PostActions
from app.models.event import EventActions
from app.models.amazon import ProductActions, UserProductActions


class DatabaseTest(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://test:Devpass123@localhost/giftsmarts_test"
        db.session.close()
        db.drop_all()
        db.create_all()

        self.profile_1 = ['118600698523151', 'Luke Skywalker Alaaaiffajfch Occhinosky', '', '', '1980-01-30']
        profile_2 = {'id': '118600698523152', 'name': 'Han Solo Alaaaiffajfch Occhinosky', 'birthday': '01/30/1979'}
        profile_3 = {'id': '118600698523153', 'name': 'Padme  Alaaaiffajfch Occhinosky', 'birthday': '01/30/1979'}

        self.user_1 = UserActions.create_user_from_csv(self.profile_1)
        user_2 = UserActions.new_facebook_user(profile_2, {'access_token': 'mock access token'})
        user_3 = UserActions.new_facebook_user(profile_3, {'access_token': 'mock access token'})
        FriendRelationshipActions.create(self.user_1, user_2)
        FriendRelationshipActions.create(self.user_1, user_3)

    def tearDown(self):
        db.session.close()

    # User
    def test_create_user_relations(self):
        relations = FriendRelationshipActions.find_by_user(self.user_1)
        self.assertEqual(2, len(relations))
        self.assertEqual(3, len(UserActions.find_all()))

        # Test relationship
        user = UserActions.find_by_id('118600698523151')
        self.assertEqual('Luke Skywalker Alaaaiffajfch Occhinosky', user.name)
        self.assertEqual(2, len(user.to_friends))

        user = UserActions.find_by_id('118600698523152')
        self.assertEqual(1, len(user.from_owners))

        user = UserActions.find_by_id('118600698523153')
        self.assertEqual(1, len(user.from_owners))
        pass

    # Category
    def test_create_category(self):
        CategoryActions.create("category 1")
        CategoryActions.create("category 2")
        CategoryActions.create("category 3")

        category_1 = CategoryActions.find_by_id("1")
        category_2 = CategoryActions.find_by_id("2")
        self.assertEqual("category 1", category_1.name)
        self.assertEqual(3, len(CategoryActions.find_all()))

        UserActions.add_category(self.user_1, category_1)
        UserActions.add_category(self.user_1, category_2)
        self.assertEqual(2, len(self.user_1.categories))
        pass

    # Post
    def test_create_post(self):
        profile_id = '118600698523151'
        post_1 = {'id': '136485780064997_181349562245285',
                  'message': 'My resolution is to join a gym and start spinning classes',
                  'created_time': '2016-03-11T15:03:46+0000'}

        post = PostActions.create(post_1, profile_id)
        self.assertEqual('136485780064997_181349562245285', post.id)
        self.assertEqual(post_1['message'], post.story)

        post_2 = {'id': '136485780064997_181349562245281',
                  'story': 'My resolution is to relax',
                  'created_time': '2016-03-11T15:03:46+0000'}

        post2 = PostActions.create(post_2, profile_id)
        self.assertEqual(post_2['id'], post2.id)
        self.assertEqual(post_2['story'], post2.story)
        pass

    def test_create_event(self):
        profile_id = '118600698523151'

        event_1 = {'id': '1042331922462207',
                   'name': "We Goin' Shopping!",
                   'description': "Arlene's Grocery is an institution in the musical culture of the lower east side. "
                                  "It says so right here! en.wikipedia.org/wiki/Arlene%27s_Grocery. "
                                  "Anyway, I am very privileged to be able to play here; it would be great to have "
                                  "the support for such a great event. There's an $8 cover. Don't think of it as "
                                  "a Wednesday, because it's the Wednesday before Thanksgiving! "
                                  "www.arlenesgrocery.net",
                   'start_time': '2013-04-06T18:00:00-0400',
                   'user_id': '115772685476890' }

        event = EventActions.create(event_1, profile_id)
        self.assertEqual('1042331922462207', event.id)
        self.assertEqual(event_1['name'], event.name)
        self.assertEqual(event_1['description'], event.description)
        self.assertEqual(profile_id, event.user_id)
        pass

    def test_create_product(self):
        profile_id = '118600698523151'
        user = UserActions.find_by_id(profile_id)
        product = ProductActions.create("123456")
        category = CategoryActions.create("category 1")
        UserProductActions.create(user, product, category)
        user_products = UserProductActions.find_by_user(user)
        self.assertEqual(1, len(user_products))

        user_product = user_products.pop()
        self.assertEqual(user.id, user_product.user_id)
        self.assertEqual(product.id, user_product.product_id)
        self.assertEqual(category.id, user_product.category_id)

if __name__ == '__main__':
    unittest.main()

