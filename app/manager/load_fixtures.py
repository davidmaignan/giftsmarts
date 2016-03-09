from flask.ext.script import Command
from app.config.config import db
from app.models.user import *


class LoadFixtures(Command):
    def run(self):
        # Relationship
        FriendRelationShipTypeActions.create("family")
        FriendRelationShipTypeActions.create("close friend")
        FriendRelationShipTypeActions.create("acquaintance")

        user1 = UserActions.create(
            {'id': '118600698523150', 'name': 'Padme Alaaaiffajfch Occhinosky', 'profile_url': '',
             'access_token': '', 'birthday': '01/30/1980'})

        user2 = UserActions.create(
            {'id': '118600698523151', 'name': 'Luke skywalker Alaaaiffajfch Occhinosky', 'profile_url': '',
             'access_token': '', 'birthday': '01/30/1980'})

        user3 = UserActions.create(
            {'id': '118600698523152', 'name': 'Han Solo Alaaaiffajfch Occhinosky', 'profile_url': '',
             'access_token': '', 'birthday': '01/30/1980'})

        relationship1 = FriendRelationship();
        relationship1.from_owner = user1;
        relationship1.to_friend = user2;

        relationship2 = FriendRelationship();
        relationship2.from_owner = user1;
        relationship2.to_friend = user3

        db.session.add(relationship1)
        db.session.add(relationship2)
        db.session.commit()


        #
        # FriendRelationshipActions.create(user1, user2)
        # FriendRelationshipActions.create(user1, user3)
        #
        # # Test relation
        # user = UserActions.find_by_id('118600698523150')
        #
        # print(user.friends)

        # c1 = Contact(name="contact 2", background="bg 2")
        # c2 = Contact(name="contact 2", background="bg 2")
        # c3 = Contact(name="contact 3", background="bg 3")
        #
        # cr1 = ContactRelation(relation_type="test 1")
        # cr1.from_contact = c1
        # cr1.to_contact = c2
        #
        # cr2 = ContactRelation(relation_type="test 1")
        # cr2.from_contact = c1
        # cr2.to_contact = c3

        #
        # b = Association(extra_data="more data")
        # b.child = Parent()
        # p.children.append(b)

        # db.session.add(cr1)
        # db.session.add(cr2)
        # db.session.commit()
        #
        item1 = db.session.query(User).get('118600698523150')

        item2 = db.session.query(FriendRelationship).filter(User.id == '118600698523150').all()
        #
        print(item1.to_friends)
        print(item2)

        pass


# class LoadFixtures(Command):
#     def run(self):
#         dir = os.path.dirname(os.path.realpath(__file__))
#
#         #Relationship
#         FriendRelationShipTypeActions.create("family")
#         FriendRelationShipTypeActions.create("close friend")
#         FriendRelationShipTypeActions.create("acquaintance")
#
#         # # user
#         with open(dir + '/users.csv', 'r') as csvfile:
#             spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
#             for row in spamreader:
#                 UserActions.create_user_from_csv(row)
#         # #
#         # #user friends: user_id,friend_id,relation_type,active
#         with open(dir + '/user_friends.csv', 'r') as csvfile:
#             spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
#             for row in spamreader:
#                 UserActions.add_friends_from_csv(row)
#         #
#         # #posts: "id","story","created","user_id"
#         with open(dir + '/posts.csv', 'r') as csvfile:
#             spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
#             for row in spamreader:
#                 PostActions.create_from_csv(row)
#
#         pass