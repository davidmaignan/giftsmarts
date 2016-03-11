from flask.ext.script import Command
from app.config.config import db
from app.models.user import *
from app.models.event import EventActions
from app.models.post import PostActions
import csv
import os
from builtins import open


class LoadFixtures(Command):
    def run(self):
        directory = os.path.dirname(os.path.realpath(__file__))

        # Relationship
        FriendRelationShipTypeActions.create("family")
        FriendRelationShipTypeActions.create("close friend")
        FriendRelationShipTypeActions.create("acquaintance")

        # user
        with open(directory + '/users.csv', 'r') as csv_file:
            spam_reader = csv.reader(csv_file, delimiter=',', quotechar='|')
            for row in spam_reader:
                UserActions.create_user_from_csv(row)

        # id,owner_id,friend_id,relation_type,active
        with open(directory + '/friend_relationships.csv', 'r') as csv_file:
            spam_reader = csv.reader(csv_file, delimiter=',', quotechar='|')
            for row in spam_reader:
                FriendRelationshipActions.create_from_csv(row)

        # id;story;created;user_id
        with open(directory + '/posts.csv', 'r') as csv_file:
            spam_reader = csv.reader(csv_file, delimiter=',', quotechar='|')
            for row in spam_reader:
                PostActions.create_from_csv(row)

        # id}name}description}start_time}user_id
        with open(directory + '/events.csv', 'r') as csv_file:
            spam_reader = csv.reader(csv_file, delimiter='}', quotechar='|')
            for row in spam_reader:
                EventActions.create_from_csv(row)

        pass
