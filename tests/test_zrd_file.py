import unittest

import sql.db
import zrd.zrd_file
from sql.elements import Ray, Segment

class TestZRDLoad(unittest.TestCase):
    def test_ZRD_load(self):
        """
        Check that we can load ZRD files alright.
        :return:
        """
        # Load a database without SQL at first
        db = zrd.zrd_file.ZRDFile('tests/basic.ZRD', enable_SQL=False)

        # Check that the SQL system is not initialized
        self.assertIsNone(db.engine)
        self.assertIsNone(db.session)

        # Check that the file is a CFD file
        self.assertEquals(db.file_type, 'CFD')

        # Check that the chunk bytecodes found in the database are 2048 and 6656
        chunk_types = db.chunk_type._chunk_objects.keys()
        self.assertEquals(chunk_types, [2048, 6656])

        # Now load the database with SQL enabled
        db = zrd.zrd_file.ZRDFile('tests/basic.ZRD', enable_SQL=True)

        # Check that the SQL system is initialized
        self.assertIsNotNone(db.engine)
        self.assertIsNotNone(db.session)

        # Check that the chunk bytecodes stored in the session are identical to those found in the file
        session_chunk_types = [query[0] for query in db.session.query(Segment.bytecode).all()]
        self.assertItemsEqual(chunk_types, session_chunk_types)

