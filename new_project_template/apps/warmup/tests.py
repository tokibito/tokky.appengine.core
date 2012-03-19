# coding: utf-8
import json

import unittests

from apps.warmup import handlers as warmup_handlers


class WarmupHandlerTest(unittests.HandlerTestCase):
    """WarmupHandlerのテスト
    """
    handler_class = warmup_handlers.WarmupHandler

    def test_ok(self):
        self.handler.get()
        self.assertEqual(self.handler.response.getvalue(), 'OK')
