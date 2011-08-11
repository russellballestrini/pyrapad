import transaction

from sqlalchemy import Integer, Unicode, String, Text, Boolean, DateTime
from sqlalchemy import Column, ForeignKey, desc, asc

from sqlalchemy.sql.expression import distinct

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound 

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, relation 

from zope.sqlalchemy import ZopeTransactionExtension

from datetime import datetime as dt

Base = declarative_base()
DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))

def initialize_sql( engine ):
    """Accept engine, configure DBsession and Base"""
    DBSession.configure( bind=engine )
    Base.metadata.bind = engine
    Base.metadata.create_all( engine )
    return DBSession

class Node( Base ):
    """This class represents a pad node"""
    __tablename__ = 'node'
    id        = Column( Integer, primary_key = True )
    pad_id  = Column( Integer, ForeignKey( 'pad.id' ), nullable = False )
    created   = Column( DateTime )
    syntax    = Column( String(16), nullable = True )
    data      = Column( Text, nullable = False )
    disabled  = Column( Boolean, default = False )

    def __init__( self, data, syntax=None ):
        self.data = data
        self.syntax = syntax
        self.created = dt.now()

class Pad( Base ):
    """This class represents a pad"""
    __tablename__ = 'pad'
    id       = Column( Integer, primary_key = True )
    uri      = Column( String(64), unique=True, nullable = False )
    disabled = Column( Boolean, default = False )

    nodes = relation( Node, order_by=desc( 'node.id' ), backref='pad' )

    def __init__( self, uri ):
        self.uri = uri

    @property
    def data( self ):
        """This will fetch the data from the first node of a pad"""
        return DBSession.query( Node ).filter( Node.pad_id == self.id ).order_by( asc( 'node.id') ).limit(1).one().data

    @property
    def syntax( self ):
        """This will fetch the syntax from the first node of a pad"""
        return DBSession.query( Node ).filter( Node.pad_id == self.id ).order_by( asc( 'node.id') ).limit(1).one().syntax

    @property
    def created( self ):
        """This will fetch the created from the first node of a pad"""
        return DBSession.query( Node ).filter( Node.pad_id == self.id ).order_by( asc( 'node.id') ).limit(1).one().created


def get_all_pads( ):
    """return all pad object"""
    return DBSession.query( Pad ).order_by( desc( Pad.id ) ).filter( Pad.disabled == False ).all()


def get_pad( pad_id ):
    """return all pad object"""
    try:
        return DBSession.query( Pad ).filter( Pad.disabled == False ).filter( Pad.id == pad_id ).one()
    except NoResultFound:
        return False

def get_all_syntaxes( ):
    """return a list of syntaxes"""
    return DBSession.query( distinct( Node.syntax) ).order_by( Node.syntax ).all()

