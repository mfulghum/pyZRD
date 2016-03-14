"""
Definitions of ZRD "chunks" for compressed ray database formats. UFD files always follow the same chunk format for every
single ray segment, while CFD/CBD ray segments begin with a bytecode descriptor that describes what data are present for
that segment.

Revision history:
- 12 March 2016: Initial commit, based on the code [mfulghum] developed originally back in 2014.
"""

import weakref

class ChunkException(Exception):
    """
    Defines an exception for improperly trying to access data that isn't present in a chunk for whatever reason.
    Currently blank, but here as a placeholder if it becomes useful in the future.
    """
    def __init__(self, message):
        super(ChunkException, self).__init__(message)

class MetaChunk(type):
    """
    Chunk metaclass for treating chunk types as quasi-singletons.
    """
    def __call__(self, bytecode=None):
        """
        Check if a chunk has already been defined for a given bytecode, and return that chunk type if so.
        :param bytecode:
        :return:
        """
        if bytecode in self._chunk_objects:
            return self._chunk_objects[bytecode]
        else:
            chunk_type = type.__call__(self, bytecode)
            self._chunk_objects[bytecode] = chunk_type
            return chunk_type

class BaseChunk(object):
    """
    Base chunk object used to define a basic interface for interacting with chunks regardless of file format.
    """
    def __init__(self, bytecode=None):
        """
        May or may not take a bytecode, as UFD files do not use bytecodes at all.
        :param bytecode:
        :return:
        """
        # Chunk format is a dictionary of tuples in the format 'name:(offset, struct format)'
        self._chunk_format = self._generate_chunk_type(bytecode)

    def __getitem__(self, item):
        """
        Tries to get the details for how to access a parameter for a given chunk type.
        :param item:
        :return:
        """
        try:
            chunk_data = self._chunk_format[item]
            return chunk_data
        except Exception as ex:
            raise ChunkException('Missing chunk parameter %s' % ex)

    def _generate_chunk_type(self, bytecode=None):
        """
        Generates the chunk type formatting for a given bytecode.
        :param bytecode:
        :return:
        """
        pass