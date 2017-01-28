from flask import render_template, url_for, \
            redirect, flash, request, current_app
from flask_ldap3_login.forms import LDAPLoginForm
from .models import User
from flask_login import login_user, current_user, login_required, logout_user

from . import user_blueprint

@user_blueprint.route('/')
def home():
    # Redirect users who are not logged in.
    if not current_user or current_user.is_anonymous:
        return redirect(url_for('user.login'))

    # User is logged in, so show them a page with their cn and dn.

    return render_template("index.html")

@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    # Instantiate a LDAPLoginForm which has a validator to check if the user
    # exists in LDAP.
    form = LDAPLoginForm()

    if form.validate_on_submit():
        # Successfully logged in, We can now access the saved user object
        # via form.user.
        current_app.logger.debug(
                "Logged in user: {user.username} ({user.full_name})".format(
                    user = form.user))
        login_user(form.user)  # Tell flask-login to log them in.
        return redirect('/')  # Send them home

    return render_template('login.html', form=form)

@user_blueprint.route("/logout")
@login_required
def logout():
        logout_user()
        return redirect(url_for("user.home"))
