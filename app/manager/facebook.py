from flask.ext.script import Command
from app.models.user import UserActions
from app.models.event import EventActions
from app.models.post import PostActions
from facebook import GraphAPI


class FacebookData(Command):
    def run(self):
        print("Get friends datas from facebook")

        user = UserActions.find_by_id('118600698523150')
        graph = GraphAPI(user.access_token)
        args = {'fields' : 'birthday, name, email'}
        friends = graph.get_object('me/friends', **args)

        for friend in friends['data']:
            UserActions.create(friend)
            posts = graph.get_connections(friend['id'], 'posts')
            for post in posts['data']:
                post = PostActions.create(post, friend)
                print(post)
        pass
