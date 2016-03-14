"""
Definitions of ZRD "chunks" for compressed ray database formats. UFD files always follow the same chunk format for every
single ray segment, while CFD/CBD ray segments begin with a bytecode descriptor that describes what data are present for
that segment.

Revision history:
- 13 March 2016: Initial implementation of SQLAlchemy ORM system
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from elements import Base

def initialize_database(verbose=True):
    """
    Start the SQLAlchemy engine (using sqlite in memory for speed).
    Verbose flag shows *all* SQL commands being passed to the database.
    :param verbose:
    :return:
    """
    engine = create_engine('sqlite:///:memory:', echo=verbose)
    Base.metadata.create_all(engine)

    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()

    return session, engine

def shutdown_database(session, engine):
    """
    Close out all of the connections to the SQL database and shut it down.
    :param session:
    :param engine:
    :return:
    """
    session.close()
    engine.dispose()