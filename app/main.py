import webapp2
import handlers


_AUTH_ROUTES = [
    webapp2.Route(r'/<:.*>', handlers.MainHandler),
]

_API_ROUTES = [
    webapp2.Route(r'/api/records/<release_name>', handlers.APIRecordHandler),
    webapp2.Route(r'/api/records/<release_name>/', handlers.APIRecordHandler),
]


_ADMIN_ROUTES = [
    webapp2.Route('/admin', handlers.AdminHandler, 'admin-index'),
    webapp2.Route('/admin/', handlers.AdminHandler, 'admin-index'),

    webapp2.Route('/admin/success', handlers.SuccessHandler, 'admin-success'),
    webapp2.Route('/admin/success/', handlers.SuccessHandler, 'admin-success'),

    webapp2.Route('/admin/<key>/delete', handlers.DeleteKeyHandler, 'admin-delete-user'),
    webapp2.Route('/admin/<key>/delete/', handlers.DeleteKeyHandler, 'admin-delete-user'),
    webapp2.Route('/admin/<key>/toggle-admin-status', handlers.ToggleAdminStatusHandler, 'adming-toggle-admin-status'),
    webapp2.Route('/admin/<key>/toggle-admin-status/', handlers.ToggleAdminStatusHandler, 'adming-toggle-admin-status'),

    webapp2.Route('/admin/wild-card/<wild_card>/delete', handlers.DeleteWildCardHandler, 'admin-delete-wild-card'),
    webapp2.Route('/admin/wild-card/<wild_card>/delete/', handlers.DeleteWildCardHandler, 'admin-delete-wild-card'),

    webapp2.Route('/admin/<:.*>', handlers.AdminAssetHandler, 'admin-asset'),
]

app = webapp2.WSGIApplication(
    routes=(
        _API_ROUTES + _ADMIN_ROUTES + _AUTH_ROUTES
    ),
debug=True)
