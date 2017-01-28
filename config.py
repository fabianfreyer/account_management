import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    FLASK_COVERAGE = 0
    MOCKSERVER = False
    LDAP_HOST = 'localhost'
    LDAP_PORT = 8369
    LDAP_BASE_DN = 'dc=my-domain,dc=com'
    LDAP_USER_DN = 'ou=users'
    LDAP_GROUP_DN = 'ou=groups'
    LDAP_BIND_USER_DN = 'uid=bind,dc=my-domain,dc=com'
    LDAP_BIND_USER_PASSWORD = 'bind123'
    LDAP_USER_RDN_ATTR = 'uid'
    LDAP_USER_LOGIN_ATTR = 'uid'
    LDAP_READONLY = False

    import ldap3
    PASSWORD_HASHING_FUNC = ldap3.HASHED_SALTED_SHA384

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    SECRET_KEY = 'secrets'
    DEBUG=True
    #MOCKSERVER = True

class ProductionConfig(Config):
    LOGPATH='logs'

class TestingConfig(Config):
    DEBUG=True
    TESTING=True
    MOCKSERVER=True
    FLASK_COVERAGE = 1
    SECRET_KEY = 'secrets'
    WTF_CSRF_ENABLED = False


config = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'testing': TestingConfig,
        'default': DevelopmentConfig
        }

