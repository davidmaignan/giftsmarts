from app.models.user import User


class FriendActions:
    model = User

    @classmethod
    def filter(cls, user_id, entity_id):
        user = cls.model.query.filter_by(id=user_id).one()
        if entity_id is None:
            return user.friends
        else:
            return user.friends.filter(User.id == entity_id)
