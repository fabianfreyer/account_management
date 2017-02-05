from flask import request
from flask.json import jsonify
from . import registration_blueprint
from .models import Uni, Registration
from app.user import groups_required
from app.oauth2 import oauth
from app.db import db

@registration_blueprint.route('/api/unis')
@oauth.require_oauth('uni_list')
def api_unis():
    unis = {uni.id: uni.name for uni in Uni.query.all()}
    return jsonify(unis)

@registration_blueprint.route('/api/registration', methods=['GET', 'POST'])
@oauth.require_oauth('registration')
def api_register():
    user = request.oauth.user
    if request.method == 'POST' and request.headers.get('Content-Type') == 'application/json':
        req = request.get_json()
        registration = Registration()
        registration.uni_id = req.uni_id
        registration.data = req.data
        db.session.add(registration)
        db.session.commit()
    elif request.method == 'GET':
        registration = Registration.query.filter_by(username=user.username).first()
        return jsonify(
                uni_id = registration.uni_id,
                confirmed = registration.confirmed,
                data = registration.blob,
            )
    else:
        raise NotImplementedError
