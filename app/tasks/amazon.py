from app.config.config import celery, amazon, redis
from app.models.user import UserActions
from app.models.amazon import UserProductActions, ProductActions
from app.models.category import CategoryActions


@celery.task
def get_product(user):
    products = amazon.search(Keywords='Star Wars', SearchIndex='Books')

    category = CategoryActions.find_by_name("Books")

    for product in products:
        product_entity = ProductActions.create(product.asin)
        print(product_entity)
        redis.set(product.asin, product.to_string())
        UserProductActions.create(user, product_entity, category)
    pass

