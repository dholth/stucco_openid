from jinja2 import Markup
from openid.consumer import consumer
from openid.extensions import pape, sreg
from pyramid.security import remember
from pyramid.url import model_url
from webob.exc import HTTPFound

import logging
log = logging.getLogger(__name__)

class OpenID(object):
    """Handle the OpenID authentication flow."""

    def __init__(self, context, request):
        self.context=context
        self.request=request

    @property
    def base_url(self):
        return model_url(self.context, self.request)

    def get_consumer(self, request=None):
        """Create OpenID consumer."""
        store = self.request.context.store
        return consumer.Consumer(request.session, store)

    def index(self):
        return {}

    def redirect(self):
        """Redirect to OpenID provider or POST+JavaScript pseudo-redirect."""
        c = self.get_consumer(self.request)
        auth_request = c.begin(user_url=self.request.POST['url'])
        return_to = self.base_url.rstrip('/')+'/success'
        # is this the place to set ax/sreg extensions?
        if auth_request.shouldSendRedirect():
            redirectURL = auth_request.redirectURL(
                    self.request.application_url, 
                    return_to=return_to
                    )
            return HTTPFound(location=redirectURL)
        else: # send as a POST via an intermediary page:
            message = auth_request.formMarkup(self.request.application_url+'/', 
                    return_to=return_to)
            return {'openid_message':Markup(message)}
      
    def success(self):
        log.debug(self.request.url)
        c = self.get_consumer(self.request)
        # or request.params? (GET and POST)? can I ask for POST?
        log.debug("Session: %r" % self.request.session)
        info = c.complete(self.request.GET,
                self.request.application_url + self.request.path_info)
        log.debug("Session: %r" % self.request.session)
        log.debug(info.status)
        if info.status == consumer.SUCCESS:
            # not unicode:
            log.debug('Display identifier: ' + 
                    (info.getDisplayIdentifier() or ''))
            log.debug(info)

            # may be broken for Python 2.6?
            sreg_resp = sreg.SRegResponse.fromSuccessResponse(info)
            pape_resp = pape.Response.fromSuccessResponse(info)

            if info.endpoint.canonicalID:
                log.debug('i-name WTF %s' % info.endpoint.canonicalID)

            # need yet another step 'offer local account registration'
            headers = remember(self.request, info.getDisplayIdentifier())
            log.debug("Remember: %r" % (headers,))
            self.request.response_headerlist = headers
            self.request.session.save()
            return {'status':info.status,
                    'sreg_resp':sreg_resp, 'pape_resp':pape_resp, 
                    'display_id':info.getDisplayIdentifier()}
        
        else:
            self.request.session.save()
            return HTTPFound(location=self.base_url)
