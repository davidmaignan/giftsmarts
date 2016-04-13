from flask.ext.script import Command
from app.config.config import db
import fnmatch
import importlib
import os
import run_tests

class test(Command):

    def run(self):
        matches = []
        for root, dirnames, filenames in os.walk('tests'):
            for filename in fnmatch.filter(filenames, '*.py'):
                matches.append(os.path.join(root, filename).split('.py')[0])

        [importlib.import_module('.'.join(m.split('/'))) for m in matches]
        run_tests.run()
