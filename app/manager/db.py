from flask.ext.script import Command
from app.config.config import db
from app.models.user import FriendRelationShipTypeActions
from app.constants import AMAZON_CATEGORIES
from app.models.category import CategoryActions


class CreateDatabase(Command):
    def run(self):
        print("Drop & Create database")
        db.reflect()
        db.drop_all()
        db.create_all()

        # Load fixtures
        print("Load Relationships type")
        FriendRelationShipTypeActions.create("family")
        FriendRelationShipTypeActions.create("close friend")
        FriendRelationShipTypeActions.create("acquaintance")
        FriendRelationShipTypeActions.create("archived")

        print("Load category")
        for category in AMAZON_CATEGORIES:
            CategoryActions.create(category)


        pass
