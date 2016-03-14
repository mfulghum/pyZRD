
import struct
import mmap

# Import the different kinds of chunks
import chunks.ufd_chunk
import chunks.cbd_chunk
import chunks.cfd_chunk

class database(object):
    def __init__(self, filename):
        with open(filename, 'rb') as fp:
            mm = mmap.mmap(fp.fileno(), 0, access=mmap.ACCESS_READ)

            self.file_type, = struct.unpack('<L', mm[0:4])
            self.max_segments, = struct.unpack('<L', mm[4:8])

            self.chunk_type = {2001:chunks.ufd_chunk.UFDChunk,
                               12001:chunks.cbd_chunk.CBDChunk,
                               22001:chunks.cfd_chunk.CFDChunk}[self.file_type]

            file_index = 8
            chunk_bytecode = struct.unpack('<H', mm[file_index:file_index+2])[0] if self.chunk_type is not chunks.ufd_chunk else None
            chunk = self.chunk_type(chunk_bytecode)
            print(chunk)
