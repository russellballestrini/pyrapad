import transaction

from sqlalchemy import Integer, Unicode, String, Text, Boolean
from sqlalchemy import Column, ForeignKey, desc, asc

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relation 

from zope.sqlalchemy import ZopeTransactionExtension

Base = declarative_base()
DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))

def initialize_sql( engine ):
    """Accept engine, configure DBsession and Base"""
    DBSession.configure( bind=engine )
    Base.metadata.bind = engine
    Base.metadata.create_all( engine )
    return DBSession

class Node( Base ):
    """This class represents a paste node"""
    __tablename__ = 'node'
    id        = Column( Integer, primary_key = True )
    paste_id  = Column( Integer, ForeignKey( 'paste.id' ), nullable = False )
    data      = Column( Text, nullable = False )
    syntax    = Column( String(16), nullable = True )
    disabled  = Column( Boolean, default = False )

    def __init__( self, data, syntax=None ):
        self.data = data
        self.syntax = syntax

class Paste( Base ):
    """This class represents a paste"""
    __tablename__ = 'paste'
    id       = Column( Integer, primary_key = True )
    uri      = Column( String(64), unique=True, nullable = False )
    disabled = Column( Boolean, default = False )

    nodes = relation( Node, order_by=desc( 'node.id' ), backref='paste' )

    def __init__( self, uri ):
        self.uri = uri

    @property
    def data( self ):
        """This will fetch the data from the first node of a paste"""
        return DBSession.query( Node ).filter( Node.paste_id == self.id ).order_by( asc( 'node.id') ).limit(1).one().data

    @property
    def syntax( self ):
        """This will fetch the syntax from the first node of a paste"""
        return DBSession.query( Node ).filter( Node.paste_id == self.id ).order_by( asc( 'node.id') ).limit(1).one().syntax
