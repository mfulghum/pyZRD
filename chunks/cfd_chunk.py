"""
Compressed Full Data (CFD) chunk format.

Revision history:
- 12 March 2016: Initial commit, based on the code [mfulghum] developed originally back in 2014.
"""

import base_chunk
import struct
import numpy as np

class CFDChunk(base_chunk.BaseChunk):
    """
    Compressed Full Data chunk type.
    """
    __metaclass__ = base_chunk.MetaChunk

    def _generate_chunk_type(self, bytecode):
        """
        Generate the unique chunk type for UFD files. Not *really* necessary to do this but it leads to a cleaner
        implementation for handling all the different types of ZRD files.
        :param bytecode:
        :return:
        """
        if bytecode is None:
            raise base_chunk.ChunkException('CFD chunks require a bytecode!')

        chunk_format = {}
        index = 0

        chunk_format['bytecode'] = (index, '<H', np.uint16)
        index += struct.calcsize(chunk_format['bytecode'][1])

        chunk_format['status'] = (index, '<L', np.uint32) if (bytecode & 0x0001) > 0 else (index, '<H', np.uint16) # status
        index += struct.calcsize(chunk_format['status'][1])

        chunk_format['hit_surface'] = (index, '<h', np.int16) if (bytecode & 0x0002) > 0 else (index, '<b', np.int8) # hit surface
        index += struct.calcsize(chunk_format['hit_surface'][1])

        chunk_format['hit_face'] = (index, '<h', np.int16) if (bytecode & 0x0004) > 0 else (index, '<b', np.int8) # hit face
        index += struct.calcsize(chunk_format['hit_face'][1])

        chunk_format['parent'] = (index, '<h', np.int16) if (bytecode & 0x0008) > 0 else (index, '<b', np.int8) # parent
        index += struct.calcsize(chunk_format['parent'][1])

        chunk_format['inside'] = (index, '<h', np.int16) if (bytecode & 0x0010) > 0 else (index, '<b', np.int8) # inside
        index += struct.calcsize(chunk_format['inside'][1])

        chunk_format['paramA'] = (index, '<L', np.uint32) if ((bytecode & 0x0020) > 0) else (0, '', None)
        index += struct.calcsize(chunk_format['paramA'][1])

        chunk_format['paramB'] = (index, '<L', np.uint32) if ((bytecode & 0x0040) > 0) else (0, '', None)
        index += struct.calcsize(chunk_format['paramB'][1])

        chunk_format['starting_phase'] = (index, '<f', np.float32) if ((bytecode & 0x0080) > 0) else (0, '', None)
        index += struct.calcsize(chunk_format['starting_phase'][1])

        chunk_format['phase_of'] = (index, '<f', np.float32) if ((bytecode & 0x0100) > 0) else (0, '', None) # Untested!!! I have not yet encountered this bit in a ZRD file
        index += struct.calcsize(chunk_format['phase_of'][1])

        chunk_format['phase_at'] = (index, '<f', np.float32) if ((bytecode & 0x0200) > 0) else (0, '', None)
        index += struct.calcsize(chunk_format['phase_at'][1])

        chunk_format['polarization'] = (index, '<ffffff') if ((bytecode & 0x0400) > 0) else (0, '', None)
        index += struct.calcsize(chunk_format['polarization'][1])

        chunk_format['index'] = (index, '<f', np.float32) if ((bytecode & 0x0800) > 0) else (0, '', None)
        index += struct.calcsize(chunk_format['index'][1])

        chunk_format['path_to'] = (index, '<f', np.float32) if ((bytecode & 0x1000) > 0) else (0, '', None)
        index += struct.calcsize(chunk_format['path_to'][1])

        chunk_format['position'] = (index, '<fff', np.array)
        index += struct.calcsize(chunk_format['position'][1])

        chunk_format['intensity'] = (index, '<f', np.float32)
        index += struct.calcsize(chunk_format['intensity'][1])

        chunk_format['cosines'] = (index, '<fff', np.array)
        index += struct.calcsize(chunk_format['cosines'][1])

        chunk_format['normal'] = (index, '<fff', np.array)
        index += struct.calcsize(chunk_format['normal'][1])

        # Note that wavenumber also only pops up if hit_surface > 0 and (bytecode & 0x1000) == 0, but we can't check
        # for that here.
        chunk_format['wavenumber'] = (index, '<B', np.uint8)

        chunk_format['chunk_length'] = sum([struct.calcsize(chunk_format[key][1]) for key in chunk_format.keys()])-1
        assert(index == chunk_format['chunk_length']) # Sanity check the length
        return chunk_format