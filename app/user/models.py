from flask_login import UserMixin
from flask import current_app

class User(UserMixin):
    def __init__(self, dn, username, firstName, surname):
        self.dn = dn
        self.username = username
        self.firstName = firstName
        self.surname = surname

    # FIXME: This could be simplified to just create a User object, populate it,
    @staticmethod
    def create(username, givenName, sn, password):
        """
        Create a user and save it.
        """
        from ldap3 import ObjectDef, Reader, Writer
        from ldap3.core.exceptions import LDAPNoSuchObjectResult
        from ldap3.utils.hashed import hashed

        conn = current_app.ldap3_login_manager.connection
        userbase = current_app.ldap3_login_manager.full_user_search_dn
        dn = '{user_attr}={username},{userbase}'.format(
                user_attr = current_app.config['LDAP_USER_LOGIN_ATTR'],
                username = username,
                userbase = userbase
            )

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
        user.cn = "{givenName} {sn}".format(givenName=givenName, sn=sn)
        user.userPassword = hashed(current_app.config['PASSWORD_HASHING_FUNC'], password)
        w.commit()
        return User(dn, username, givenName, sn)

    @staticmethod
    def from_ldap(username=None, dn=None):
        """
        Load a user from LDAP
        """
        user = User(dn, username, None, None)
        user.load()
        return user

    @property
    def _read_cursor(self):
        """
        return a read cursor containing just this user.
        """
        from ldap3 import ObjectDef, Reader
        from ldap3.core.exceptions import LDAPNoSuchObjectResult

        conn = current_app.ldap3_login_manager.connection

        if self.dn:
            r = Reader(conn,
                    ObjectDef(['inetOrgPerson','simpleSecurityObject'], conn),
                    current_app.ldap3_login_manager.full_user_search_dn,
                    )
            try:
                r.search_object(self.dn)
            except LDAPNoSuchObjectResult:
                raise LookupError("User does not exist: {username}".format(username=username))
                return None
        elif self.username:
            query = '{user_attr}: {username}'.format(
                user_attr = current_app.config['LDAP_USER_LOGIN_ATTR'],
                username = self.username
                )
            r = Reader(conn,
                    ObjectDef(['inetOrgPerson','simpleSecurityObject'], conn),
                    current_app.ldap3_login_manager.full_user_search_dn,
                    query
                    )
            try:
                r.search()
            except LDAPNoSuchObjectResult:
                raise LookupError("User does not exist: {username}".format(username=username))
                return None
        else:
            raise AttributeError("At least the username or the dn have to be specified")


        return r

    @property
    def _write_cursor(self):
        """
        return a write cursor containing just this user.
        """
        from ldap3 import Writer
        w = Writer.from_cursor(self._read_cursor)
        return w

    def load(self):
        """
        Load the User from the LDAP
        """
        entry = self._read_cursor[0]
        self.dn = entry.entry_dn
        self.username = getattr(entry, current_app.config['LDAP_USER_LOGIN_ATTR']),
        self.firstName = entry.givenName
        self.surname = entry.sn

    def save(self):
        """
        Save the User to LDAP
        """
        writer = self._write_cursor
        entry = writer[0]
        entry.sn = self.surname
        entry.cn = self.full_name
        entry.givenName = self.firstName
        writer.commit()

    def change_password(self, password):
        """
        Change User's password
        """
        from ldap3.utils.hashed import hashed
        writer = self._write_cursor
        entry = writer[0]
        entry.userPassword = hashed(current_app.config['PASSWORD_HASHING_FUNC'], password)
        writer.commit()

    def __repr__(self):
        return "<User: {full_name}>".format(full_name = self.full_name)

    def get_id(self):
        return self.dn

    @property
    def full_name(self):
        return "{firstName} {surname}".format(
                firstName = self.firstName,
                surname = self.surname
                )
