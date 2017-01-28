class Grant(object):
    user_id =  None
    client_id =  None
    code = None
    redirect_uri = None
    expires = None
    _scopes = []

    def delete(self):
        return self

    @property
    def scopes(self):
        return _scopes

class Token(object):
    client_id = None
    user_id = None
    token_type = "bearer"
    access_token = None
    refresh_token = None
    expires = None
    _scopes = []

    def delete(self):
        return self

    @property
    def scopes(self):
        return _scopes

class Client(object):
    # human readable name, not required
    name = None

    # human readable description, not required
    description = None

    client_id = None
    client_secret = None

    # public or confidential
    is_confidential = False

    _redirect_uris = []
    _default_scopes = []

    @staticmethod
    def from_id(clientid):
        from flask import current_app
        from ldap3 import ObjectDef, Reader
        conn = current_app.ldap3_login_manager.connection
        obj = ObjectDef(['oauthClientMetadata'], conn)
        r = Reader

    @property
    def client_type(self):
        if self.is_confidential:
            return 'confidential'
        return 'public'

    @property
    def redirect_uris(self):
        if self._redirect_uris:
            return self._redirect_uris
        return []

    @property
    def default_redirect_uri(self):
        return self.redirect_uris[0]

    @property
    def default_scopes(self):
        if self._default_scopes:
            return self._default_scopes
        return []

