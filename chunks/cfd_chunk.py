"""
Compressed Full Data (CFD) chunk format.

Revision history:
- 12 March 2016: Initial commit, based on the code [mfulghum] developed originally back in 2014.
"""

import base_chunk
import struct
import numpy as np
from collections import namedtuple

class CFDChunk(base_chunk.BaseChunk):
    """
    Compressed Full Data chunk type.
    """
    __metaclass__ = base_chunk.MetaChunk



    def _generate_chunk_type(self, bytecode):
        """
        Generate chunk types for CFD files.
        :param bytecode:
        :return:
        """
        if bytecode is None:
            raise base_chunk.ChunkException('CFD chunks require a bytecode!')

        chunk_format = {}
        index = 0

        field_names = []
        field_packing = '<'

        chunk_data = [chunk_format, index, field_names, field_packing]

        def add_parameter(chunk_data, parameter_name, packing):
            param_type = {'L':np.uint32, 'l':np.int32,
                          'H': np.uint16, 'h': np.int16,
                          'B':np.uint8, 'b':np.int8,
                          'd':np.float64, 'f':np.float32,
                          '0s':None}
            chunk_data[0][parameter_name] = (chunk_data[1], packing, param_type[packing])
            chunk_data[1] += struct.calcsize(chunk_format[parameter_name][1])
            chunk_data[2].append(parameter_name)
            chunk_data[3] += chunk_format[parameter_name][1]

        add_parameter(chunk_data, 'bytecode', 'H')
        add_parameter(chunk_data, 'status', 'L' if (bytecode & 0x0001) > 0 else 'H')
        add_parameter(chunk_data, 'hit_surface', 'h' if (bytecode & 0x0002) > 0 else 'b')
        add_parameter(chunk_data, 'hit_face', 'h' if (bytecode & 0x0004) > 0 else 'b')
        add_parameter(chunk_data, 'parent', 'h' if (bytecode & 0x0008) > 0 else 'b')
        add_parameter(chunk_data, 'inside', 'h' if (bytecode & 0x0010) > 0 else 'b')
        add_parameter(chunk_data, 'paramA', 'L' if (bytecode & 0x0020) > 0 else '0s')
        add_parameter(chunk_data, 'paramB', 'L' if (bytecode & 0x0040) > 0 else '0s')
        add_parameter(chunk_data, 'starting_phase', 'f' if (bytecode & 0x0080) > 0 else '0s')
        add_parameter(chunk_data, 'phase_of', 'f' if (bytecode & 0x0100) > 0 else '0s')
        add_parameter(chunk_data, 'phase_at', 'f' if (bytecode & 0x0200) > 0 else '0s')

        add_parameter(chunk_data, 'Exr', 'f' if (bytecode & 0x0400) > 0 else '0s')
        add_parameter(chunk_data, 'Exi', 'f' if (bytecode & 0x0400) > 0 else '0s')
        add_parameter(chunk_data, 'Eyr', 'f' if (bytecode & 0x0400) > 0 else '0s')
        add_parameter(chunk_data, 'Eyi', 'f' if (bytecode & 0x0400) > 0 else '0s')
        add_parameter(chunk_data, 'Ezr', 'f' if (bytecode & 0x0400) > 0 else '0s')
        add_parameter(chunk_data, 'Ezi', 'f' if (bytecode & 0x0400) > 0 else '0s')

        add_parameter(chunk_data, 'index', 'f' if (bytecode & 0x0800) > 0 else '0s')
        add_parameter(chunk_data, 'path_to', 'f' if (bytecode & 0x1000) > 0 else '0s')

        add_parameter(chunk_data, 'x', 'f')
        add_parameter(chunk_data, 'y', 'f')
        add_parameter(chunk_data, 'z', 'f')

        add_parameter(chunk_data, 'intensity', 'f')

        add_parameter(chunk_data, 'u', 'f')
        add_parameter(chunk_data, 'v', 'f')
        add_parameter(chunk_data, 'w', 'f')

        add_parameter(chunk_data, 'nx', 'f')
        add_parameter(chunk_data, 'ny', 'f')
        add_parameter(chunk_data, 'nz', 'f')

        # Note that wavenumber also only pops up if hit_surface > 0 and (bytecode & 0x1000) == 0, but we can't check
        # for that here.
        add_parameter(chunk_data, 'wavenumber', '0s')

        chunk_format, index, field_names, field_packing = chunk_data
        index -= 1

        chunk_length = sum([struct.calcsize(chunk_format[key][1]) for key in chunk_format.keys()])-1
        assert(index == chunk_length) # Sanity check the length

        return (field_names, field_packing)
