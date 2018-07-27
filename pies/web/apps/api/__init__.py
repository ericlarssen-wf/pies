from flask import current_app
from flask.ext import yarl
from flaskiva.util import load_modules
from werkzeug import LocalProxy


api = yarl.API(name='pies.api', url_prefix='/api', version=1)


def init_app(app):
    def ignore_test_modules(name):
        return 'test' in name

    module_gen = load_modules(
        __name__,
        recursive=False,
        filter=ignore_test_modules
    )

    for name, module in module_gen:
        if hasattr(module, 'init_app'):
            module.init_app(app)

    api.init_app(app)
