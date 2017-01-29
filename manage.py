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

def _getpass():
    """
    Simple getpass wrapper that asks for a password twice.
    """
    from getpass import getpass
    password = getpass('New password: ')
    if (getpass('Repeat password: ') != password):
        raise Exception("Paswords were not equal")

@manager.command
def passwd(username, password=None):
    """
    Change a user's password
    """
    from app.user.models import User
    try:
        user = User.get(username)
    except LookupError:
        app.logger.fatal("User does not exist: %d", dn)
    else:
        user.password = password or _getpass()
        user.save()
        return user

@manager.command
def create_user(uid, givenName, sn, mail=None, password=None):
    """
    Create a user
    """
    from app.user.models import User
    return User.create(uid, givenName, sn, password or _getpass(), mail)

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
