from flask import Blueprint

registration_blueprint = Blueprint('registration', __name__, template_folder='templates/')

from . import models, views

def init_app(app):
    pass
