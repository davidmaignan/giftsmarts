from flask.ext.script import Command
from tests.test_nltk import TestNltk

class fb_to_amazon(Command):

    def run(self):
         TestNltk.test_run()
