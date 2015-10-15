import webapp2
from google.appengine.api import memcache
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext.webapp import template
import functools
import security
import logging
import models
import cgi
import os

def requires_xsrf_token(f):
    """Decorator to validate XSRF tokens for any verb but GET, HEAD, OPTIONS."""

    @functools.wraps(f)
    def wrapper(self, *args, **kwargs):
        non_xsrf_protected_verbs = ['options', 'head', 'get']
        if (self.request.method.lower() in non_xsrf_protected_verbs or
                self.has_valid_xsrf_token()):
            return f(self, *args, **kwargs)
        else:
            return self.xsrf_fail()

    return wrapper

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

    def __init__(self, request, response):
        self.initialize(request, response)

        user = users.get_current_user()

        if user:
            key = models.SiteConfig.get_cached_xsrf_key()
            self._xsrf_token = security.generate_token(key, user.email())
            #if self.app.config.get('using_angular', constants.DEFAULT_ANGULAR):
                # AngularJS requires a JS readable XSRF-TOKEN cookie and will pass this
                # back in AJAX requests.
                #self.response.set_cookie('XSRF-TOKEN', self._xsrf_token, httponly=False)

        else:
            self._xsrf_token = None

        self.data = {
            'xsrf': self._xsrf_token,
            'is_admin': users.is_current_user_admin() is True,
            'nickname': user.nickname()
        }

    def success(self, status=200, message="Success!"):
        path = os.path.join(os.path.dirname(__file__), 'templates/success.html')
        self.response.status_int = status
        self.response.out.write(template.render(path, {'message': message}))

    def error(self, status=500, message="Unknown error occurred"):
        path = os.path.join(os.path.dirname(__file__), 'templates/error.html')
        self.response.status_int = status
        self.response.out.write(template.render(path, {'message': message}))

    def xsrf_fail(self):
        return self.error(status=500, message="Invalid XSRF token")

    def has_valid_xsrf_token(self):
        token = self.request.get('xsrf') or self.request.headers.get('X-XSRF-TOKEN')

        # By default, Angular's $http service will add quotes around the
        # X-XSRF-TOKEN.
        # if (token and
        #         self.app.config.get('using_angular', constants.DEFAULT_ANGULAR) and
        #             token[0] == '"' and token[-1] == '"'):
        #     token = token[1:-1]

        current_user = users.get_current_user()
        xsrf_key = models.SiteConfig.get_cached_xsrf_key()
        if security.validate_token(xsrf_key, current_user.email(), token):
            return True
        return False

    def deny_access(self, redirect_uri='/'):
        path = os.path.join(os.path.dirname(__file__), 'templates/access-denied.html')
        self.response.status_int = 403

        user = users.get_current_user()
        self.data['logout_url'] = users.create_logout_url(redirect_uri)
        self.response.out.write(template.render(path, self.data))


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

class SuccessHandler(BaseHandler):

    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'templates/success.html')
        self.response.out.write(template.render(path, self.data))

class DeleteWildCardHandler(BaseHandler):

    @requires_admin
    @requires_xsrf_token
    def post(self, wild_card):

        site_config = models.SiteConfig.get_or_create()
        site_config.wild_card_domains.remove(wild_card)
        site_config.put()

        return self.success(message="Successfully deleted item")

class DeleteKeyHandler(BaseHandler):

    @requires_admin
    @requires_xsrf_token
    def post(self, key):

        k = ndb.Key(urlsafe=key)
        obj = k.get()
        if obj is None:
            #TODO HANDLE error
            return self.error()

        k.delete()
        return self.success(message="Successfully deleted item")


class AdminHandler(BaseHandler):

    @requires_admin
    @requires_xsrf_token
    def post(self):

        email = cgi.escape(self.request.get('email'))

        if email is None or email == '':
            return self.error(message="Valid email not provided")

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


        self.data['users'] = auth_users
        self.data['wild_card_domains'] = models.SiteConfig.get_or_create().wild_card_domains
        self.data['logout_url'] = users.create_logout_url('/admin')

        path = os.path.join(os.path.dirname(__file__), 'templates/admin/admin.html')
        self.response.out.write(template.render(path, self.data))


class MainHandler(BaseHandler):

    @requires_auth
    def get(self, *args, **kwargs):

        tpl = self.request.uri
        newtpl = 'templates/project' +tpl.replace(self.request.host_url+'/', '')

        if any(x in newtpl for x in ['js/', 'css/', 'img/', 'images/', 'scripts/']):
            pass
        else:
            if '.html' not in newtpl:
                newtpl += '/index.html'

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
