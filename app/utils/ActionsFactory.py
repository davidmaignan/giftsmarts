from app.models.user import UserActions, FriendRelationshipActions
from app.models.friend import FriendActions


class ActionsFactory(object):
    def __init__(self, size):
        self.size = size

    @staticmethod
    def get_repository(entity):
        if entity == "User": return UserActions
        elif entity == "Friend": return FriendActions
        elif entity == "FriendRelationship" : return FriendRelationshipActions
        assert 0, "Bad shape creation: " + type
        return entity

    def get_size(self):
        return self.size


