from flask import render_template_string, url_for, \
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
    template = """
    <h1>Welcome: {{ current_user.data.cn }}</h1>
    <h2>{{ current_user.dn }}</h2>
    """

    return render_template_string(template)

@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    template = """
    <div id="flash">{{ get_flashed_messages() }}</div>
    {{ form.errors }}
    <form method="POST">
        <label>Username{{ form.username() }}</label>
        <label>Password{{ form.password() }}</label>
        {{ form.submit() }}
        {{ form.hidden_tag() }}
    </form>
    """

    # Instantiate a LDAPLoginForm which has a validator to check if the user
    # exists in LDAP.
    form = LDAPLoginForm()

    if form.validate_on_submit():
        # Successfully logged in, We can now access the saved user object
        # via form.user.
        current_app.logger.debug(current_app.ldap3_login_manager.authenticate("foo", "bar").status)
        current_app.logger.debug(form.user)
        login_user(form.user)  # Tell flask-login to log them in.
        return redirect('/')  # Send them home

    return render_template_string(template, form=form)

@user_blueprint.route("/logout")
@login_required
def logout():
        logout_user()
        return redirect(url_for("user.home"))
