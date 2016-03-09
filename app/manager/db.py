from flask.ext.script import Command
from app.config.config import db


class CreateDatabase(Command):
    def run(self):
        print("Create database")
        db.reflect()
        db.drop_all()
        db.create_all()
        pass
