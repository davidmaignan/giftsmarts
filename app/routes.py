import json
import jwt
import pprint
import jsonpickle
import json
from flask import g, render_template, request, jsonify, make_response, session, redirect, url_for, Flask, flash
from facebook import get_user_from_cookie, GraphAPI
from amazon.api import AmazonAPI
from functools import wraps
from app.controllers.userauthentication import UserAuthentication
from app.models.user import UserActions, FriendRelationshipActions
from app.models.comment import CommentActions
from app.models.forms import ContactForm
from app.config.config import app, db, celery
from app.tasks import facebook as facebook_task
from app.utils.ActionsFactory import ActionsFactory


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
    facebook_task.get_friends.delay(g.user)
    return redirect(url_for('index'))


@app.route("/amazon/", methods=["GET"])
def find_amazon_product():
    amazon = AmazonAPI(app.config['AMAZON_ACCESS_KEY'],
                       app.config['AMAZON_SECRET_KEY'],
                       app.config['AMAZON_ASSOC_TAG'])
    #
    products = amazon.search(Keywords='Star Wars', SearchIndex='Books')
    #
    # for product in products:
    #     pprint.pprint(product.title)
    #
    # pprint.pprint(product.title)
    return render_template('amazon.html', app_id=app.config["FB_APP_ID"], user=g.user, products=products)


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
            args = {'fields' : 'birthday, name, email'}
            friends = graph.get_object('me/friends', **args);

            for friend in friends['data']:
                UserActions.add_friend(friend)
                FriendRelationshipActions.create(g.user, friend)

            relations = FriendRelationshipActions.find_all_by_user(g.user)

            return render_template("index.html", app_id=app.config["FB_APP_ID"], user=g.user, relations=relations)
        # except Exception:
        #     return redirect(url_for('logout'))

    return render_template("login.html", app_id=app.config["FB_APP_ID"])


@app.route("/friend/<string:friend_id>/")
def friend_profile_page(friend_id):

    user = UserActions.find_by_id(g.user['id'])
    friend = UserActions.find_by_id(str(friend_id))

    return render_template("friend_profile.html", app_id=app.config["FB_APP_ID"], user=user, friend=friend)

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
        repository = ActionsFactory.get_repository(entity)
        result = repository.filter(g.user['id'], entity_id=id)
        return jsonpickle.encode(result.all())
    else:
        return "not connected"


@app.route('/v1/api/<string:entity>/', methods=["PUT"])
def api_request_put(entity):
    if g.user:
        repository = ActionsFactory.get_repository(entity)

        data = jsonpickle.decode(request.data.decode('utf-8'))

        result = repository.put(data['data'])

        # entity_dict = data['data']
        #  user = UserActions.find_by_id(entity_dict['user_id'])

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
            UserActions.create_user(profile, result)
        elif user.access_token != result['access_token']:
            user.access_token = result['access_token']

        user = UserActions.find_by_id(result['uid'])

        session['user'] = dict(name=user.name, profile_url=user.profile_url,
                               id=user.id, access_token=user.access_token)

    db.session.commit()
    g.user = session.get('user', None)

@app.route('/user_feedback', methods=['GET', 'POST'])
def user_feedback():
    user = UserActions.find_by_id(g.user['id'])
    form = ContactForm()

    if request.method == 'POST':
        comment = jsonify(subject=form.subject.data,
                          feedback=form.message.data),

        CommentActions.create(comment, user)
        return render_template('user_feedback.html', success=True, user=user)

    elif request.method == 'GET':
        return render_template("user_feedback.html", form=form, user=user)
