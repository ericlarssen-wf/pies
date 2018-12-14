import json
import logging

import atlas
from atlas.migrate import config, manager, meta
from flask import blueprints, render_template_string, session, current_app
from flaskiva.ext import auth, db


logger = logging.getLogger(__name__)

blueprint = blueprints.Blueprint(
    'pies.base',
    __name__,
)


def init_app(app):
    app.register_blueprint(blueprint)


@blueprint.route('/pies')
def index():
    if auth.current_user:
        t = 'Hello! <a href="{{ url_for("pies.api.user") }}">Get user</a> ' \
            '<a href="{{ url_for("pies.base.logout") }}">Logout</a>'

    return render_template_string(t)

@auth.exempt
@blueprint.route('/health')
def health():
    try:
        core_config = config.load('pies.core')
        meta_manager = meta.MetaManager(prefix='pies')
        meta_manager.connect(db.session.bind)

        migration_manager = manager.MigrateManager(
            core_config.scripts,
            lambda: atlas.Base.metadata,
            meta_manager,
            logger,
            bind=db.session.bind,
        )

        version = migration_manager.schema_version
        max_version = migration_manager.max_version
        if version == max_version:
            return '', 201

        return 'DB version mismatch: {} {}'.format(version, max_version), 429
    except Exception as e:
        return 'DB Exception', 500

@auth.exempt
@blueprint.route('/logout')
def logout():
    session.clear()
    auth.ctx.logout()

    return render_template_string('Logged out! <a href="{{ url_for("pies.base.index") }}">Login</a>')
