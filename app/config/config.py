from flask import Flask
from flask.ext.mail import Mail
from flask.ext.script import Server
from flask.ext.sqlalchemy import SQLAlchemy
import os
import yaml


#Initialize Application
app = Flask(__name__, template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), '../views'))
app._static_folder = '../../static'


#Load Configs
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


config["JWT_ALGORITHM"] = 'HS512'
config["BCRYPT_ROUNDS"] = 12
#session duration in minutes
config["SESSION_DURATION"] = 15
config["THREADED"] = parsed_config["application"]["threaded"]
config["SECRET_KEY"] = parsed_config["application"]["secret_key"]
config["SQLALCHEMY_DATABASE_URI"] = "postgresql://" + parsed_config["database"]["user"] + ":" + parsed_config["database"]["pass"] + "@" + parsed_config["database"]["host"] + "/" + parsed_config["database"]["name"]

app.config.update(config)


#Create server (WSGI config)
server = Server(host="127.0.0.1", port=parsed_config["application"]["port"])


#Create DB
db = SQLAlchemy(app)


#Create Mail
mail = Mail(app)

# Freeze Model modules so they can be used in the shell
from app.routes import *
# from app.models.relationships import *
from app.models.user import *
from app.models.authtoken import *
from app.models.useremail import *
from app.models.userprofile import *
