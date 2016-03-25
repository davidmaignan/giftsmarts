from marshmallow import Schema, fields, ValidationError, pre_load


def must_not_be_blank(data):
    if not data:
        raise ValidationError('Data not provided.')


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    profile_url = fields.Str()
    birthday = fields.Date(dump_only=True)

    class Meta:
        fields = ("id", "name", "profile_url", "birthday")
        ordered = True


class FriendRelationshipTypeSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()

    class Meta:
        fields = ("id", "name")
        ordered = True


class FriendRelationshipSchema(Schema):
    id = fields.Int(dump_only=True)
    owner_id = fields.Str()
    friend_id = fields.Str()
    relation_type = fields.Integer()
    from_owner = fields.Nested(UserSchema, validate=must_not_be_blank)
    to_friend = fields.Nested(UserSchema, validate=must_not_be_blank)
    relationship = fields.Nested(FriendRelationshipTypeSchema)

    class Meta:
        fields = ("id", "owner_id", "friend_id", "relation_type", "from_owner", "to_friend", "relationship")
        ordered = True


class CategorySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()

    class Meta:
        fields = ("id", "name")
        ordered = True


class ProductSchema(Schema):
    id = fields.Int(dump_only=True)


class UserProductSchema(Schema):
    user_id = fields.Str()
    product_id = fields.Str()
    category_id = fields.Int()
    product = fields.Nested(ProductSchema, validate=must_not_be_blank)

    class Meta:
        fields = ("user_id", "product_id", "category_id", "product")
        ordered = True
