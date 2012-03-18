import config

from core.exceptions import Http404


def not_found_middleware(app):
    def _inner(environ, start_response):
        try:
            return app(environ, start_response)
        except Http404, e:
            from core.loader import get_application
            not_found_app = get_application(config.NOT_FOUND_APP)
            return not_found_app(environ, start_response)
    _inner.__func__ = app
    return _inner
