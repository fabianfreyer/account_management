from flask_login import UserMixin
from flask import current_app

from app.orm import LDAPOrm

class User(UserMixin, LDAPOrm):
    # This doesn't really work either, so we have to overload _basedn
    # basedn_config_var = 'LDAP_OAUTH2_CLIENT_DN'
    @classmethod
    def _basedn(cls):
        return current_app.ldap3_login_manager.full_user_search_dn

    objectClasses = ['inetOrgPerson','simpleSecurityObject']
    # FIXME: 'uid' should really be current_app.config['LDAP_USER_LOGIN_ATTR']
    # here. Unfortunately, current_app doesn't really work here, so the ORM
    # has to be adapted to deal with this.
    keyMapping = ('uid', 'username')

    def __init__(self, username=None, dn=None, firstName=None, surname=None, mail=None):
        self.dn = dn
        self.username = username
        self.firstName = firstName
        self.surname = surname
        self._full_name = None
        self._password = None
        self.mail = mail

    # FIXME: This could be simplified to just create a User object, populate it,
    @staticmethod
    def create(username, givenName, surname, password, mail = None):
        """
        Create a user and save it.
        """
        user = User(username = username, firstName = givenName, surname = surname, mail = mail)
        user.password = password
        user.save()
        return user

    @property
    def password(self):
        """
        Return if the password has been changed
        """
        if self._password:
            return True
        return False

    @password.setter
    def password(self, value):
        """
        Set the password
        """
        from ldap3.utils.hashed import hashed
        self._password = hashed(current_app.config['PASSWORD_HASHING_FUNC'], value)

    def _orm_mapping_load(self, entry):
        # FIXME: It would be nice if the ORM could somehow automagically
        # build up this mapping.
        self.dn = entry.entry_dn
        (self.username,) = getattr(entry, current_app.config['LDAP_USER_LOGIN_ATTR'])[0],
        current_app.logger.debug(self.username)
        self.firstName = entry.givenName.value
        self.surname = entry.sn.value
        self._full_name = entry.cn.value
        self.mail = entry.mail.value

    def _orm_mapping_save(self, entry):
        # FIXME: It would be nice if the ORM could somehow automagically
        # build up this mapping.
        entry.sn = self.surname
        entry.cn = self.full_name
        entry.givenName = self.firstName
        if self.password:
            entry.userPassword = self._password
        if self.mail:
            entry.mail = self.mail

    def __repr__(self):
        return "<User: {full_name}>".format(full_name = self.full_name)

    def get_id(self):
        return self.username

    @property
    def full_name(self):
        return self._full_name or "{firstName} {surname}".format(
                firstName = self.firstName,
                surname = self.surname
                )
