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
def create_user(uid, givenName, sn, password=None):
    """
    Create a user
    """
    from ldap3 import ObjectDef, Reader, Writer
    from ldap3.core.exceptions import LDAPNoSuchObjectResult
    from ldap3.utils.hashed import hashed
    from getpass import getpass

    conn = app.ldap3_login_manager.connection
    userbase = "%s,%s"%(app.config['LDAP_USER_DN'], app.config['LDAP_BASE_DN'])
    dn = "uid=%s,%s" %(uid,userbase)

    if password is None:
        password = getpass('New password: ')
        if (getpass('Repeat password: ') != password):
            raise Exception("Paswords were not equal")

    obj_account = ObjectDef(['inetOrgPerson','simpleSecurityObject'], conn)
    r = Reader(conn, obj_account, userbase)
    try:
        r.search()
    except LDAPNoSuchObjectResult:
        pass

    w = Writer.from_cursor(r)
    user = w.new(dn)
    user.sn = sn
    user.givenName = givenName
    user.cn = "%s %s" % ( givenName, sn )
    user.userPassword = hashed(app.config['PASSWORD_HASHING_FUNC'], password)
    w.commit()

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
