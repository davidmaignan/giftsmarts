import json, xmltodict, jwt, jsonpickle, requests
from flask import g, render_template, request, jsonify, make_response, session, redirect, url_for
from facebook import get_user_from_cookie, GraphAPI
from functools import wraps
from app.controllers.userauthentication import UserAuthentication
from app.models.user import UserActions, FriendRelationshipActions
from app.models.amazon import ProductActions, UserProductActions
from app.config.config import app, db, amazon
from app.tasks import facebook as facebook_task
from app.utils.ActionsFactory import ActionsFactory
from app.config.config import redis
from app.tasks import amazon as amazon_task
from lxml import html
from io import StringIO


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


@app.route("/amazon/", methods=["GET"])
def find_amazon_product():
    products = amazon.search(Keywords='Star Wars', SearchIndex='Books')

    user = UserActions.find_by_id(g.user['id'])

    for product in products:
        redis.set(product.asin, product)
        product = ProductActions.create(product.asin)
        UserActions.add_product(user, product)

    return "Amazon sucess"


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


@app.route("/amazon/comments/", methods=["POST"])
def amazon_user_comments():

    return "amazon user comments"


@app.route("/friend/<string:friend_id>/")
def friend_profile_page(friend_id):
    user = UserActions.find_by_id(g.user['id'])
    friend = UserActions.find_by_id(friend_id)
    # task = amazon_task.get_product.delay(friend)

    # task = amazon_task.get_product.apply_async([friend])

    task = amazon_task.get_product.apply_async([friend])

    products = []
    # user_products = UserProductActions.find_by_user(friend)

    # for user_product in user_products:
    #     product = redis.get(user_product.product_id)
    #     product_dict = xmltodict.parse(product)
    #     products.append(product_dict)

    return render_template("friend_profile.html", app_id=app.config["FB_APP_ID"], user=user, friend=friend, products=products, task=task)


@app.route('/status/<task_id>')
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
    elif task.state != 'FAILURE':
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

        for user_product in user_products:
            product = redis.get(user_product.product_id)
            product_dict = xmltodict.parse(product)
            products.append(product_dict)

        response['products'] = products

    else:
        response = {
            'state': task.state,
            'task_id': task_id,
            'current': 0,
            'total': 0,
            'status': 'Pending...'
        }

    return json.dumps(response)


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


@app.route('/v1/api/<string:entity>/', methods=["GET"])
@app.route('/v1/api/<entity>/<string:id>/', methods=["GET"])
def api_request(entity, id=None):
    if g.user:
        user = UserActions.find_by_id(g.user['id'])

        repository = ActionsFactory.get_repository(entity)
        result = repository.find_by_user(user)

        print(result);

        return jsonify(**{
            "data": "test"
        })
    else:
        return "not connected"


@app.route('/v1/api/<string:entity>/', methods=["PUT"])
def api_request_put(entity):
    if g.user:
        repository = ActionsFactory.get_repository(entity)
        data = jsonpickle.decode(request.data.decode('utf-8'))
        result = repository.put(data['data'])

        return "api_request success: " + str(result) + str(data['data'])
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

