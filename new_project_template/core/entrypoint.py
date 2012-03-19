from google.appengine.ext.webapp import Request

from core.exceptions import Http404

import config

_url_map = []
_application = None


def _init_url_map():
    # initialize url mapping
    import re
    global _url_map
    patterns = []
    for pattern, app in config.APPS:
        patterns.append([re.compile(pattern), app])
    _url_map = patterns


def apply_middleware(app):
    from core.loader import load_module
    for middleware_name in config.MIDDLEWARE:
        middleware = load_module(middleware_name)
        app = middleware(app)
    return app


def application(environ, start_response):
    # entry point
    global _url_map
    if not _url_map:
        _init_url_map()
    request = Request(environ)
    match_app = ''
    for regexp, app in _url_map:
        match_obj = regexp.match(request.path)
        if match_obj:
            # path info hack
            path_prefix = environ['PATH_PREFIX'] = match_obj.group()
            path_info = environ['ROOT_PATH_INFO'] = environ['PATH_INFO']
            new_path_info = path_info[len(path_prefix):]
            if new_path_info.startswith('/'):
                environ['PATH_INFO'] = new_path_info
            else:
                environ['PATH_INFO'] = '/' + new_path_info
            match_app = app
            break
    else:
        # no match patterns.
        raise Http404

    # select app
    from core.loader import get_application
    real_app = get_application(match_app)
    # run app
    return real_app(environ, start_response)


def get_root_application():
    global _application
    if not _application:
        _application = apply_middleware(application)
    return _application