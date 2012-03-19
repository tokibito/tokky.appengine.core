# coding: utf-8
import json

import unittests

from apps.new_application_template import handlers as myapp_handlers


class MyAppHandlerTest(unittests.HandlerTestCase):
    """MyAppHandlerのテスト
    """
    handler_class = myapp_handlers.MyAppHandler

    def test_ok(self):
        self.handler.get()
        self.assertEqual(self.handler.response.getvalue(), 'OK')
