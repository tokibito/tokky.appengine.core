# coding: utf-8
import webapp2


class WSGIApplication(webapp2.WSGIApplication):
    """WSGIアプリケーションのベースクラス
    """
    def __init__(self, routes=None, debug=False, config=None):
        super(WSGIApplication, self).__init__(routes, debug, config)
        # 404ページのハンドラ設定
        self.error_handlers[404] = 'core.defaultapps.webapp2_not_found_handler'
