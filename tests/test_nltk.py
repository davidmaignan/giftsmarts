from app.nlp import nltk
import unittest
from tests.utils import get_file_text
from run_tests import addTestCase
from app.models.post import Post
from app.constants import AMAZON_CATEGORIES
from nltk.tag import pos_tag
from app.config.config import amazon
import random

test_text = get_file_text('tests/speech.txt')
test_keywords = [AMAZON_CATEGORIES[0]]
class TestNltk(unittest.TestCase):

    @staticmethod
    def test_run():
        results = {}
        nouns = []
        product_list = {}
        for p in Post.query.all():
            tagged_sent = pos_tag(p.story.split())
            propernouns = [word for word,pos in tagged_sent if pos == 'NNP']
            for n in propernouns:
                if n == "I’m" or n == "It’s" or n == "Can’t":
                    continue
                results[n.replace('.', '')] = True

        for r in results.keys():
            nouns.append(r)

        for i in range(10):
            noun = random.choice(nouns)
            for k in test_keywords:
                try:
                    products = amazon.search(Keywords=noun, SearchIndex=k)
                    for product in products:
                        product_list[product.title] = True
                except:
                    continue

        for p in product_list.keys():
            print("     Found title: %s" % (p,))


addTestCase(TestNltk)

if __name__ == '__main__':
    unittest.main()
