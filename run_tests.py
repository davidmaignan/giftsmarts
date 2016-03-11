import unittest
from tests import all_tests
testSuite = all_tests.create_test_suite()

def addTestCase(test_case):
    testSuite.addTests(unittest.makeSuite(test_case))

def run():
    unittest.TextTestRunner().run(testSuite)
