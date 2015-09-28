from google.appengine.ext import ndb
from google.appengine.api import memcache
import os

class SiteConfig(ndb.Model):

    xsrf_key = ndb.BlobProperty()
    wild_card_domains = ndb.StringProperty(repeated=True)

    @classmethod
    def ancestor(cls):
        return ndb.Key('SiteConfig', 'master_parent')

    @classmethod
    def get_cached_xsrf_key(cls):
        xsrf_key = memcache.get('xsrf_key')
        if not xsrf_key:
            xsrf_key = cls.get_or_create().xsrf_key
            memcache.set('xsrf_key', xsrf_key)
        return xsrf_key


    @classmethod
    @ndb.transactional
    def get_or_create(cls):
        config = cls.query(ancestor=cls.ancestor()).get()
        if config is None:
            config = cls(parent=cls.ancestor())
            config.xsrf_key = os.urandom(16)
            config.put()
        return config


class AuthorizedUser(ndb.Model):
    email = ndb.StringProperty(required=True, indexed=True)

    @classmethod
    def ancestor(cls):
        return ndb.Key('AuthorizedUser', 'master_parent')

    DENIED = 0
    APPROVED = 2

    STATUS_CHOICES = [DENIED, APPROVED]

    status = ndb.IntegerProperty(choices=STATUS_CHOICES, default=APPROVED)

    @classmethod
    @ndb.transactional
    def create(cls, email):
        user = cls.query(cls.email == email.lower(), ancestor=cls.ancestor()).get()
        if user:
            return user
        else:
            new_user = cls(parent=cls.ancestor(), email=email.lower())
            key = new_user.put()
            # Refresh
            return key.get()


    @classmethod
    def all(cls):
        return cls.query(ancestor=cls.ancestor()).fetch(1000)

    @classmethod
    def is_user_allowed(cls, user):
        auth_user = cls.query(cls.email == user.email(), cls.status == cls.APPROVED, ancestor=cls.ancestor()).get()
        return auth_user is not None
