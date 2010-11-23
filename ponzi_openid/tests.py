import unittest

from pyramid.configuration import Configurator
from pyramid import testing

import logging
log = logging.getLogger()

class ViewTests(unittest.TestCase):
    def setUp(self):
        self.config = Configurator()
        self.config.begin()

    def tearDown(self):
        self.config.end()

    def test_index(self):
        from ponzi_openid.views import OpenID
        request = testing.DummyRequest()
        info = OpenID(None, request).index()
        self.assertEqual(info, {})

    def test_redirect(self):
        import webob.exc
        from ponzi_openid.views import OpenID
        from ponzi_openid.models import OpenID as OpenID_model

        class DummyBegin:
            redirect=False
            def shouldSendRedirect(self, *args):
                return self.redirect

            def formMarkup(*args, **kw):
                log.debug(kw['return_to'])
                return '<form>http://myapp.example.org</form>'

            def redirectURL(*args, **kw):
                return 'http://myapp.example.org'

        class DummyConsumer:
            def __init__(self, *args, **kw):
                pass

            def begin(*args, **kw):
                return DummyBegin()

        context = OpenID_model()
        context.store = {}

        request = testing.DummyRequest(
                post={'url':'http://www.example.org/'}, 
                session={})

        OpenID.Consumer = DummyConsumer
        cut = OpenID(context, request)

        DummyBegin.redirect = True
        rc = cut.redirect()
        assert isinstance(rc, webob.exc._HTTPMove)

        DummyBegin.redirect = False
        rc = cut.redirect()
        assert 'openid_message' in rc, 'No openid_message for renderer'
