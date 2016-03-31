import os, random, csv
from flask.ext.script import Command
from app.models.user import *
from app.models.event import EventActions
from app.models.post import PostActions
from app.models.category import CategoryActions
from app.constants import AMAZON_CATEGORIES
from builtins import open


class LoadFixtures(Command):
    def run(self):
        directory = os.path.dirname(os.path.realpath(__file__))

        # Relationship
        print("Load Relationships type")
        FriendRelationShipTypeActions.create("family")
        FriendRelationShipTypeActions.create("close friend")
        FriendRelationShipTypeActions.create("acquaintance")
        FriendRelationShipTypeActions.create("archived")

        # user
        print("Load Users")
        with open(directory + '/users.csv', 'r') as csv_file:
            spam_reader = csv.reader(csv_file, delimiter=',', quotechar='|')
            for row in spam_reader:
                UserActions.create_user_from_csv(row)

        # id,owner_id,friend_id,relation_type,active
        print("Load Friend relationships")
        with open(directory + '/friend_relationships.csv', 'r') as csv_file:
            spam_reader = csv.reader(csv_file, delimiter=',', quotechar='|')
            for row in spam_reader:
                FriendRelationshipActions.create_from_csv(row)

        # id;story;created;user_id
        print("Load Posts")
        with open(directory + '/posts.csv', 'r') as csv_file:
            spam_reader = csv.reader(csv_file, delimiter=',', quotechar='|')
            for row in spam_reader:
                PostActions.create_from_csv(row)

        # id}name}description}start_time}user_id
        print("Load Events")
        with open(directory + '/events.csv', 'r') as csv_file:
            spam_reader = csv.reader(csv_file, delimiter='}', quotechar='|')
            for row in spam_reader:
                EventActions.create_from_csv(row)

        # Category
        print("Load categories")
        categories = AMAZON_CATEGORIES

        for category in categories:
            CategoryActions.create(category)

        # Assign randomly some category
        print("Load Category per user")
        min = 1
        max = len(categories) + 1

        users = UserActions.find_all();

        for user in users:
            list_numbers = random.sample(range(min, max), random.randint(min + 5, max - 5))
            for number in list_numbers:
                category = CategoryActions.find_by_id(number)
                UserActions.add_category(user, category)

        pass
