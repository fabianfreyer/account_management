from flask import Flask, current_app
from flask_login import LoginManager
from flask_ldap3_login import LDAP3LoginManager
from config import config
import logging

from . import models

def create_app(profile="default"):
    app = Flask(__name__)

    app.config.from_object(config[profile])
    config[profile].init_app(app)
    app.logger.setLevel(logging.DEBUG)

    try:
        logfile = os.path.join(app.config['LOGPATH'], 'anmeldesystem.log')
        loghandler = logging.handlers.RotatingFileHandler(logfile, maxBytes=10**4, backupCount=4)
        loghandler.setLevel(logging.WARNING)
        app.logger.addHandler(loghandler)
    except:
        pass


    login_manager = LoginManager(app)
    ldap_manager = LDAP3LoginManager(app)

    app.users = {}
    @login_manager.user_loader
    def load_user(id):
        if id in app.users:
            return app.users[id]
        return None

    @ldap_manager.save_user
    def save_user(dn, username, data, memberships):
        user = models.User(dn, username, data)
        app.logger.info("saving user %r" % ((dn, username, data),))
        app.users[dn] = user
        return user

    from app.user import user_blueprint
    app.register_blueprint(user_blueprint)

    from app.oauth2 import oauth2_blueprint, init_app as init_oauth2
    app.register_blueprint(oauth2_blueprint)
    init_oauth2(app)

    return app

def check_sanity(fix=True):
    from . import sanity
    for i in dir(sanity):
        item = getattr(sanity,i)
        if callable(item) and i.startswith('check'):
            item(fix)
