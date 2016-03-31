import struct
import mmap

import sql.db
from sql.elements import Ray, Segment

# Import the different kinds of chunks
import chunks.ufd_chunk
import chunks.cbd_chunk
import chunks.cfd_chunk

class ZRDFile(object):
    def __init__(self, filename, enable_SQL=True, verbose_SQL=False, sql_filename=None):
        """
        Load a ZRD file into memory

        :param filename:
        :return:
        """
        self._SQL = enable_SQL
        self.session, self.engine = sql.db.initialize_database(verbose=verbose_SQL, filename=sql_filename) if enable_SQL else (None, None)

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

        ray_index = 0
        while True:
            if file_index+4 > len(self.data):
                break

            num_segments, = struct.unpack('<L', self.data[file_index:file_index+4])
            file_index += 4

            rays += [{'file_index':file_index}]
            segment_wavenumber = 0

            new_segments = [{'parent':ray_index, 'segment_number':segnum} for segnum in xrange(num_segments)]
            for n in xrange(num_segments):
                new_segments[n]['file_index'] = file_index
                chunk_fields, chunk_packing = self.decode_chunk(file_index)
                chunk_length = struct.calcsize(chunk_packing)

                data = self.data[file_index:file_index+chunk_length]
                file_index += chunk_length

                segment_data = dict(zip(chunk_fields, struct.unpack(chunk_packing, data)))
                for key,value in segment_data.items():
                    if value == '':
                        segment_data[key] = None

                if (segment_data['bytecode'] & 0x1000) == 0 and \
                        segment_data['hit_surface'] > 0:
                    segment_wavenumber, = struct.unpack('<B', self.data[file_index:file_index+1])
                    file_index += 1 # Deal with the presence of the wavenumber entry

                segment_data['wavenumber'] = segment_wavenumber
                new_segments[n].update(segment_data)
            segments += new_segments

            ray_index += 1

        if enable_SQL:
            conn = self.engine.connect()
            conn.execute(Ray.__table__.insert(), rays)
            conn.execute(Segment.__table__.insert(), segments)
            conn.close()
            self.session.commit()
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
        chunk = self.chunk_type(bytecode)
        return chunk[0], chunk[1]

    def read_parameter(self, parameter, chunk_data):
        if parameter[1] is '':
            return None

        data = struct.unpack(parameter[1], chunk_data[parameter[0]:parameter[0]+struct.calcsize(parameter[1])])

        if len(data) > 1:
            return data
        elif len(data) == 1:
            return data[0]