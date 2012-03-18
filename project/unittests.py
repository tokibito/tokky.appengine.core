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
        self.testbed.init_taskqueue_stub()

    def _teardown_testbed(self):
        self.testbed.deactivate()

    def setUp(self):
        self._setup_testbed()

    def tearDown(self):
        self._teardown_testbed()


class DummyRequest(dict):
    def get_params(self):
        return self

    params = property(get_params)

    def get_uri(self):
        if 'uri' in self:
            return self['uri']

    def set_uri(self, value):
        self['uri'] = value

    uri = property(get_uri, set_uri)

    def get_scheme(self):
        if 'scheme' in self:
            return self['scheme']
        return 'http'

    def set_scheme(self, value):
        self['scheme'] = value

    scheme = property(get_scheme, set_scheme)

    def set_headers(self, value):
        self['headers'] = value

    def get_headers(self):
        if 'headers' in self:
            return self['headers']
        return {}

    headers = property(get_headers, set_headers)

    def set_environ(self, value):
        self['environ'] = value

    def get_environ(self):
        if 'environ' in self:
            return self['environ']
        return {}

    environ = property(get_environ, set_environ)


class DummyResponse(object):
    def getvalue(self):
        return self.out.getvalue()

    def reset(self):
        self.clear()
        self.headers = {}
        self.status_code = 200

    def clear(self):
        self.out = StringIO()

    def set_status(self, status_code):
        self.status_code = status_code

    def error(self, status_code):
        self.set_status(status_code)


def create_test_handler(handler_class):
    instance = handler_class()
    instance.request = DummyRequest()
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
    os.environ['SERVER_SOFTWARE'] = 'Development'
    os.environ['HTTP_HOST'] = 'localhost'
    if len(sys.argv) >= 2:
        discover_path = os.path.abspath(sys.argv[1])
    else:
        discover_path = os.path.dirname(os.path.abspath(__file__))
    suite = unittest.loader.TestLoader().discover(discover_path)
    unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == '__main__':
    main()
