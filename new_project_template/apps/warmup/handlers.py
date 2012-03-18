# coding: utf-8
import logging
import webapp2

import config

from core import wsgi as core_wsgi


class WarmupHandler(webapp2.RequestHandler):
    """warmup用のハンドラ
    """
    def get(self):
        # warmupで必要な操作はここに記述します

        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('OK')


application = core_wsgi.WSGIApplication([
        (r'.*', WarmupHandler),
        ], debug=config.DEBUG)
