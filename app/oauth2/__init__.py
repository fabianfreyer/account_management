from flask import Blueprint
from flask_oauthlib.provider import OAuth2Provider

oauth2_blueprint = Blueprint('oauth2', __name__,)

from . import views

def init_app(app):
    oauth = OAuth2Provider(app)
    oauth.init_app(app)
    app.oauth2_provider = oauth

    # Set up sanity checks.
    from . import sanity
    getattr(app, 'sanity_check_modules', []).append(sanity)

    return app
