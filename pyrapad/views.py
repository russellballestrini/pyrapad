from pyrapad.models import DBSession
from pyrapad.models import Paste, Node

from pyramid.httpexceptions import HTTPFound

from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters import HtmlFormatter
from pygments.util import ClassNotFound

def add( request ):
    """homepage and add paste page"""  
    uri = data = ''

    if 'form.submitted' in request.params: # handle form
        try:
            form_uri = request.params['uri'].replace(' ', '-') # from form
            form_data = request.params['data']

        except KeyError:
            return { 'error': 'uri and data fields are required.' }
        
        try:
            form_syntax = request.params['syntax']
        except KeyError:
            form_syntax = None 

        paste = Paste( form_uri )
        node = Node( form_data, form_syntax )
 
        paste.nodes.append( node )       
 
        DBSession.add( paste )
        DBSession.flush()

        return HTTPFound( location = '/' + str( paste.id ) + '/' + paste.uri )

    else: # display form
        return { 'uri': uri, 'data': data }

def show( request ):
    """show the paste and reply form"""
    # prettier varible
    paste_id = request.matchdict['id']
    # query for the paste object by id
    paste = DBSession.query( Paste ).filter( Paste.id == paste_id ).first()   

    if not paste: # redirect home if invalid id
        return HTTPFound( location = '/' )

    try: # if missing url string
        paste_id = request.matchdict['uri']
    except KeyError:
        return HTTPFound( location = '/' + str( paste.id ) + '/' + paste.uri )

    pygnodes = []

    for node in paste.nodes:
        try: 
            lexer = get_lexer_by_name( node.syntax )
        except ClassNotFound:
            lexer = guess_lexer( node.data )
        #formatter = HtmlFormatter( linenos=True, style='tango' )
        formatter = HtmlFormatter( linenos=True, style='colorful' )
        pygnodes.append( highlight( node.data, lexer, formatter ) )

    pygpaste = pygnodes[-1]
    pygnodes = pygnodes[:-1]

    return { 'paste': paste, 'pygpaste': pygpaste, 'pygnodes': pygnodes }

def reply( request ):
    """handle paste reply"""
    # prettier varible
    paste_id = request.matchdict['id']
    # query for the paste object by id
    paste = DBSession.query( Paste ).filter( Paste.id == paste_id ).first()   

    if not paste: # redirect home if invalid id
        return HTTPFound( location = '/' )

    node = Node( request.params['data'], request.params['syntax'] )
    paste.nodes.append( node )

    return HTTPFound( location = '/' + str( paste.id ) + '/' + paste.uri )
