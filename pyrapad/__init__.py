from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from pyrapad.models import initialize_sql

from pyramid.events import BeforeRender


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    initialize_sql(engine)
    config = Configurator(settings=settings)

    # inject renderer globals
    config.add_subscriber( inject_renderer_globals, BeforeRender )

    config.add_static_view('static', 'pyrapad:static')
    config.add_route( 'home', '/', view='pyrapad.views.add', view_renderer='add.mako' )
    config.add_route( 'add', '/add', view='pyrapad.views.add', view_renderer='add.mako' )
    config.add_route( 'random', '/random', view='pyrapad.views.random' )
    config.add_route( 'recent', '/recent', view='pyrapad.views.recent', view_renderer='recent.mako' )
    config.add_route( 'syntaxes', '/syntaxes', view='pyrapad.views.syntaxes', view_renderer='syntaxes.mako' )
    config.add_route( 'reply', '/{id}/reply', view='pyrapad.views.reply' )
    config.add_route( 'show', '{id}/{uri:.*}', view='pyrapad.views.show', view_renderer='show.mako' )
    config.add_route( 'show2', '{id}', view='pyrapad.views.show', view_renderer='show.mako' )

    return config.make_wsgi_app()


def inject_renderer_globals( event ):
    """Inject some renderer globals before passing to template"""

    request = event['request']

    # Build ${title} from the current request.path  
    event['title'] =  ' - '.join( request.path.replace( '-', ' ' ).split( '/' )[1:] ).title()
    
    # Build ${google.analytics} from the configuration file  
    event['google_analytics_key'] = request.registry.settings[ 'google_analytics_key' ]
