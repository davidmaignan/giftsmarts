from flask import render_template, request, jsonify, make_response
import json
from functools import wraps
from app.controllers.userauthentication import UserAuthentication
from app.models.user import UserActions
from app.config.config import app
from app.lib import jwt


def not_found():
    return "", 404


def not_authorized():
    return "", 403


def bad_auth():
    return "", 401


def get_request_args():
    if request.data:
        return json.loads(request.data.decode("utf-8"))
    return {}


def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        authorization = request.headers.get("Authorization", None)

        if authorization is None:
            return not_authorized()

        token = jwt.valid_token(authorization[7:])

        if token is None:
            return not_authorized()

        kwargs["token"] = token

        resp = make_response(f(*args, **kwargs))
        resp.headers["token"] = "Bearer " + token
        return resp
    return decorated_function


@app.route("/", methods=["GET"], defaults={'path': ''})
@app.route("/#/", methods=["GET"])
@app.route("/<path:path>/", methods=["GET"])
@app.route("/#/<path:path>/", methods=["GET"])
def index(name="index", *args, **kawrgs):
    if request.is_xhr:
        return "", 400
    return render_template("index.html")


@app.route("/robots.txt")
def robots():
    ''' Prevent robots from crawling when not in production '''
    if not app.env == "prod":
        return '''User-agent: *\n\nDisallow: /admin/'''


@app.route("/api/auth/login", methods=["POST"])
def login(name="login"):

    args = get_request_args()

    if not "username" in args or not "password" in args:
        return not_found()

    user_token = UserAuthentication.login(args["username"], args["password"])

    if user_token is None:
        return bad_auth()

    return jsonify(**{
        "token": user_token
    })


@app.route("/api/user/username", methods=["GET"])
@token_required
def username(name="username", token=None):

    user_id = jwt.get_payload(token)["sub"]
    username = UserActions.get_username(user_id)

    return jsonify(**{
        "username": username
    })
