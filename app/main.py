import webapp2
import handlers


_AUTH_ROUTES = [
    #webapp2.Route('/', handlers.IndexHandler),
    webapp2.Route(r'/<:.*>', handlers.MainHandler),
]

_ADMIN_ROUTES = [
    webapp2.Route('/admin', handlers.AdminHandler, 'admin-index'),
    webapp2.Route('/admin/', handlers.AdminHandler, 'admin-index'),

    webapp2.Route('/admin/success', handlers.SuccessHandler, 'admin-success'),
    webapp2.Route('/admin/success/', handlers.SuccessHandler, 'admin-success'),

    webapp2.Route('/admin/<key>/delete', handlers.DeleteKeyHandler, 'admin-delete-user'),
    webapp2.Route('/admin/<key>/delete/', handlers.DeleteKeyHandler, 'admin-delete-user'),

    webapp2.Route('/admin/wild-card/<wild_card>/delete', handlers.DeleteWildCardHandler, 'admin-delete-wild-card'),
    webapp2.Route('/admin/wild-card/<wild_card>/delete/', handlers.DeleteWildCardHandler, 'admin-delete-wild-card'),
]

app = webapp2.WSGIApplication(
    routes=(
        _ADMIN_ROUTES + _AUTH_ROUTES
    ),
debug=True)
