from pyramid.configuration import Configurator
from stucco_openid.models import get_root, OpenID

def configure(config, template_extension="jinja2"):
    """Add stucco_openid views, resources to `config`.
    
    template_extension: Change this to use another templating
    language. Only Jinja2 implementation included."""

    config.add_static_view('static', 'stucco_openid:static')

    config.add_view(
            view=".views.OpenID",
            for_=".models.OpenID",
            attr="index",
            renderer="openid.%s" % (template_extension,))

    config.add_view(
            view=".views.OpenID",
            for_=".models.OpenID",
            request_method="POST",
            attr="redirect",
            renderer="openid_redirect.%s" % (template_extension,))

    config.add_view(
            name="success",
            attr="success",
            for_=".models.OpenID",
            view=".views.OpenID",
            renderer="openid_success.%s" % (template_extension,))

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    import logging
    logging.basicConfig(level=logging.DEBUG)

    config = Configurator(root_factory=get_root, settings=settings)
    config.begin()

    from pyramid_jinja2 import renderer_factory
    config.add_renderer('.jinja2', renderer_factory)

    # configure views, templates
    configure(config) 

    # configure session
    import pyramid_beaker
    session_factory = pyramid_beaker.session_factory_from_settings(settings)
    config.set_session_factory(session_factory)

    # configure OpenID-specific storage
    import stucco_openid.models
    from openid.store import filestore
    stucco_openid.models.root.store = \
        filestore.FileOpenIDStore(settings['openid.store_file_path'])

    config.end()
    return config.make_wsgi_app()

