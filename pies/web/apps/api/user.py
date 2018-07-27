from flaskiva.ext import auth

from . import api


@api.route('/user')
class User(object):
    def get(self):
        user = auth.current_user

        return dict(
            full_name=user.full_name,
            username=user.username,
            email=user.email,
        )
