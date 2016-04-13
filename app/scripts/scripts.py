import pprint
import os
from app.config.config import db
from facebook import GraphAPI
from app.models.user import UserActions


def load_fixtures():
    pprint.pprint("Load fixtures -----------------")
    dir = os.path.dirname(os.path.realpath(__file__))
    file = open(dir + '/posts.txt', 'r')
    posts = file.readlines()
    # pprint.pprint(posts)

    users = UserActions.find_all()

    for user in users:
        if user.access_token is not "":
            graph = GraphAPI(user.access_token)
            for post in posts:
                graph.put_object("me", "feed", message=post)


    pprint.pprint("Total user: " + str(len(users)))