from marshmallow import Schema, fields, ValidationError, pre_load, post_load, post_dump
from app.models.category import Category


def must_not_be_blank(data):
    if not data:
        raise ValidationError('Data not provided.')


class CategorySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()

    class Meta:
        fields = ("id", "name")
        ordered = True


class ProductSchema(Schema):
    id = fields.Int(dump_only=True)


class UserProductSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Str()
    product_id = fields.Str()
    category_id = fields.Int()
    product = fields.Nested(ProductSchema, validate=must_not_be_blank)
    category = fields.Nested(CategorySchema, validate=must_not_be_blank)
    active = fields.Boolean()
    wish_list = fields.Boolean();

    class Meta:
        fields = ("user_id", "product_id", "category_id", "product", "category", "active", "wish_list")
        ordered = True


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    profile_url = fields.Str()
    birthday = fields.Date(dump_only=True)

    class Meta:
        fields = ("id", "name", "profile_url", "birthday")
        ordered = True


class UserDetailSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    profile_url = fields.Str()
    birthday = fields.Date(dump_only=True)
    categories = fields.List(fields.Nested(CategorySchema))
    products = fields.List(fields.Nested(UserProductSchema))

    @post_dump
    def set_wish_total(self, item):
        total = 0
        for product in item['products']:
            if product['wish_list'] is True:
                total += 1
        item['context'] = {"wish_total": total}
        return item

    class Meta:
        fields = ("id", "name", "profile_url", "birthday", "categories", "products")
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
    to_friend = fields.Nested(UserDetailSchema, validate=must_not_be_blank)
    relationship = fields.Nested(FriendRelationshipTypeSchema)

    class Meta:
        fields = ("id", "owner_id", "friend_id", "relation_type", "from_owner", "to_friend", "relationship")
        ordered = True


