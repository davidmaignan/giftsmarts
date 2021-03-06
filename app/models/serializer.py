from app.models.schema import *


class Serializer(object):
    def __init__(self, entity, data):
        self.entity = entity
        self.data = data

    def __schema(self):
        if self.entity == "User":
            return UserSchema(many=True)
        elif self.entity == "Friend":
            return UserSchema(many=True)
        elif self.entity == "FriendRelationship":
            return FriendRelationshipSchema(many=True)
        elif self.entity == "UserProduct":
            return UserProductSchema(many=True)
        elif self.entity == "FriendRelationshipType":
            return FriendRelationshipTypeSchema(many=True)
        elif self.entity == "Category":
            return CategorySchema(many=True)
        elif self.entity == "UserCategory":
            return CategorySchema(many=True)
        else:
            assert 0, "Unknown entity for serializer: " + self.entity

    def run(self):
        schema = self.__schema()
        return schema.dump(self.data).data
