from flaskiva.ext import auth, db

def init_app(app):
    """
    Called when the flask web app is initialising itself
    """
    auth_ctx = auth.get_app_context(app)
