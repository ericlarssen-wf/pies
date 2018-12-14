import functools

from flask import abort, blueprints, current_app, g, request
from flaskiva.ext import db

blueprint = blueprints.Blueprint(
    'pies.auth',
    __name__
)


def init_app(app):
    app.register_blueprint(blueprint)


def exempt(func):
    """
    A decorator which sets an exempt flag on the function.
    """
    func.auth_exempt = True

    return func


def is_exempt():
    """
    Returns whether the current request is exempt from auth.
    """
    if not request.endpoint:
        return False

    view = current_app.view_functions.get(request.endpoint)

    return getattr(view, 'auth_exempt', False)


def permission_required(permission):
    """
    Decorator that will check to see if the current user has the supplied
    permission.
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
    """
    Check if the current user has the supplied permission.
    """
    return g.user and getattr(g.user, permission, False)
