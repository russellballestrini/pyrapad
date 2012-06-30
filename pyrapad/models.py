import transaction

from sqlalchemy import Integer, String, UnicodeText, Boolean, DateTime
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

class Pad( Base ):
    """This class represents a pad"""
    __tablename__ = 'pad'
    id       = Column( Integer, primary_key = True )
    uri      = Column( String(64), unique=True, nullable = False )
    syntax   = Column( String(16), nullable = True )
    data     = Column( UnicodeText, nullable = False )
    disabled = Column( Boolean, default = False )
    created  = Column( DateTime )

    def __init__( self, uri, data, syntax=None ):
        self.uri = uri
        self.data = data
        self.syntax = syntax
        self.created = dt.now()

def get_all_pads( ):
    """return all pad object"""
    return DBSession.query( Pad ).order_by( desc( Pad.id ) ).filter( Pad.disabled == False ).all()


def get_pad( pad_id ):
    """return pad object by id"""
    try:
        return DBSession.query( Pad ).filter( Pad.disabled == False ).filter( Pad.id == pad_id ).one()
    except NoResultFound:
        return False

def get_all_syntaxes( ):
    """return a list of syntaxes"""
    return DBSession.query( distinct( Pad.syntax) ).order_by( Pad.syntax ).all()

