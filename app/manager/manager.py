from app.config.config import app, db, server
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from app.manager.db import CreateDatabase
from app.manager.load_fixtures import LoadFixtures
from app.manager.seed import seed

migrate = Migrate(app, db)

migrate.init_app(app, db, directory='../../migrations')

manager = Manager(app)

manager.add_command("runserver", server)

manager.add_command('db', MigrateCommand)

manager.add_command('createDb', CreateDatabase)

manager.add_command('loadFixtures', LoadFixtures)

manager.add_command('seed', seed)
