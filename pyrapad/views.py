from pyrapad.models import DBSession
from pyrapad.models import Pad, Node
from pyrapad.models import get_pad, get_all_pads, get_all_syntaxes

from pyramid.httpexceptions import HTTPFound

from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters import HtmlFormatter
from pygments.util import ClassNotFound

import webhelpers.paginate as paginate

from datetime import datetime as dt

def add( request ):
    """homepage and add pad page"""  
    uri = data = ''

    if 'form.submitted' in request.params: # handle form
        try:
            form_uri = request.params['uri'].replace(' ', '-')
            form_data = request.params['data']
            #form_syntax = request.params['syntax']
            if not form_uri or not form_data:
                return { 'error': 'uri and data fields are required.' }

        except KeyError:
            return { 'error': 'uri and data fields are required.' }
        
        # this block supports syntax guessing,
        # but it doesn't work well ...
        form_syntax = request.params['syntax']
        try: 
            form_syntax = get_lexer_by_name( form_syntax ).aliases[0]
        except ClassNotFound:
            form_syntax = guess_lexer( form_data ).aliases[0]

        pad = Pad( form_uri )
        node = Node( form_data, form_syntax )
 
        pad.nodes.append( node )       
 
        DBSession.add( pad )
        DBSession.flush()

        return HTTPFound( location = '/' + str( pad.id ) + '/' + pad.uri )

    else: # display form
        return { 'uri': uri, 'data': data }

def show( request ):
    """show the pad and reply form"""
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

    pygnodes = []

    for node in pad.nodes:
        try: 
            lexer = get_lexer_by_name( node.syntax )
        except ClassNotFound:
            lexer = guess_lexer( node.data )
        #formatter = HtmlFormatter( style='colorful' )
        #formatter = HtmlFormatter( style='tango' )
        formatter = HtmlFormatter( linenos=True, style='tango' )
        pygnodes.append( highlight( node.data, lexer, formatter ) )

    pygpad = pygnodes[-1]
    pygnodes = pygnodes[:-1]

    return { 'pad': pad, 'pygpad': pygpad, 'pygnodes': pygnodes }

def reply( request ):
    """handle pad reply"""
    # prettier varible
    pad_id = request.matchdict['id']
    # query for the papad object by id
    pad = get_pad( pad_id )   

    if not pad: # redirect home if invalid id
        return HTTPFound( location = '/' )

    node = Node( request.params['data'], request.params['syntax'] )
    pad.nodes.append( node )

    return HTTPFound( location = '/' + str( pad.id ) + '/' + pad.uri )


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

    # get first 5 lines of each pad and run it into pygments
    pygpads = []
    for pad in pads:
        # get the first 5 lines in the pad
        data = pad.data.split( '\n', 5 )[:5]
        data = '\n'.join( data )

        lexer = get_lexer_by_name( pad.syntax )
        #formatter = HtmlFormatter( style='tango' )
        formatter = HtmlFormatter( linenos=True, style='tango' )
        pygpads.append( highlight( data, lexer, formatter ) )

    timenow = dt.now()

    return { 'pads': pads, 'pygpads': pygpads, 'pad_count': pad_count, 'current_page': current_page, 'timenow': timenow } 

def syntaxes( request ):
    """list the supported syntaxes"""
    syntaxes = [ syntax[0] for syntax in get_all_syntaxes() ] 
    return { 'syntaxes': syntaxes }
