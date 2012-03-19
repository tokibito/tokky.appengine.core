# coding: utf-8
import logging
import webapp2

import config

from core import wsgi as core_wsgi


#class MyAppHandler(webapp2.RequestHandler):
#    """MyAppハンドラ
#    """
#    def get(self):
#        self.response.headers['Content-Type'] = 'text/plain'
#        self.response.out.write('OK')


def application_factory():
    application = core_wsgi.WSGIApplication([
        #(r'.*', MyAppHandler),
    ], debug=config.DEBUG)
    return application
