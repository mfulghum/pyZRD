import unittest

import chunks.base_chunk
import chunks.ufd_chunk
import chunks.cfd_chunk
import chunks.cbd_chunk

class TestChunkTyping(unittest.TestCase):
    def test_UFD_chunking(self):
        """
        Generate the UFD chunk type and ensure that it behaves properly
        :return:
        """
        chunks.ufd_chunk.UFDChunk._chunk_objects = {}
        self.assertEqual(chunks.ufd_chunk.UFDChunk._chunk_objects, {})

        # Generate the UFD chunk
        chunk = chunks.ufd_chunk.UFDChunk()

        # Check that the UFD chunk is now registered
        self.assertNotEqual(chunks.ufd_chunk.UFDChunk._chunk_objects, {})
        self.assertIn(chunk, chunks.ufd_chunk.UFDChunk._chunk_objects.values())

        # Generate a second UFD chunk
        chunk2 = chunks.ufd_chunk.UFDChunk()

        # Check that the new chunk is just a reference to the first
        self.assertIs(chunk, chunk2)

        # Check that a UFD chunk cannot be generated using a bytecode
        with self.assertRaises(chunks.base_chunk.ChunkException):
            chunk3 = chunks.ufd_chunk.UFDChunk(1234)

        # Check that the UFD chunks are exactly 208 bytes long
        self.assertEqual(chunk['chunk_length'], 208)

        # Check that it properly raises an exception if we try to grab a nonexistent property
        with self.assertRaises(chunks.base_chunk.ChunkException):
            result = chunk['nonsense']

    def test_CFD_chunking(self):
        """
        Generate a few different CFD chunk types and make sure they don't do anything unexpected
        :return:
        """
        chunks.cfd_chunk.CFDChunk._chunk_objects = {}
        self.assertEqual(chunks.cfd_chunk.CFDChunk._chunk_objects, {})

        # Check that a CFD chunk cannot be generated without a bytecode
        with self.assertRaises(chunks.base_chunk.ChunkException):
            chunk = chunks.cfd_chunk.CFDChunk()

        # Now check that we can generate a CFD chunk with a bytecode
        chunk = chunks.cfd_chunk.CFDChunk(1)

        # Check that the chunk is now registered
        self.assertNotEqual(chunks.cfd_chunk.CFDChunk._chunk_objects, {})
        self.assertIn(chunk, chunks.cfd_chunk.CFDChunk._chunk_objects.values())
        self.assertIn(1, chunks.cfd_chunk.CFDChunk._chunk_objects.keys())

        # Generate a second CFD chunk with the same bytecode
        chunk2 = chunks.cfd_chunk.CFDChunk(1)

        # Check that the new chunk is just a reference to the first
        self.assertIs(chunk2, chunk)

        # Generate a third CFD chunk with a new bytecode
        chunk3 = chunks.cfd_chunk.CFDChunk(2)

        # Check that it is now registered
        self.assertIn(chunk3, chunks.cfd_chunk.CFDChunk._chunk_objects.values())
        self.assertIn(2, chunks.cfd_chunk.CFDChunk._chunk_objects.keys())

        # Check that the new chunk is *not* a reference to the first chunk
        self.assertIsNot(chunk3, chunk)

        # Check that it properly raises an exception if we try to grab a nonexistent property
        with self.assertRaises(chunks.base_chunk.ChunkException):
            result = chunk['nonsense']

    def test_CBD_chunking(self):
        """
        Generate a few different CBD chunk types and make sure they don't do anything unexpected
        :return:
        """
        chunks.cbd_chunk.CBDChunk._chunk_objects = {}
        self.assertEqual(chunks.cbd_chunk.CBDChunk._chunk_objects, {})

        with self.assertRaises(chunks.base_chunk.ChunkException):
            chunk = chunks.cbd_chunk.CBDChunk()
