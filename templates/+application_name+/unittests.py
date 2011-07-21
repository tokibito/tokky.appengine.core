#!/usr/bin/env python
import os
import sys
from StringIO import StringIO

try:
    import unittest2 as unittest
except ImportError:
    if (sys.version_info.major, sys.version_info.minor) >= (2, 7):
        import unittest
    else:
        sys.stdout.write('Please install unittest2.'\
            '(eg easy_install unittest2)\n')
        sys.exit()


class TestBedTestCase(unittest.TestCase):
    def _setup_testbed(self):
        from google.appengine.ext import testbed
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

    def _teardown_testbed(self):
        self.testbed.deactivate()

    def setUp(self):
        self._setup_testbed()

    def tearDown(self):
        self._teardown_testbed()


class DummyResponse(object):
    def getvalue(self):
        return self.out.getvalue()

    def reset(self):
        self.out = StringIO()


def create_test_handler(handler_class):
    instance = handler_class()
    instance.request = {}
    instance.response = DummyResponse()
    instance.response.reset()
    return instance


class HandlerTestCase(TestBedTestCase):
    def _setup_handler(self):
        self.handler = create_test_handler(self.__class__.handler_class)

    def setUp(self):
        super(HandlerTestCase, self).setUp()
        self._setup_handler()


def search_sdk_path():
    raw_paths = os.environ['PATH']
    if sys.platform == 'win32':
        sep = ';'
    else:
        sep = ':'
    for path in raw_paths.split(sep):
        dev_script_path = os.path.join(path, 'dev_appserver.py')
        if os.path.exists(dev_script_path):
            return path
    raise Exception("SDK Path is not found.")


def main():
    sys.path.insert(0, search_sdk_path())
    import dev_appserver
    dev_appserver.fix_sys_path()
    suite = unittest.loader.TestLoader().discover(
        os.path.dirname(os.path.abspath(__file__)))
    unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == '__main__':
    main()