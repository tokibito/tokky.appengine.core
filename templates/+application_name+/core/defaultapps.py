def not_found(environ, start_response):
    start_response('404 Not Found', [('Content-Type', 'text/plain')])
    return '404 Not Found.'