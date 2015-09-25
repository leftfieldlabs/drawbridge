from google.appengine.ext import ndb


class SiteConfig(ndb.Model):

    wild_card_domains = ndb.StringProperty(repeated=True)

    @classmethod
    def get_or_create(cls):
        config = cls.query().get()
        if config is None:
            config = cls()
            config.put()
        return config


class AuthorizedUser(ndb.Model):
    email = ndb.StringProperty(required=True, indexed=True)

    DENIED = 0
    APPROVED = 2

    STATUS_CHOICES = [DENIED, APPROVED]

    status = ndb.IntegerProperty(choices=STATUS_CHOICES, default=APPROVED)

    @classmethod
    def create(cls, email):
        user = cls.query(cls.email == email.lower()).get()
        if user:
            return user
        else:
            new_user = cls(email=email.lower())
            key = new_user.put()
            # Refresh
            return key.get()


    @classmethod
    def all(cls):
        return cls.query().fetch(1000)

    @classmethod
    def is_user_allowed(cls, user):
        auth_user = cls.query(cls.email == user.email(), cls.status == cls.APPROVED).get()
        return auth_user is not None
