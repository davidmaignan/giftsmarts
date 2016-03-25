from app.models.user import UserActions, FriendRelationshipActions
from app.models.friend import FriendActions
from app.models.amazon import UserProductActions


class ActionsFactory(object):
    def __init__(self, size):
        self.size = size

    @staticmethod
    def get_repository(entity):
        if entity == "User": return UserActions
        elif entity == "FriendRelationship" : return FriendRelationshipActions
        elif entity == "UserProduct": return UserProductActions
        assert 0, "Entity not supported: " + entity
        return entity

    def get_size(self):
        return self.size


