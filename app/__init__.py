from flask import Flask, current_app
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

    from app.user import user_blueprint, init_app as init_user
    app.register_blueprint(user_blueprint)
    init_user(app)

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
