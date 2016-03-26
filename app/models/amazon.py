from app.config.config import db
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import exists


class UserProduct(db.Model):
    __tablename__ = 'user_product'
    user_id = db.Column(db.String, db.ForeignKey('user.id'), primary_key=True)
    product_id = db.Column(db.String, db.ForeignKey('product.id'), primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    product = db.relationship("Product", back_populates="users")
    user = db.relationship("User", back_populates="products")
    category = db.relationship("Category", back_populates="user_products")
    active = db.Column(db.Boolean, default=True)


class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.String, primary_key=True)
    users = db.relationship("UserProduct", back_populates="product")


class ProductActions:
    model = Product

    @classmethod
    def create(cls, id):
        try:
            product = cls.model.query.filter_by(id=id).one()
            return product
        except NoResultFound:
            product = cls.model(id=id)
            db.session.add(product)
            db.session.commit()
            return product


class UserProductActions:
    model = UserProduct

    @classmethod
    def filter(cls, user, **kwargs):
        if 'id' in kwargs and kwargs['id'] is not None:
            return cls.model.query.filter_by(user_id=kwargs['id']).all()
        else:
            return None;

    @classmethod
    def create(cls, user, product, category):
        if db.session.query(exists().where(UserProduct.user_id == user.id)
                                    .where(UserProduct.product_id == product.id)).scalar() is not True:
            user_product = UserProduct()
            user_product.user_id = user.id
            user_product.product_id = product.id
            user_product.category_id = category.id
            db.session.add(user_product)
            db.session.commit()
            return user_product

    @classmethod
    def find_by_user(cls, user):
        return cls.model.query.filter_by(user_id=user.id).all()

