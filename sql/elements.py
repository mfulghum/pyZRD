"""
Definitions of ZRD "chunks" for compressed ray database formats. UFD files always follow the same chunk format for every
single ray segment, while CFD/CBD ray segments begin with a bytecode descriptor that describes what data are present for
that segment.

Revision history:
- 13 March 2016: Initial implementation of SQLAlchemy ORM system
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.orderinglist import ordering_list

Base = declarative_base()

class Ray(Base):
    __tablename__ = 'rays'

    id = Column(Integer, primary_key=True, nullable=False)
    segments = relationship('Segment', back_populates='ray', order_by='Segment.segment_number', collection_class=ordering_list('segment_number'))

    file_index = Column(Integer) # Position (in bytes) in the ZRD file of the first segment

class Segment(Base):
    __tablename__ = 'segments'

    id = Column(Integer, primary_key=True, nullable=False)
    segment_number = Column(Integer)
    parent = Column(Integer, ForeignKey('rays.id'))
    ray = relationship('Ray', back_populates='segments')

    file_index = Column(Integer) # Position (in bytes) in the ZRD file of the segment
    bytecode = Column(Integer)
    status = Column(Integer)
    hit_surface = Column(Integer)
    hit_face = Column(Integer)
    inside = Column(Integer)
    paramA = Column(Integer)
    paramB = Column(Integer)

    starting_phase = Column(Float)
    phase_of = Column(Float)
    phase_at = Column(Float)

    Exr = Column(Float)
    Exi = Column(Float)
    Eyr = Column(Float)
    Eyi = Column(Float)
    Ezr = Column(Float)
    Ezi = Column(Float)

    index = Column(Float)
    path_to = Column(Float)

    x = Column(Float)
    y = Column(Float)
    z = Column(Float)

    intensity = Column(Float)

    u = Column(Float)
    v = Column(Float)
    w = Column(Float)

    nx = Column(Float)
    ny = Column(Float)
    nz = Column(Float)

    wavenumber = Column(Integer)
