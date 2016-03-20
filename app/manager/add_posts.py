from flask.ext.script import Command
import os
from app.models.user import UserActions
from facebook import GraphAPI


class FacebookPosts(Command):
    def run(self):
        print("Add posts to facebook profile")
        directory = os.path.dirname(os.path.realpath(__file__))
        file = open(directory + '/posts.txt', 'r')
        posts = file.readlines()

        for user in UserActions.find_all():
            if user.access_token is not "":
                graph = GraphAPI(user.access_token)
                for post in posts:
                    print(graph.put_object("me", "feed", message=post))

        pass
