import re

from google.appengine.ext import webapp

from core.generics import TemplatePageHandler

import config

class TopPageHandler(TemplatePageHandler):
    template_name = 'templates/index.html'

application = webapp.WSGIApplication([
    (r'/', TopPageHandler),
    ], debug=config.DEBUG)