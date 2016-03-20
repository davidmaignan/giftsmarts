from app.nlp import rake
import unittest
from run_tests import addTestCase
from utils import get_file_text



class TestRake(unittest.TestCase):

    test_text = get_file_text('speech.txt')

    def test_run(self):
        keywords = rake.run(self.test_text)
        self.assertGreater(len(keywords), 0)
        self.assertEquals(keywords[0], ('helps families find jobs', 13.333333333333334))
        self.assertEquals(keywords[16], ('make hard choices', 7.333333333333334))

addTestCase(TestRake)

if __name__ == '__main__':
    unittest.main()
