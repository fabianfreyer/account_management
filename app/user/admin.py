from flask import render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, Optional
from wtforms.fields.html5 import EmailField
from app.views import confirm
from . import groups_required, user_blueprint
from .models import User

class UserEditForm(FlaskForm):
    username = StringField('Username')
    givenName = StringField('Given Name', validators=[DataRequired('Please enter a given name')])
    surname = StringField('Surname', validators=[DataRequired('Please enter a surname')])
    mail = EmailField('E-Mail', validators=[
            DataRequired('Please enter a E-Mail address'),
            Email('Please enter a valid E-Mail address')])
    password = PasswordField('Password', validators=[
            Optional(False),
            EqualTo('confirm_password', 'Passwords must match')])
    confirm_password = PasswordField('Repeat password')
    submit = SubmitField('Submit')

@user_blueprint.route('/admin/users')
@login_required
@groups_required('admin')
def list_users():
    users = User.query()
    return render_template('admin/listUsers.html',
        users = users
    )

@user_blueprint.route('/admin/user/<string:username>/delete', methods=['GET', 'POST'])
@login_required
@confirm(title='Delete User?',
        prompt='Are you sure you want to delete this user?',
        action='Delete',
        back='user.list_users')
@groups_required('admin')
def delete_user(username):
    user = User.get(username)
    if not user:
        flash('Invalid user name!', 'error')
        return redirect(url_for('user.list_users'))
    user.delete()
    flash('User has been deleted', 'success')
    return redirect(url_for('user.list_users'))

@user_blueprint.route('/admin/user/<string:username>/edit', methods=['GET', 'POST'])
@login_required
def edit_user(username, directCall = True):
    user = User.get(username)
    if not user:
        flash('Invalid user name!', 'error')
        if directCall:
            return redirect(url_for('user.list_users'))
        else:
            return redirect(url_for('user.home'))
    if not current_user.is_admin and user.username != current_user.username:
        abort(403)
        return ''

    form = UserEditForm()
    if form.validate_on_submit():
        if form.password.data:
            user.update(
              givenName = form.givenName.data,
              surname = form.surname.data,
              mail = form.mail.data,
              password = form.password.data
            )
        else:
            user.update(
              givenName = form.givenName.data,
              surname = form.surname.data,
              mail = form.mail.data
            )

        flash('User information changed', 'success')
        if directCall:
            return redirect(url_for('user.list_users'))
        else:
            return redirect(url_for('user.home'))

    if not form.username.data:
        form.username.data = user.username
        form.givenName.data = user.firstName
        form.surname.data = user.surname
        form.mail.data = user.mail

    return render_template('admin/editUser.html',
        form = form,
        user = user
    )
