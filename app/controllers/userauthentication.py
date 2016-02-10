from app.models.user import UserActions
import jwt


class UserAuthentication():

    def login(username, password, *args, **kwargs):
        user = UserActions.match_credentials(username, password)
        if user:
            return jwt.create_auth_token(user)
        return None
