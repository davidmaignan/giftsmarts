import pprint
from app.config.config import celery
from app.models.user import UserActions, FriendRelationshipActions
from app.models.event import EventActions
from app.models.post import PostActions
from facebook import GraphAPI


@celery.task
def get_friends(user):
    graph = GraphAPI(user.access_token)
    args = {'fields' : 'birthday, name, email'}
    facebook_friends = graph.get_object('me/friends', **args)

    for facebook_friend in facebook_friends['data']:
        friend = UserActions.new(facebook_friend)
        FriendRelationshipActions.create(user, friend)
        get_friend_post(facebook_friend, user.access_token)
        get_friend_event(facebook_friend, user.access_token)
    pass


@celery.task
def get_friend_event(user, access_token):
    graph = GraphAPI(access_token)

    events = graph.get_connections(user['id'], 'events')
    for event in events['data']:
        event = EventActions.create(event, user['id'])
    pass


@celery.task
def get_friend_post(user, access_token):
    graph = GraphAPI(access_token)

    posts = graph.get_connections(user['id'], 'posts')
    for post in posts['data']:
        post = PostActions.create(post, user['id'])
    pass
