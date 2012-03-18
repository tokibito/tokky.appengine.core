from google.appengine.ext import webapp


class TemplatePageHandler(webapp.RequestHandler):
    template_name = ''

    def get(self, *args, **kwargs):
        result = self.render(*args, **kwargs)
        self.response.out.write(result)

    def head(self, *args, **kwargs):
        self.get(*args, **kwargs)

    def pre_render(self, *args, **kwargs):
        pass

    def get_context(self, *args, **kwargs):
        return {}

    def get_pathprefix(self):
        return self.request.environ.get('PATH_PREFIX') or ''

    def get_template_name(self):
        return self.template_name

    def render(self, *args, **kwargs):
        import config
        from google.appengine.ext.webapp import template
        self.pre_render(*args, **kwargs)
        context = {
            'path_prefix': self.get_pathprefix(),
            'MEDIA_URL': config.MEDIA_URL,
        }
        context.update(self.get_context(*args, **kwargs))
        template_name = self.get_template_name()
        if config.DEBUG:
            self.response.template_name = template_name
            self.response.template_context = context
        return template.render(template_name, context)

    def handle_exception(self, exception, debug_mode):
        from core.exceptions import Http404
        if isinstance(exception, Http404):
            raise
        super(TemplatePageHandler, self).handle_exception(exception, debug_mode)
