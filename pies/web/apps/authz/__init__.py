from datetime import datetime
import functools

from flask import abort, blueprints
from flaskiva.ext import auth, db
from flaskiva.ext.auth import users

from pies.core.user import User


blueprint = blueprints.Blueprint(
    'pies.authz',
    __name__
)


def init_app(app):
    """
    Called when the flask web app is initialising itself
    """
    app.register_blueprint(blueprint)


@auth.user_logged_in.connect
def user_logged_in(app, **kwargs):
    """
    This is called when a user first logs in to the application.
    :param app: The bound Flask application.
    """
    username = kwargs['user']['username']
    user = db.session.query(User).filter(User.id == username).first()

    if user:
        user.last_login = datetime.utcnow()
    else:
        name = username.rstrip('@workiva.com')
        name = name.replace('.', ' ')
        user = User(id=username, last_login=datetime.utcnow(), name=name)
        db.session.add(user)

    db.session.commit()

def permission_required(permission):
    """
    Decorator that will check the session permissions to see if the supplied
    permission is supported.
    """
    def wrapped(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if not has_permission(permission):
                return abort(403, 'Insufficient permissions')

            return func(*args, **kwargs)

        return wrapper

    return wrapped


def has_permission(permission):
    return permission in auth.current_user.permissions


def is_user_human(user):
    return isinstance(user, users.Human)

