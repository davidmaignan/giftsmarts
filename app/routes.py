import json
import jwt
import pprint
from flask import g, render_template, request, jsonify, make_response, session, redirect, url_for
from facebook import get_user_from_cookie, GraphAPI
from functools import wraps
from app.controllers.userauthentication import UserAuthentication
from app.models.user import UserActions
from app.config.config import app, db, celery
from app.tasks import facebook as facebook_task

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


@app.route("/friends/", methods=["GET"])
def test_task():
    task3 = facebook_task.get_friends.delay(g.user)
    return "friend list"


@app.route("/", methods=["GET"], defaults={'path': ''})
@app.route("/#/", methods=["GET"])
@app.route("/<path:path>/", methods=["GET"])
@app.route("/#/<path:path>/", methods=["GET"])
def index(name="index", *args, **kawrgs):
    if request.is_xhr:
        return "", 400

    if g.user:
        try:
            graph = GraphAPI(g.user['access_token'])
            args = {'fields' : 'birthday, name, email, posts, likes, books'}
            friends = graph.get_object('me/friends', **args)

            return render_template("index.html", app_id=app.config["FB_APP_ID"], user=g.user, friends=friends)
        except Exception:
            return redirect(url_for('logout'))

    return render_template("login.html", app_id=app.config["FB_APP_ID"])


@app.route("/robots.txt")
def robots():
    ''' Prevent robots from crawling when not in production '''
    if not app.env == "prod":
        return '''User-agent: *\n\nDisallow: /admin/'''


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

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


@app.before_request
def check_user_logged_in():
    if session.get('user'):
        g.user = session.get('user')
        return

    result = get_user_from_cookie(cookies=request.cookies, app_id=app.config["FB_APP_ID"],
                                  app_secret=app.config["FB_APP_SECRET"])

    if result:
        user = UserActions.find_by_id(result['uid'])

        if not user:
            graph = GraphAPI(result['access_token'])
            args = {'fields' : 'birthday, name, email'}
            profile = graph.get_object('me', **args);

            user = UserActions.create_user(profile, result)
           
        elif user.access_token != result['access_token']:
            user.access_token = result['access_token']

        user = UserActions.find_by_id(result['uid'])

        session['user'] = dict(name=user.name, profile_url=user.profile_url,
                               id=user.id, access_token=user.access_token)

    db.session.commit()
    g.user = session.get('user', None)
