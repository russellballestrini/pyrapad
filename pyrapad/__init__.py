from pyrapad.models import initialize_sql

from pyramid.events import BeforeRender

from pyramid.config import Configurator

from sqlalchemy import engine_from_config

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    engine = engine_from_config(settings, 'sqlalchemy.')
    initialize_sql(engine)

    config = Configurator(
        settings=settings,
    )

    # we now must include mako manually
    config.include('pyramid_mako')

    # inject renderer globals
    config.add_subscriber( inject_renderer_globals, BeforeRender )

    config.add_static_view('static', 'pyrapad:static')

    config.add_route( 'home', '/' )
    config.add_view( 'pyrapad.views.save', route_name='home', renderer='save.mako' )

    config.add_route( 'save', '/save' )
    config.add_view( 'pyrapad.views.save', route_name='save', renderer='save.mako' )

    config.add_route( 'random', '/random' )
    config.add_view( 'pyrapad.views.random', route_name='random' )

    config.add_route( 'recent', '/recent' )
    config.add_view( 'pyrapad.views.recent', route_name='recent', renderer='recent.mako' )

    config.add_route( 'syntaxes', '/syntaxes' )
    config.add_view( 'pyrapad.views.syntaxes', route_name='syntaxes', renderer='syntaxes.mako' )

    config.add_route( 'clone', '{id}/{uri:.*}/clone' )
    config.add_view( 'pyrapad.views.clone', route_name='clone', renderer='save.mako' )

    config.add_route( 'clone2', '{id}/clone' )
    config.add_view( 'pyrapad.views.clone', route_name='clone2', renderer='save.mako' )

    #......... ip_addr in db must match  ...............
    config.add_route( 'edit', '{id}/{uri:.*}/edit' )
    config.add_view( 'pyrapad.views.edit', route_name='edit', renderer='save.mako' )

    config.add_route( 'edit2', '{id}/edit' )
    config.add_view( 'pyrapad.views.edit', route_name='edit2', renderer='save.mako' )

    config.add_route( 'raw', '{id}/{uri:.*}/raw' )
    config.add_view( 'pyrapad.views.raw', route_name='raw', renderer='string' )

    config.add_route( 'raw2', '{id}/raw' )
    config.add_view( 'pyrapad.views.raw', route_name='raw2', renderer='string' )

    config.add_route( 'alter', '{id}/{uri:.*}/alter' )
    config.add_view( 'pyrapad.views.alter', route_name='alter' )

    config.add_route( 'show', '{id}/{uri:.*}' )
    config.add_view( 'pyrapad.views.show', route_name='show', renderer='show.mako' )

    config.add_route( 'show2', '{id}' )
    config.add_view( 'pyrapad.views.show', route_name='show2', renderer='show.mako' )

    return config.make_wsgi_app()


def inject_renderer_globals( event ):
    """Inject some renderer globals before passing to template"""

    request = event['request']

    # Build ${title} from the current request.path  
    event['title'] =  ' - '.join( request.path.replace( '-', ' ' ).split( '/' )[1:] ).title()
    
    # Build ${google.analytics} from the configuration file  
    event['google_analytics_key'] = request.registry.settings[ 'google_analytics_key' ]
