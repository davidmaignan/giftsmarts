import json
import jsonpickle
import jwt
import requests
import xmltodict

from facebook import get_user_from_cookie, GraphAPI

from app.config.config import app, db, amazon
from app.config.config import redis
from app.controllers.userauthentication import UserAuthentication
from app.models.actionfactory import ActionsFactory
from app.models.amazon import ProductActions, UserProductActions
from app.models.serializer import Serializer
from app.models.user import UserActions, FriendRelationshipActions
from app.tasks import amazon as amazon_task
from app.tasks import facebook as facebook_task
from flask import g, render_template, request, jsonify, make_response, session, redirect, url_for
from functools import wraps


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


@app.route("/facebook_friends_data/", methods=["GET"])
def get_facebook_friends_data():
    user = UserActions.find_by_id(g.user['id'])
    facebook_task.get_friends.delay(user)
    return redirect(url_for('index'))


@app.route("/amazon/fetch-products/<string:friend_id>/", methods=["GET"])
def amazon_fetch_product(friend_id):
    user = UserActions.find_by_id(g.user['id'])
    friend = UserActions.find_by_id(friend_id)

    task = amazon_task.get_product.apply_async([friend])

    return jsonify(**{
        "data": {
            'task_id': task.id
        }
    })


@app.route('/amazon/status/<task_id>/')
def taskstatus(task_id):
    task = amazon_task.get_product.AsyncResult(task_id)

    if task.status == "PROGRESS":
        response = {
            'state': task.state,
            'task_id': task_id,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 0),
            'status': 'Pending...'
        }

        friend = UserActions.find_by_id(task.info.get('user_id'))
        products = []
        user_products = UserProductActions.find_by_user(friend)
        result_to_json = Serializer("UserProduct", user_products).run()

        for user_product in result_to_json:
            product = redis.get(user_product['product_id'])
            product_dict = xmltodict.parse(product)
            user_product['product_details']= product_dict
        response['data'] = result_to_json

    elif task.status == 'SUCCESS':
        response = {
            'state': task.state,
            'task_id': task_id,
            'current': 3,
            'total': 3,
            'status': task.status,
        }

        friend = UserActions.find_by_id(task.info.get('user_id'))
        products = []
        user_products = UserProductActions.find_by_user(friend)
        result_to_json = Serializer("UserProduct", user_products).run()

        for user_product in result_to_json:
            product = redis.get(user_product['product_id'])
            product_dict = xmltodict.parse(product)
            user_product['product_details']= product_dict
        response['data'] = result_to_json
    else:
        response = {
            'state': task.state,
            'task_id': task_id,
            'current': 0,
            'total': 0,
            'status': 'Pending...'
        }

    return json.dumps(response)


@app.route("/", methods=["GET"], defaults={'path': ''})
@app.route("/#/", methods=["GET"])
@app.route("/<path:path>/", methods=["GET"])
@app.route("/#/<path:path>/", methods=["GET"])
def index(name="index", *args, **kawrgs):
    if request.is_xhr:
        return "", 400

    if g.user:
        # try:
            graph = GraphAPI(g.user['access_token'])
            args = {'fields': 'birthday, name, email'}
            facebook_friends = graph.get_object('me/friends', **args);

            user = UserActions.find_by_id(g.user['id'])

            for facebook_friend in facebook_friends['data']:
                friend = UserActions.new(facebook_friend)
                FriendRelationshipActions.create(user, friend)

            relations = FriendRelationshipActions.find_by_user(user)

            return render_template("index.html", app_id=app.config["FB_APP_ID"], user=user, relations=relations)
        # except Exception:
        #     return redirect(url_for('logout'))

    return render_template("login.html", app_id=app.config["FB_APP_ID"])


@app.template_filter('to_json')
def to_json(value):
    return json.dumps(value)


@app.template_filter('curl')
def request_reviews(value):
    headers = {'Content-type': 'text/html', 'Accept-Encoding': 'charset=ISO-8859-1'}
    r = requests.get(value, headers)

    return r.text


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


@app.route('/v1/api/<string:entity>/', methods=["GET", "POST"])
@app.route('/v1/api/<entity>/<string:id>/', methods=["GET"])
def api_request(entity, id=None):
    if g.user:
        try:
            # args = request.args.lists()
            user = UserActions.find_by_id(g.user['id'])
            repository = ActionsFactory.get_repository(entity)
            result = repository.filter(user, id=id)

            result_to_json = Serializer(entity, result).run()

            if entity == "UserProduct":
                for elt in result_to_json:
                    product = redis.get(elt['product_id'])
                    product_dict = xmltodict.parse(product)
                    elt['product_details'] = product_dict

            return jsonify(**{
                "data": result_to_json
            })
        except Exception:
            return "Request invalid", 500

    else:
        return "not connected"


@app.route('/v1/api/<string:entity>/', methods=["PUT"])
def api_request_put(entity):
    if g.user:
        repository = ActionsFactory.get_repository(entity)
        data = jsonpickle.decode(request.data.decode('utf-8'))
        result = repository.put(data['data'])
        result_to_json = Serializer(entity, [result]).run()

        return jsonify(**{
                "data": result_to_json
            })
    else:
        return "not connected"


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
            args = {'fields': 'birthday, name, email'}
            profile = graph.get_object('me', **args);
            UserActions.new_facebook_user(profile, result)
        elif user.access_token != result['access_token']:
            user.access_token = result['access_token']

        user = UserActions.find_by_id(result['uid'])

        session['user'] = dict(name=user.name, profile_url=user.profile_url,
                               id=user.id, access_token=user.access_token)

    db.session.commit()
    g.user = session.get('user', None)
