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
    'pies.web.apps.authz'
]

SESSION_REDIS_HOSTS = None
if os.getenv('SESSION_REDIS_HOSTS'):
    SESSION_REDIS_HOSTS = os.getenv('SESSION_REDIS_HOSTS').split(',')
    SESSION_REDIS_AUTH = os.getenv('SESSION_REDIS_AUTH')

SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', True)
SESSION_COOKIE_HTTPONLY = os.getenv('SESSION_COOKIE_HTTPONLY', True)

SERVER_NAME = os.getenv('SERVER_NAME')
WTF_CSRF_TIME_LIMIT = int(os.getenv('WTF_CSRF_TIME_LIMIT', 3600))

num_proto = os.getenv('PROXY_NUM_PROTO')
if num_proto:
    PROXY_NUM_PROTO = num_proto
