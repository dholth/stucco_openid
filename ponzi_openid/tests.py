import unittest

from pyramid.configuration import Configurator
from pyramid import testing

class ViewTests(unittest.TestCase):
    def setUp(self):
        self.config = Configurator()
        self.config.begin()

    def tearDown(self):
        self.config.end()

    def test_my_view(self):
        from ponzi_openid.views import OpenID
        request = testing.DummyRequest()
        info = OpenID(None, request).index()
        self.assertEqual(info, {})


