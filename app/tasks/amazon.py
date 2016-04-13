import time
from app.config.config import celery, amazon, redis
from app.models.user import UserActions
from app.models.amazon import UserProductActions, ProductActions
from app.models.category import CategoryActions


@celery.task(bind=True)
def get_product(self, user):
    products = amazon.search(Keywords='Star Wars', SearchIndex='All')
    # category = CategoryActions.find_by_name("Books")


    for index, product in enumerate(products, start=1):   # default is zero
        product_endity = ProductActions.create(product.asin)
        redis.set(product.asin, product.to_string())

        # check category
        product_category = product.get_attribute('ProductGroup')
        category = CategoryActions.find_by_name(product_category)

        if category is None:
            category = CategoryActions.create(product_category)
            UserActions.add_category(user, category)

        UserProductActions.create(user, product_endity, category)
        self.update_state(state='PROGRESS',
                          meta={
                              'current': index,
                              'total': 100,
                              'user_id': user.id
                          })

    return {'user_id': user.id, 'status': 'Task completed!'}
