from app.nlp import nltk
import unittest
from run_tests import addTestCase

class TestNltk(unittest.TestCase):

    test_text = get_file_text('speech.txt')

    def test_run(self):
        print(nltk.Nltk.findConcordance(self.test_text, ['family', 'job']))

addTestCase(TestNltk)

if __name__ == '__main__':
    unittest.main()
