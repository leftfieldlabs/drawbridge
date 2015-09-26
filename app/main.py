import webapp2
import handlers


_AUTH_ROUTES = [
    webapp2.Route('/', handlers.IndexHandler),
    webapp2.Route(r'/<:.*>', handlers.MainHandler),
]

_ADMIN_ROUTES = [
    webapp2.Route('/admin', handlers.AdminHandler, 'admin-index'),
    webapp2.Route('/admin/', handlers.AdminHandler, 'admin-index'),
]

app = webapp2.WSGIApplication(
    routes=(
        _ADMIN_ROUTES + _AUTH_ROUTES
    ),
debug=True)
