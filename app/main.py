import webapp2
import handlers


_AUTH_ROUTES = [
    webapp2.Route('/', handlers.MainHandler),
]

_ADMIN_ROUTES = [
    webapp2.Route('/admin', handlers.AdminHandler),
    webapp2.Route('/admin/', handlers.AdminHandler),
]

#################################
# DO NOT MODIFY BELOW THIS LINE #
#################################

app = webapp2.WSGIApplication(
    routes=(
        _AUTH_ROUTES + _ADMIN_ROUTES
    ),
debug=True)
