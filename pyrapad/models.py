"""Database models for pyrapad"""
from datetime import datetime
from typing import Optional

from sqlalchemy import String, UnicodeText, Boolean, DateTime, Integer, desc, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, scoped_session, sessionmaker
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from zope.sqlalchemy import register


class Base(DeclarativeBase):
    """Base class for all models"""
    pass


# Create scoped session
DBSession = scoped_session(sessionmaker())
register(DBSession)


def initialize_sql(engine):
    """Initialize the database connection and create tables"""
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
    return DBSession


class Pad(Base):
    """Model representing a code paste/pad"""
    __tablename__ = 'pad'

    # Primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # Pad identification and metadata
    uri: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    syntax: Mapped[Optional[str]] = mapped_column(String(16), nullable=True)

    # Content
    data: Mapped[str] = mapped_column(UnicodeText, nullable=False)

    # Status and display options
    disabled: Mapped[bool] = mapped_column(Boolean, default=False)
    wordwrap: Mapped[bool] = mapped_column(Boolean, default=False)

    # Audit fields
    created: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    ip_addr: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)

    def __init__(self, uri: str, data: str, syntax: Optional[str] = None,
                 ip_addr: Optional[str] = None):
        self.uri = uri
        self.data = data
        self.syntax = syntax
        self.created = datetime.now()
        self.ip_addr = ip_addr

    def __repr__(self) -> str:
        return f"<Pad(id={self.id}, uri='{self.uri}', syntax='{self.syntax}')>"


def get_all_pads():
    """Return all non-disabled pads ordered by ID descending"""
    stmt = select(Pad).where(Pad.disabled == False).order_by(desc(Pad.id))
    return list(DBSession.execute(stmt).scalars().all())


def get_pad(pad_id: int) -> Optional[Pad]:
    """Return pad object by ID, or None if not found or disabled"""
    try:
        stmt = select(Pad).where(
            Pad.disabled == False,
            Pad.id == pad_id
        )
        return DBSession.execute(stmt).scalar_one()
    except NoResultFound:
        return None


def get_all_syntaxes():
    """Return a list of all distinct syntax values used in pads"""
    stmt = select(Pad.syntax).distinct().order_by(Pad.syntax)
    return list(DBSession.execute(stmt).all())
