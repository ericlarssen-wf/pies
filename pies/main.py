"""
    GitHub Example
    --------------
    Shows how to authorize users with Github.
"""
import os
import logging

from flask import Flask, request, g, session, redirect, url_for
from flask import render_template_string
from flask_github import GitHub
import app_intelligence
import pyformance

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URI = 'sqlite:////tmp/github-flask.db'
SECRET_KEY = os.getenv('GITHUB_CLIENT_ID', 'development key')
DEBUG = True

# Set these values
GITHUB_CLIENT_ID = os.getenv('GITHUB_CLIENT_ID')
GITHUB_CLIENT_SECRET = os.getenv('GITHUB_CLIENT_SECRET')

# setup flask
app = Flask(__name__)
app.config.from_object(__name__)
app.config['PREFERRED_URL_SCHEME'] = 'https'

# setup github-flask
github = GitHub(app)

# setup sqlalchemy
engine = create_engine(app.config['DATABASE_URI'])
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logsHandler = app_intelligence.logger.Handler()
logger.addHandler(logsHandler)

reporter = app_intelligence.telemetry.Reporter(
    pyformance.global_registry(),
    reporting_interval=5
)
reporter.set_toplevel_metadata(serverInfo='pies')
reporter.start()


def init_db():
    Base.metadata.create_all(bind=engine)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(200))
    github_access_token = Column(String(200))

    def __init__(self, github_access_token):
        self.github_access_token = github_access_token


@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])


@app.after_request
def after_request(response):
    db_session.remove()
    return response


@app.route('/')
def index():
    meta = app_intelligence.metadata(hello='world')
    context = app_intelligence.context(user_id='abc')

    pyformance.counter('homepage.hits').inc()

    with meta, context:
        logging.info('hello')

    logging.info('pies', extra={'some':'metadata', 'account_id': 'abcdefg'})

    if g.user:
        t = 'Hello! <a href="{{ url_for("user") }}">Get user</a> ' \
            '<a href="{{ url_for("logout") }}">Logout</a>'
    else:
        t = 'Hello! <a href="{{ url_for("login") }}">Login</a>'

    return render_template_string(t)


@github.access_token_getter
def token_getter():
    user = g.user
    if user is not None:
        return user.github_access_token

# https://pies.inf-dev.workiva.org/login?next=%Fuser
@app.route('/github-callback')
@github.authorized_handler
def authorized(access_token):
    next_url = request.args.get('next') or url_for('index')
    logger.error('next_url: ' + next_url)
    if access_token is None:
        return redirect(next_url)

    user = User.query.filter_by(github_access_token=access_token).first()
    if user is None:
        user = User(access_token)
        db_session.add(user)
    user.github_access_token = access_token
    db_session.commit()

    session['user_id'] = user.id
    return redirect(next_url)


@app.route('/login')
def login():
    if session.get('user_id', None) is None:
        return github.authorize()
    else:
        return 'Already logged in'


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))


@app.route('/user')
def user():
    return str(github.get('user'))


def run():
    init_db()
    app.run(debug=DEBUG, host='0.0.0.0')
