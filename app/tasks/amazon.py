import time
from app.config.config import celery, amazon, redis
from app.models.user import UserActions
from app.models.amazon import UserProductActions, ProductActions
from app.models.category import CategoryActions
from app.constants import AMAZON_CATEGORIES
from app.models.post import Post
from app.nlp import nltk
import random


@celery.task(bind=True)
def get_product(self, user):

    product_list = {}
    products = []

    searches = nltk.Nltk.generate_searches(Post.query.filter_by(user_id=user.id))

    print('# of searches')
    print(len(searches))
    print('post searches')
    for i in range(3):
        search = random.choice(searches)
        print(i, search)
        try:
            ps = amazon.search(Keywords=search, SearchIndex=AMAZON_CATEGORIES[0])
            for p in ps:
                product_list[p.title] = p
        except Exception as e:
            print('Exception')
            print(e)
            continue

    for p in product_list.keys():
        print(p.title)
        products.append(product_list[p])

    print('Total # of products')
    print(len(products))

    random.shuffle(products)
    products = products[:100]

    print('Sliced # of products')
    print(len(products))

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
