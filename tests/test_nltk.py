from app.nlp import nltk
import unittest
from tests.utils import get_file_text
from run_tests import addTestCase

class TestNltk(unittest.TestCase):

    test_text = get_file_text('tests/speech.txt')
    test_keywords = [
        'family',
        'job',
        'america',
        'freedom'
    ]

    def test_run(self):
        print('Test Find concordance');
        for k in self.test_keywords:
            print(k, nltk.Nltk.find_concordance(k, self.test_text))


addTestCase(TestNltk)

if __name__ == '__main__':
    unittest.main()
