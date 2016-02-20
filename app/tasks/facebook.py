import pprint
from app.config.config import app, db, celery
from app.models.user import UserActions
from app.models.event import EventActions
from app.models.post import PostActions
from facebook import GraphAPI

@celery.task
def add(x, y):
    # pprint.pprint("debugging task: " + str(x + y))
    return x + y


@celery.task
def get_friends(user):
    graph = GraphAPI(user['access_token'])
    args = {'fields' : 'birthday, name, email'}
    friends = graph.get_object('me/friends', **args)
    UserActions.add_friends(user, friends['data'])

    for friend in friends['data']:
        get_friend_post(user, friend)
        get_friend_event(user, friend)

    return "get friends task completed"


@celery.task
def get_friend_event(user, friend):
    graph = GraphAPI(user['access_token'])

    events = graph.get_connections(friend['id'], 'events')
    for event in events['data']:
        event = EventActions.create(event, friend)
        pprint.pprint(event)

    return "get friend post"


@celery.task
def get_friend_post(user, friend):
    graph = GraphAPI(user['access_token'])

    posts = graph.get_connections(friend['id'], 'posts')
    for post in posts['data']:
        post = PostActions.create(post, friend)
        pprint.pprint(post)

    return "get friend post"