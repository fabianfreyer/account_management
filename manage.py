#!/usr/bin/env python3
from flask_script import Manager
from app import create_app, check_sanity

app = create_app()
manager = Manager(app)

@manager.command
def sanity():
    """
    Run a number of sanity checks and attempt to automatically
    fix any inconsistencies.
    """
    check_sanity()

@manager.command
def passwd(username, password=None):
    """
    Change a user's password
    """
    from app.user.models import User
    from getpass import getpass

    try:
        user = User.from_ldap(username)
    except LookupError:
        app.logger.fatal("User does not exist: %d", dn)
    else:
        if password is None:
            password = getpass('New password: ')
            if (getpass('Repeat password: ') != password):
                raise Exception("Paswords were not equal")

        user.change_password(password)
        return user

@manager.command
def create_user(uid, givenName, sn, password=None):
    """
    Create a user
    """
    from app.user.models import User
    from getpass import getpass

    if password is None:
        password = getpass('New password: ')
        if (getpass('Repeat password: ') != password):
            raise Exception("Paswords were not equal")

    return User.create(uid, givenName, sn, password)

if __name__ == "__main__":
    if app.config['MOCKSERVER'] == True:
        from unittest import mock
        from flask_ldap3_login import LDAP3LoginManager
        from test.MockLDAP import _mock_connection
        with mock.patch.object(LDAP3LoginManager, '_make_connection', new=_mock_connection):
            app.logger.info("using mocked ldap")
            manager.run()
    else:
        manager.run()
