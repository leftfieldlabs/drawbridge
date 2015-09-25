import webapp2
from google.appengine.api import memcache
from google.appengine.api import users
from google.appengine.ext.webapp import template
import functools
import os

def requires_auth(f):
    """A decorator that requires a currently logged in user."""

    @functools.wraps(f)
    def wrapper(self, *args, **kwargs):
        if not users.get_current_user():
            self.DenyAccess()
        else:
            return f(self, *args, **kwargs)

    return wrapper


def requires_admin(f):
    """A decorator that requires a currently logged in administrator."""

    @functools.wraps(f)
    def wrapper(self, *args, **kwargs):
        if not users.is_current_user_admin():
            self.DenyAccess()
        else:
            return f(self, *args, **kwargs)

    return wrapper



class AdminHandler(webapp2.RequestHandler):

    @requires_admin
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'templates/admin.html')
        self.response.out.write(template.render(path, {}))


class MainHandler(webapp2.RequestHandler):

    @requires_auth
    def get(self):
        pass


class StaticHandler(webapp2.RequestHandler):
    pass
