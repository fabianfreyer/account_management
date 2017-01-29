from .models import Client, Grant, Token
from flask import current_app
from . import oauth2_blueprint, oauth, admin
from flask_login import login_required

@oauth2_blueprint.route('/oauth/authorize', methods=['GET', 'POST'])
@login_required
@oauth.authorize_handler
def authorize(*args, **kwargs):
    if request.method == 'GET':
        client_id = kwargs.get('client_id')
        client = Client.get(client_id)
        kwargs['client'] = client
        return render_template('oauthorize.html', **kwargs)

    confirm = request.form.get('confirm', 'no')
    return confirm == 'yes'

@oauth2_blueprint.route('/oauth/token', methods=['POST'])
@oauth.token_handler
def access_token():
    return None

