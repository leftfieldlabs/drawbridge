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
            return self.redirect(users.create_login_url(self.request.uri))

        user_email = user.email()
        site_config = models.SiteConfig.get_or_create()
        is_wild_card_allowed = user_email.split('@')[1] in site_config.wild_card_domains

        if is_wild_card_allowed or models.AuthorizedUser.is_user_allowed(user) or users.is_current_user_admin():
            return f(self, *args, **kwargs)
        else:
            return self.deny_access()

    return wrapper


def requires_admin(f):
    """A decorator that requires a currently logged in administrator."""

    @functools.wraps(f)
    def wrapper(self, *args, **kwargs):
        if not users.is_current_user_admin():
            self.deny_access(redirect_uri='/admin')
        else:
            return f(self, *args, **kwargs)

    return wrapper


class BaseHandler(webapp2.RequestHandler):

    def error(self, status=500):
        path = os.path.join(os.path.dirname(__file__), 'templates/error.html')
        self.response.status_int = status
        self.response.out.write(template.render(path, {}))

    def deny_access(self, redirect_uri='/'):
        path = os.path.join(os.path.dirname(__file__), 'templates/access-denied.html')
        self.response.status_int = 403

        user = users.get_current_user()

        data = {
            'nickname': user.nickname(),
            'logout_url': users.create_logout_url(redirect_uri)
        }

        self.response.out.write(template.render(path, data))


class IndexHandler(BaseHandler):

    @requires_auth
    def get(self):

        user = users.get_current_user()

        # What pages are available?
        path = os.path.join(os.path.dirname(__file__), 'templates/project')
        project_pages = [f for f in os.listdir(path) if f not in ['.DS_Store', 'README.md']]

        data = {
            'pages': project_pages,
            'nickname': user.nickname(),
            'logout_url': users.create_logout_url('/')
        }
        path = os.path.join(os.path.dirname(__file__), 'templates/index.html')
        self.response.out.write(template.render(path, data))


class AdminHandler(BaseHandler):

    @requires_admin
    def post(self):
        # TODO: XSRF protection
        email = cgi.escape(self.request.get('email'))

        if email is None or email == '':
            return self.error()

        # Check for wild card
        if '*' in email:
            wild_card = email.replace('*', '')
            site_config = models.SiteConfig.get_or_create()
            if wild_card not in site_config.wild_card_domains:
                site_config.wild_card_domains.append(wild_card)
                site_config.put()
        else:
            # Add user
            new_user = models.AuthorizedUser.create(email)

        return webapp2.redirect_to('admin-index')



    @requires_admin
    def get(self):

        user = users.get_current_user()
        auth_users = models.AuthorizedUser.all()

        data = {
            'nickname': user.nickname(),
            'logout_url': users.create_logout_url('/admin'),
            'users': auth_users,
            'wild_card_domains': models.SiteConfig.get_or_create().wild_card_domains
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

        try:
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
        except IOError:
            webapp2.abort(404)

        self.response.out.write(data)
