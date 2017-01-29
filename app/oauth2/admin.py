"""
Administrative views for OAuth2.
"""
from flask import render_template, url_for, \
            redirect, flash, request, current_app
from flask_login import login_required
from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField
from wtforms.validators import DataRequired

from .models import Client
from . import oauth2_blueprint

# FIXME: This should be only accessible by admins.
@login_required
@oauth2_blueprint.route('/admin/oauth2/client')
def clients():
    clients = Client.query()
    return render_template('/admin/oauth2/clients.html', clients=clients)


@login_required
@oauth2_blueprint.route('/admin/oauth2/client/<string:client_id>/delete')
def delete_client(client_id):
    client = Client.get(client_id)
    flash('Deleted client: {uuid}({name})'.format(
        uuid = client.client_id,
        name = client.name))
    client.delete()
    return redirect(url_for('oauth2.clients'))


@login_required
@oauth2_blueprint.route('/admin/oauth2/client/new', methods=['GET', 'POST'])
def add_client():
    class AddClientForm(FlaskForm):
        name = StringField('name', validators=[DataRequired()])
        description = TextField('description')
        submit =SubmitField('Submit')
    form = AddClientForm()
    if form.validate_on_submit():
        client = Client.create(name=form.name.data, description=form.description.data)
        flash("Added client. Secret key is {secret_key}".format(
            secret_key = client.client_secret
            ))
        return redirect(url_for('oauth2.clients'))

    return render_template('/admin/oauth2/new.html', form=form)
