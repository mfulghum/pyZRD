"""
Definitions of ZRD "chunks" for compressed ray database formats. UFD files always follow the same chunk format for every
single ray segment, while CFD/CBD ray segments begin with a bytecode descriptor that describes what data are present for
that segment.

Revision history:
- 13 March 2016: Initial implementation of SQLAlchemy ORM system
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Binary, Text, String, ForeignKey
from sqlalchemy.orm import relationship, object_session
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.types import PickleType
from sqlalchemy import select, func

import struct

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
    bytecode = Column(Integer, ForeignKey('chunks.bytecode')) # Chunk bytecode
    chunk = relationship('Chunk', foreign_keys=[bytecode])
    data = Column(Binary) # Chunk data

    status = Column(Integer)
    hit_surface = Column(Integer)
    hit_face = Column(Integer)
    inside = Column(Integer)

    """
    @hybrid_property
    def bytecode(self):
        return struct.unpack('<H', self.data[0:2])[0]

    @hybrid_property
    def status(self):
        chunk_offset = object_session(self).query(Chunk.offsets).filter(Chunk.bytecode == self.bytecode).scalar()['status']
        data = struct.unpack(chunk_offset[1], self.data[chunk_offset[0]:chunk_offset[0] + struct.calcsize(chunk_offset[1])])
        return data[0] if len(data) == 1 else list(data)

    @status.expression
    def status(cls):
        return select([func.hex(func.substr(Segment.data, Chunk.status, Chunk.len_status))]).where(Chunk.bytecode==Segment.bytecode)

    @hybrid_property
    def hit_surface(self):
        chunk_offset = object_session(self).query(Chunk.offsets).filter(Chunk.bytecode == self.bytecode).scalar()['hit_surface']
        data = struct.unpack(chunk_offset[1], self.data[chunk_offset[0]:chunk_offset[0] + struct.calcsize(chunk_offset[1])])
        return data[0] if len(data) == 1 else list(data)

    @hit_surface.expression
    def hit_surface(cls):
        return select([func.substr(cls.data, Chunk.hit_surface, Chunk.len_hit_surface)]).where(Chunk.bytecode==cls.bytecode)
    """


class Chunk(Base):
    __tablename__ = 'chunks'

    bytecode = Column(Integer, primary_key=True)
    offsets = Column(PickleType)

    status = Column(Integer)
    hit_surface = Column(Integer)
    hit_face = Column(Integer)
    parent = Column(Integer)
    inside = Column(Integer)
    paramA = Column(Integer)
    paramB = Column(Integer)
    starting_phase = Column(Integer)
    phase_of = Column(Integer)
    phase_at = Column(Integer)
    polarization = Column(Integer)
    index = Column(Integer)
    path_to = Column(Integer)
    position = Column(Integer)
    intensity = Column(Integer)
    cosines = Column(Integer)
    normal = Column(Integer)
    wavenumber = Column(Integer)

    len_status = Column(Integer)
    len_hit_surface = Column(Integer)
    len_hit_face = Column(Integer)
    len_parent = Column(Integer)
    len_inside = Column(Integer)
    len_paramA = Column(Integer)
    len_paramB = Column(Integer)
    len_starting_phase = Column(Integer)
    len_phase_of = Column(Integer)
    len_phase_at = Column(Integer)
    len_polarization = Column(Integer)
    len_index = Column(Integer)
    len_path_to = Column(Integer)
    len_position = Column(Integer)
    len_intensity = Column(Integer)
    len_cosines = Column(Integer)
    len_normal = Column(Integer)
    len_wavenumber = Column(Integer)