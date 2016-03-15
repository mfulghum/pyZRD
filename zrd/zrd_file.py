import struct
import mmap

import sql.db
import sql.elements

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
        self.session, self.engine = sql.db.initialize_database(verbose=verbose_SQL) if enable_SQL else (None, None)

        self.filename = filename

        with open(self.filename, 'rb') as fp:
            self.mm = mmap.mmap(fp.fileno(), 0, access=mmap.ACCESS_READ)

            file_type, = struct.unpack('<L', self.mm[0:4])
            self.version = file_type % 10000
            self.file_type = {0:'UFD', 1:'CBD', 2:'CFD'}[file_type / 10000]
            self.chunk_type = {'UFD':chunks.ufd_chunk.UFDChunk,
                               'CBD':chunks.cbd_chunk.CBDChunk,
                               'CFD':chunks.cfd_chunk.CFDChunk}[self.file_type]
            self.chunk_type._chunk_objects = {}

            self.max_segments, = struct.unpack('<L', self.mm[4:8])
            file_index = 8

            rays = []
            segments = []

            ray_index = 0
            while True:
                if file_index+4 > len(self.mm):
                    break

                num_segments, = struct.unpack('<L', self.mm[file_index:file_index+4])
                file_index += 4

                rays += [{'file_index':file_index}]

                new_segments = [{'parent':ray_index, 'segment_number':segnum} for segnum in xrange(num_segments)]
                for n in xrange(num_segments):
                    chunk = self.decode_chunk(file_index)

                    bytecode = self.read_parameter(chunk['bytecode'], file_index)
                    new_segments[n].update({'file_index':file_index, 'bytecode':bytecode})

                    if (bytecode & 0x1000) == 0 and self.read_parameter(chunk['hit_surface'], file_index) > 0:
                        file_index += 1 # Deal with the presence of the wavenumber entry
                    file_index += chunk['chunk_length']
                segments += new_segments

                ray_index += 1

            if enable_SQL:
                conn = self.engine.connect()
                conn.execute(sql.elements.Ray.__table__.insert(), rays)
                conn.execute(sql.elements.Segment.__table__.insert(), segments)
                conn.close()

    def decode_chunk(self, file_index):
        bytecode, = struct.unpack('<H', self.mm[file_index:file_index+2])
        return self.chunk_type(bytecode)

    def read_parameter(self, parameter, file_index):
        idx = file_index + parameter[0]
        data, = struct.unpack(parameter[1], self.mm[idx:idx+struct.calcsize(parameter[1])])
        return data