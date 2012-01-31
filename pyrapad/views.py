from pyrapad.models import DBSession
from pyrapad.models import Pad, Node
from pyrapad.models import get_pad, get_all_pads, get_all_syntaxes

from pyramid.httpexceptions import HTTPFound, HTTPNotFound

from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters import HtmlFormatter
from pygments.util import ClassNotFound

import webhelpers.paginate as paginate

from datetime import datetime as dt

from uuid import uuid4

def save( request ):
    """homepage and save pad page"""  
    try: data = request.params['data']
    except: data = ''

    try: data_form = request.params['data_form']
    except: data_form = ''

    if data_form:
        if request.params['semail'] != '': return HTTPNotFound()

        uri = str( uuid4() ) 
        
        # this block supports syntax guessing,
        # but it doesn't work well ...
        syntax = guess_lexer( data_form ).aliases[0]

        pad = Pad( uri )
        node = Node( data_form, syntax )
 
        pad.nodes.append( node )       
 
        DBSession.add( pad )
        DBSession.flush()

        return HTTPFound( location = '/' + str( pad.id ) + '/' + pad.uri )

    else: # display form
        return { 'title': 'Add a pad', 'data': data }

def show( request ):
    """show the pad"""
    # prettier varible
    pad_id = request.matchdict['id']
    # query for the pad object by id
    pad = get_pad( pad_id )   

    if not pad: # redirect home if invalid id
        return HTTPFound( location = '/' )

    try: # if missing url string
        pad_id = request.matchdict['uri']
    except KeyError:
        return HTTPFound( location = '/' + str( pad.id ) + '/' + pad.uri )

    try: 
        lexer = get_lexer_by_name( pad.syntax )
    except ClassNotFound:
        lexer = guess_lexer( pad.data )
    formatter = HtmlFormatter( linenos=True, style='native' )
    pygdata = highlight( pad.data, lexer, formatter )

    return { 'pad': pad, 'pygdata': pygdata }

def raw( request ):
    """show the raw text pad"""
    # prettier varible
    pad_id = request.matchdict['id']
    # query for the pad object by id
    pad = get_pad( pad_id )   

    if not pad: # redirect home if invalid id
        return HTTPFound( location = '/' )

    try: # if missing url string
        pad_id = request.matchdict['uri']
    except KeyError:
        return HTTPFound( location = '/' + str( pad.id ) + '/' + pad.uri + '/raw' )

    return pad.data

def clone( request ):
    """clone the given pad"""
    # prettier varible
    pad_id = request.matchdict['id']
    # query for the pad object by id
    pad = get_pad( pad_id )   

    if not pad: # redirect home if invalid id
        return HTTPFound( location = '/' )

    return { 'title': 'Add a pad', 'data': pad.data }


def random( request ):
    """redirect to a random pad"""
    from random import choice
    pads = get_all_pads()
    pad  = choice( pads ) 
    return HTTPFound( location = '/' + str(pad.id) + '/' + pad.uri )

def recent( request ):
    """show most recent 20 pads and a few lines, and pagination"""
    try: current_page = int( request.params["page"] )
    except KeyError: current_page = 1

    # get all pads
    pads = get_all_pads( )
   
    # pad count
    pad_count = len( pads )
 
    # paginate pads 
    page_url = paginate.PageURL_WebOb( request )
    pads = paginate.Page( pads, current_page, url=page_url, items_per_page=20 )

    timenow = dt.now()

    return { 'pads': pads, 'pad_count': pad_count, 'current_page': current_page, 'timenow': timenow } 

def syntaxes( request ):
    """list the supported syntaxes"""
    syntaxes = [ syntax[0] for syntax in get_all_syntaxes() ] 
    return { 'syntaxes': syntaxes }
