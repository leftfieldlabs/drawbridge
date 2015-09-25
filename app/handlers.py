import webapp2
from google.appengine.api import memcache
from google.appengine.api import users
from google.appengine.ext.webapp import template
import functools
import logging
import models
import cgi
import os

def requires_auth(f):
    """A decorator that requires a currently logged in user."""

    @functools.wraps(f)
    def wrapper(self, *args, **kwargs):
        user = users.get_current_user()
        if not user:
            return self.deny_access()

        user_email = user.email()
        site_config = models.SiteConfig.get_or_create()
        is_wild_card_allowed = user_email.split('@')[1] in site_config.wild_card_domains

        if is_wild_card_allowed or models.AuthorizedUser.is_user_allowed(user):
            return f(self, *args, **kwargs)
        else:
            return self.deny_access()

    return wrapper


def requires_admin(f):
    """A decorator that requires a currently logged in administrator."""

    @functools.wraps(f)
    def wrapper(self, *args, **kwargs):
        if not users.is_current_user_admin():
            self.deny_access()
        else:
            return f(self, *args, **kwargs)

    return wrapper


class BaseHandler(webapp2.RequestHandler):

    def error(self, status=500):
        path = os.path.join(os.path.dirname(__file__), 'templates/error.html')
        self.response.status_int = status
        self.response.out.write(template.render(path, {}))

    def deny_access(self):
        path = os.path.join(os.path.dirname(__file__), 'templates/access-denied.html')
        self.response.status_int = 403
        self.response.out.write(template.render(path, {}))

class AdminHandler(BaseHandler):

    @requires_admin
    def post(self):
        # TODO: XSRF protection
        email = cgi.escape(self.request.get('email'))
        if email is None or email == '':
            return self.error()

        # Add user
        new_user = models.AuthorizedUser.create(email)

        return webapp2.redirect_to('admin-index')



    @requires_admin
    def get(self):

        users = models.AuthorizedUser.all()

        data = {
            'users': users
        }

        path = os.path.join(os.path.dirname(__file__), 'templates/admin.html')
        self.response.out.write(template.render(path, data))


class MainHandler(BaseHandler):

    @requires_auth
    def get(self, *args, **kwargs):

        tpl = self.request.uri
        newtpl = 'templates/' +tpl.replace(self.request.host_url+'/', '')

        extension = os.path.splitext(newtpl)[1]
        file_path = os.path.join(os.path.dirname(__file__), newtpl)

        with open (file_path, "r") as myfile:
            data = myfile.read()
            if extension == '.js':
                self.response.headers["Content-Type"] = "text/javascript"
            if extension == '.css':
                self.response.headers["Content-Type"] = "text/css"
            if extension == '.png':
                self.response.headers["Content-Type"] = "image/png"
            if extension == '.jpg':
                self.response.headers["Content-Type"] = "image/jpeg"

        self.response.out.write(data)
