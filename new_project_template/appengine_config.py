import config

#webapp_django_version = '1.2'

if config.ENABLE_APPSTATS:
    def webapp_add_wsgi_middleware(app):
        from google.appengine.ext.appstats import recording
        app = recording.appstats_wsgi_middleware(app)
        return app