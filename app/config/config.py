from flask import Flask
from flask.ext.mail import Mail
from flask.ext.script import Server
from flask.ext.sqlalchemy import SQLAlchemy
from flask_redis import Redis
from app.tasks.celery import make_celery
from amazon.api import AmazonAPI
import os
import yaml

# Initialize Application
app = Flask(__name__, template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), '../views'))
app._static_folder = '../../static'

# Load Configs
parsed_config = None
config = {}
config_path = None

env = os.environ.get('FLASK_ENV')

if env == "prod":
    config_path = "config_prod.yaml"
else:
    config_path = "config_dev.yaml"

with open(config_path, 'r') as stream:
    parsed_config = yaml.load(stream)


config["STOPLIST"] = 'data/stoplist.txt'

config["JWT_ALGORITHM"] = 'HS512'
config["BCRYPT_ROUNDS"] = 12
# session duration in minutes
config["SESSION_DURATION"] = 15
config["THREADED"] = parsed_config["application"]["threaded"]
config["SECRET_KEY"] = parsed_config["application"]["secret_key"]
config["FB_APP_ID"] = parsed_config["facebook"]["id"]
config["FB_APP_NAME"] = parsed_config["facebook"]["name"]
config["FB_APP_SECRET"] = parsed_config["facebook"]["secret"]
config["SQLALCHEMY_DATABASE_URI"] = "postgresql://" + parsed_config["database"]["user"] + ":" + \
                                    parsed_config["database"]["pass"] + "@" + parsed_config["database"]["host"] + "/" + \
                                    parsed_config["database"]["name"]
app.config['CELERY_BROKER_URL'] = "redis://" \
                                  + parsed_config['celery']['broker_url']['host'] \
                                  + ":" \
                                  + str(parsed_config['celery']['broker_url']['port'])
app.config['CELERY_RESULT_BACKEND'] = "redis://" \
                                      + parsed_config['celery']['result_backend']['host'] \
                                      + ":" \
                                      + str(parsed_config['celery']['result_backend']['port'])
app.config['AMAZON_ACCESS_KEY'] = parsed_config['amazon']['access_key']
app.config['AMAZON_SECRET_KEY'] = parsed_config['amazon']['secret_key']
app.config['AMAZON_ASSOC_TAG'] = parsed_config['amazon']['assoc_tag']

app.config['REDIS_HOST'] = parsed_config['redis']['host']
app.config['REDIS_PORT'] = parsed_config['redis']['port']
app.config['REDIS_DB'] = parsed_config['redis']['db']

app.config.update(config)

# Create server (WSGI config)
server = Server(host="0.0.0.0", port=parsed_config["application"]["port"])

# Create DB
db = SQLAlchemy(app)

# Create Mail
mail = Mail(app)

# Celery
celery = make_celery(app)

# Redis
redis = Redis(app)

# amazon
amazon = AmazonAPI(app.config['AMAZON_ACCESS_KEY'],
                   app.config['AMAZON_SECRET_KEY'],
                   app.config['AMAZON_ASSOC_TAG'])

# Freeze Model modules so they can be used in the shell
from app.routes import *
from app.models.relationships import *
from app.models.user import *
from app.models.authtoken import *
from app.models.useremail import *
from app.models.userprofile import *
from app.models.post import *
from app.models.event import *
from app.scripts.scripts import *
