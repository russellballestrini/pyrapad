from pyrapad.models import DBSession
from pyrapad.models import Pad
from pyrapad.models import get_pad, get_all_pads, get_all_syntaxes

from pyramid.httpexceptions import HTTPFound, HTTPNotFound

from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters import HtmlFormatter
from pygments.util import ClassNotFound

import webhelpers.paginate as paginate

from uuid import uuid4

def save( request ):
    """homepage and save pad page"""  
    try: data = unicode( request.params['data'] )
    except: data = u''

    if data:
        if request.params['semail'] != '': return HTTPNotFound()

        pad = get_pad(request.params['pad_id'])

        if pad != None:
            # this is an edit of an existing pad.
            if request.remote_addr == pad.ip_addr:
                pad.data = data
        else:
            # this is an new or clone of an existing pad.

            # try to guess syntax (doesn't work most of the time).
            syntax = guess_lexer( data ).aliases[0]
            pad = Pad( str(uuid4()), data, syntax, request.remote_addr )
 
        DBSession.add( pad )
        DBSession.flush()

        return HTTPFound( location = '/' + str( pad.id ) + '/' + pad.uri )

    return { 'title' : 'Add a pad', 'pad_id' : '', 'data' : data }

def show( request ):
    """show the pad"""
    # prettier varible
    pad_id = request.matchdict['id']
    # query for the pad object by id
    pad = get_pad( pad_id )   

    if pad == None: # redirect home if invalid id
        return HTTPFound( location = '/' )

    try: # make sure 'uri' key in matchdict
        pad_uri = request.matchdict['uri']
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

    if pad == None: # redirect home if invalid id
        return HTTPFound( location = '/' )

    try: # make sure 'uri' key in matchdict
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

    if pad == None: # redirect home if invalid id
        return HTTPFound( location = '/' )

    return {
      'title'  : 'Clone pad',
      'pad_id' : '',
      'data'   : pad.data
    }

def edit(request):
    """edit the given pad"""
    # prettier varible
    pad_id = request.matchdict['id']
    # query for the pad object by id
    pad = get_pad( pad_id )

    if pad == None: # redirect home if invalid id
        return HTTPFound( location = '/' )

    return {
      'title'  : 'Edit pad',
      'pad_id' : pad_id,
      'data'   : pad.data
    }

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

    return { 'pads': pads, 'pad_count': pad_count, 'current_page': current_page } 

def syntaxes( request ):
    """list the supported syntaxes"""
    syntaxes = [ syntax[0] for syntax in get_all_syntaxes() ] 
    return { 'syntaxes': syntaxes }

def alter( request ):
    """alter the pad"""
    from slugify import slugify

    # prettier varible
    pad_id = request.matchdict['id']
    # query for the pad object by id
    pad = get_pad( pad_id )

    if pad == None: # redirect home if invalid id
        return HTTPFound( location = '/' )

    try: # make sure 'uri' key in matchdict
        pad_uri = request.matchdict['uri']
    except KeyError:
        return HTTPFound( location = '/' + str( pad.id ) + '/' + pad.uri )

    if 'save' in request.POST:

        try: pad.uri = slugify( request.params['newuri'] )
        except: pass 

        try: pad.syntax = request.params['newsyntax']
        except: pass

        if 'wordwrap' in request.params: pad.wordwrap = True
        else: pad.wordwrap = False

        DBSession.add( pad )
        DBSession.flush()

    return HTTPFound( location = '/' + str(pad.id) + '/' + pad.uri )

