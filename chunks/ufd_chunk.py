"""
Uncompressed Full Data (UFD) chunk format.

Revision history:
- 12 March 2016: Initial commit, based on the code [mfulghum] developed originally back in 2014.
"""

import base_chunk
import struct

class UFDChunk(base_chunk.BaseChunk):
    """
    Uncompressed Full Data chunk type.
    """
    __metaclass__ = base_chunk.MetaChunk

    def _generate_chunk_type(self, bytecode=None):
        """
        Generate the unique chunk type for UFD files. Not *really* necessary to do this but it leads to a cleaner
        implementation for handling all the different types of ZRD files.
        :param bytecode:
        :return:
        """
        if bytecode is not None:
            raise base_chunk.ChunkException('UFD chunks do not have bytecodes!')

        chunk_format = {}
        chunk_format['bytecode'] = (0, '')
        chunk_format['status'] = (0, '<I')
        chunk_format['level'] = (4, '<i')
        chunk_format['hit_surface'] = (8, '<i')
        chunk_format['hit_face'] = (12, '<i')
        chunk_format['unused'] = (16, '<I')# Unused 4 byte chunk -->here<--
        chunk_format['inside'] = (20, '<i')
        chunk_format['parent'] = (24, '<i')
        chunk_format['storage'] = (28, '<i')
        chunk_format['xybin'] = (32, '<i')
        chunk_format['lmbin'] = (36, '<i')
        chunk_format['index'] = (40, '<d')
        chunk_format['starting_phase'] = (48, '<d')
        chunk_format['position'] = (56, '<ddd')
        chunk_format['cosines'] = (80, '<ddd')
        chunk_format['normal'] = (104, '<ddd')
        chunk_format['path_to'] = (128, '<d')
        chunk_format['intensity'] = (136, '<d')
        chunk_format['phase_of'] = (144, '<d')
        chunk_format['phase_at'] = (152, '<d')
        chunk_format['polarization'] = (160, '<dddddd')

        chunk_format['chunk_length'] = sum([struct.calcsize(chunk_format[key][1]) for key in chunk_format.keys()])
        return chunk_format
