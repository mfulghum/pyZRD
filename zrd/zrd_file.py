import struct
import mmap

import sql.db
from sql.elements import Ray, Segment

# Import the different kinds of chunks
import chunks.ufd_chunk
import chunks.cbd_chunk
import chunks.cfd_chunk

class ZRDFile(object):
    def __init__(self, filename, enable_SQL=True, verbose_SQL=False):
        """
        Load a ZRD file into memory

        :param filename:
        :return:
        """
        self._SQL = enable_SQL
        self.session, self.engine = sql.db.initialize_database(verbose=verbose_SQL) if enable_SQL else (None, None)

        self.filename = filename

        fp = open(self.filename, 'rb')
        self.data = mmap.mmap(fp.fileno(), 0, access=mmap.ACCESS_READ)

        file_type, = struct.unpack('<L', self.data[0:4])
        self.version = file_type % 10000
        self.file_type = {0:'UFD', 1:'CBD', 2:'CFD'}[file_type / 10000]
        self.chunk_type = {'UFD':chunks.ufd_chunk.UFDChunk,
                           'CBD':chunks.cbd_chunk.CBDChunk,
                           'CFD':chunks.cfd_chunk.CFDChunk}[self.file_type]
        self.chunk_type._chunk_objects = {}

        self.max_segments, = struct.unpack('<L', self.data[4:8])
        file_index = 8

        rays = []
        segments = []

        segment_keys = set(Segment.__table__.columns.keys()) - {'id', 'parent', 'file_index', 'segment_number'}

        ray_index = 0
        while True:
            if file_index+4 > len(self.data):
                break

            num_segments, = struct.unpack('<L', self.data[file_index:file_index+4])
            file_index += 4

            rays += [{'file_index':file_index}]

            new_segments = [{'parent':ray_index, 'segment_number':segnum} for segnum in xrange(num_segments)]
            for n in xrange(num_segments):
                chunk = self.decode_chunk(file_index)
                new_segments[n]['data'] = self.data[file_index:file_index+chunk['chunk_length']]

                new_segments[n]['file_index'] = file_index
                new_segments[n]['bytecode'] = self.read_parameter(chunk['bytecode'], new_segments[n]['data'])

                #chunk_keys = segment_keys & set(chunk.keys()) - {'wavenumber'}
                #new_segments[n].update({key:self.read_parameter(chunk[key], file_index) for key in (segment_keys & chunk_keys)})

                if (new_segments[n]['bytecode'] & 0x1000) == 0 and self.read_parameter(chunk['hit_surface'], new_segments[n]['data']) > 0:
                    file_index += 1 # Deal with the presence of the wavenumber entry
                file_index += chunk['chunk_length']
            segments += new_segments

            ray_index += 1

        if enable_SQL:
            conn = self.engine.connect()
            conn.execute(Ray.__table__.insert(), rays)
            conn.execute(Segment.__table__.insert(), segments)
            conn.close()
        else:
            self.ray_elements = rays
            self.segment_elements = segments

    @property
    def rays(self):
        return self.session.query(Ray) if self._SQL else self.ray_elements

    @property
    def segments(self):
        return self.session.query(Segment) if self._SQL else self.segment_elements

    def decode_chunk(self, file_index):
        bytecode, = struct.unpack('<H', self.data[file_index:file_index+2])
        return self.chunk_type(bytecode)

    def read_parameter(self, parameter, chunk_data):
        if parameter[1] is '':
            return None

        data = struct.unpack(parameter[1], chunk_data[parameter[0]:parameter[0]+struct.calcsize(parameter[1])])

        if len(data) > 1:
            return data
        elif len(data) == 1:
            return data[0]