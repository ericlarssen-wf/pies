import os

FLASKIVA_AUTH_PROVIDER = 'github'

GITHUB_CLIENT_ID = os.getenv('GITHUB_CLIENT_ID')
GITHUB_CLIENT_SECRET = os.getenv('GITHUB_CLIENT_SECRET')
GITHUB_SCOPE = os.environ.get('GITHUB_SCOPE', 'user,repo')
GITHUB_WHITELISTED_ORGS = os.getenv('GITHUB_WHITELISTED_ORGS', 'Workiva')

DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:////tmp/github-flask.db')

INSTALLED_APPS = [
    'pies.web.apps.api',
    'pies.web.apps.base',
]

SERVER_NAME = os.getenv('SERVER_NAME')
SECRET_KEY = 'secret_key'
CSRF_ENABLED = False
