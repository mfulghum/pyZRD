"""
Compressed Basic Data (CBD) chunk format.

Revision history:
- 12 March 2016: Initial commit, based on the code [mfulghum] developed originally back in 2014.
"""

import base_chunk

class CBDChunk(base_chunk.BaseChunk):
    """
    Compressed Basic Data chunk type.
    """
    __metaclass__ = base_chunk.MetaChunk

    def __init__(self, bytecode):
        """
        Compressed basic data files use a bytecode method to show what data are present in a segment and where they can
        be found.
        :param bytecode:
        :return:
        """
        # Call the BaseChunk constructor
        super(CBDChunk, self).__init__()

        # Raise an exception as CBD files are not yet supported.
        raise base_chunk.ChunkException('CBD files are not currently supported!')