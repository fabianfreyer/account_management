from flask import Blueprint
from flask_login import LoginManager
from flask_ldap3_login import LDAP3LoginManager

user_blueprint = Blueprint('user', __name__, template_folder='templates/')

from . import models, views

def init_app(app):

    login_manager = LoginManager(app)
    ldap_manager = LDAP3LoginManager(app)

    @ldap_manager.save_user
    def save_user(dn, username, data, memberships):
        user = models.User.get(username)
        return user

    @login_manager.user_loader
    def load_user(id):
        return models.User.get(id)

    # Set up sanity checks.
    from . import sanity
    getattr(app, 'sanity_check_modules', []).append(sanity)
