from app.config.config import db

user_categories = db.Table('user_categories',
                           db.Column("user_id", db.String, db.ForeignKey("user.id")),
                           db.Column("category_id", db.Integer, db.ForeignKey("category.id"))
                           )


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)


class CategoryActions:
    model = Category

    @classmethod
    def find_by_id(cls, id):
        try:
            category = cls.model.query.filter_by(id=id).one()
            return category
        except Exception as e:
            print(e)
            return None

    @classmethod
    def create(cls, name):
        try:
            new_category = cls.model(name=name)
            db.session.add(new_category)
            db.session.commit()
        except Exception as e:
            print(e)
            return None
