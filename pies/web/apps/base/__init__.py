from flask import blueprints, render_template_string, session, current_app
from flaskiva.ext import auth


blueprint = blueprints.Blueprint(
    'pies.base',
    __name__,
)


def init_app(app):
    app.register_blueprint(blueprint)


@blueprint.route('/')
def index():
    # t = 'Hello!'
    if auth.current_user:
        t = 'Hello! <a href="{{ url_for("pies.api.user") }}">Get user</a> ' \
            '<a href="{{ url_for("pies.base.logout") }}">Logout</a>'

    return render_template_string(t)

@auth.exempt
@blueprint.route('/logout')
def logout():
    session.clear()
    auth.ctx.logout()

    return render_template_string('Logged out! <a href="{{ url_for("pies.base.index") }}">Login</a>')
