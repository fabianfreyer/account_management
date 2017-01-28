"""
Sanity checks for the environment of this app.
All functions starting with check_ are executed automatically.
"""
from flask import current_app
from ldap3 import ObjectDef, Reader, Writer
from ldap3.core.exceptions import LDAPNoSuchObjectResult

def check_userbase_exists(fix=True):
    """
    Check the User base DN exists, and if not, create it.
    """
    conn = current_app.ldap3_login_manager.connection
    ou = ObjectDef('organizationalunit', conn)
    r = Reader(conn, ou, current_app.config['LDAP_BASE_DN'])
    userbase = "%s,%s"%(current_app.config['LDAP_USER_DN'],
            current_app.config['LDAP_BASE_DN'])
    try:
        base = r.search_object(userbase)
    except LDAPNoSuchObjectResult:
        current_app.logger.error("User base DN does not exist: %s" % userbase)
        if fix:
            current_app.logger.info("Attempting to fix...")
            w = Writer.from_cursor(r)
            base = w.new(userbase)
            base.description = "Automagically added by quasisentient sanity checks"
            w.commit()

def check_oauthbase_exists(fix=True):
    """
    Check the oauth2 base DN exists, and if not, create it
    """
    conn = current_app.ldap3_login_manager.connection
    ou = ObjectDef('organizationalunit', conn)
    r = Reader(conn, ou, current_app.config['LDAP_OAUTH2_CLIENT_DN'])
    userbase = "%s,%s"%(current_app.config['LDAP_OAUTH2_CLIENT_DN'],
            current_app.config['LDAP_BASE_DN'])
    try:
        base = r.search_object(userbase)
    except LDAPNoSuchObjectResult:
        current_app.logger.error("Oauth2 client DN does not exist: %s" % userbase)
        if fix:
            current_app.logger.info("Attempting to fix...")
            w = Writer.from_cursor(r)
            base = w.new(userbase)
            base.description = "Automagically added by quasisentient sanity checks"
            w.commit()

def check_hashfunc(fix=True):
    from ldap3 import HASHED_NONE, HASHED_MD5, HASHED_SALTED_MD5, HASHED_SALTED_SHA, HASHED_SALTED_SHA256, \
                HASHED_SALTED_SHA384, HASHED_SALTED_SHA512, HASHED_SHA, HASHED_SHA256, HASHED_SHA384, HASHED_SHA512

    allowed_hashes = [
            HASHED_NONE, HASHED_MD5, HASHED_SALTED_MD5, HASHED_SALTED_SHA, HASHED_SALTED_SHA256,
            HASHED_SALTED_SHA384, HASHED_SALTED_SHA512, HASHED_SHA, HASHED_SHA256, HASHED_SHA384, HASHED_SHA512
            ]
    insecure_hashes = [HASHED_NONE, HASHED_MD5, HASHED_SALTED_MD5, HASHED_SALTED_SHA, HASHED_SHA]
    salted_hashes = [HASHED_SALTED_MD5, HASHED_SALTED_SHA, HASHED_SALTED_SHA256, HASHED_SALTED_SHA384, HASHED_SALTED_SHA512]

    hashfunc = current_app.config['PASSWORD_HASHING_FUNC']

    if hashfunc not in allowed_hashes:
        current_app.logger.error("Invalid hashing function selected.")
        if (fix):
            current_app.logger.warn("Invalid hashing function selected.")
            current_app.config['PASSWORD_HASHING_FUNC'] = HASHED_SALTED_SHA385
    elif hashfunc in insecure_hashes:
        current_app.logger.warn('Yo dawg, I heard you like insecure hashes.')
    if hashfunc not in salted_hashes:
        current_app.logger.warn('Would you like some salt with your users\' passwords?')


