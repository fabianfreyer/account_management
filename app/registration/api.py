from flask.json import jsonify
from . import registration_blueprint
from .models import Uni
from app.user import groups_required
from app.oauth2 import oauth

@registration_blueprint.route('/api/unis')
@oauth.require_oauth('uni_list')
def api_unis():
    unis = {uni.id: uni.name for uni in Uni.query.all()}
    return jsonify(unis)
