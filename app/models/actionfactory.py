from app.models.user import UserActions, FriendRelationshipActions, FriendRelationShipTypeActions, UserCategoryActions
from app.models.friend import FriendActions
from app.models.amazon import UserProductActions
from app.models.category import CategoryActions


class ActionsFactory(object):
    def __init__(self, size):
        self.size = size

    @staticmethod
    def get_repository(entity):
        if entity == "User":
            return UserActions
        elif entity == "FriendRelationship":
            return FriendRelationshipActions
        elif entity == "FriendRelationshipType":
            return FriendRelationShipTypeActions
        elif entity == "UserProduct":
            return UserProductActions
        elif entity == "Category":
            return CategoryActions
        elif entity == "UserCategory":
            return UserCategoryActions
        assert 0, "Entity not supported: " + entity
        return entity

    def get_size(self):
        return self.size
