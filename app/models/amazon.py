from app.config.config import db

user_products = db.Table('user_products',
                         db.Column("user_id", db.String, db.ForeignKey("user.id")),
                         db.Column("product_id", db.Integer, db.ForeignKey("product.id"))
                         )


class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)


class ProductActions:
    model = Product

    @classmethod
    def create(cls, id):
        product = cls.model(id=id)
        db.session.add(product)
        db.session.commit()
        return product
