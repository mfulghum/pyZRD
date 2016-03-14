import unittest

import sql.db
import sql.elements

class TestSQLConnection(unittest.TestCase):
    def test_initialization(self):
        """
        Start up the SQLAlchemy engine and initialize the database, then shut it all down.
        :return:
        """
        # Initialize the database.
        session, engine = sql.db.initialize_database(verbose=False)

        # Check that the database is shut down.
        self.assertIsNotNone(engine)
        self.assertIsNotNone(session)

        # Shut the database down.
        sql.db.shutdown_database(session, engine)

class TestSQLCommit(unittest.TestCase):
    def setUp(self):
        """

        :return:
        """
        self.session, self.engine = sql.db.initialize_database(verbose=False)

    def test_commit(self):
        """
        Start up the SQLAlchemy engine and initialize the database
        :return:
        """
        # First make sure that we have a SQL session
        self.assertIsNotNone(self.engine)
        self.assertIsNotNone(self.session)

        # Create a ray element without assigning an ID
        ray = sql.elements.Ray()

        # The ID should be None
        self.assertIsNone(ray.id)

        # Add the ray to the session
        self.session.add(ray)

        # The ID should *still* be None
        self.assertIsNone(ray.id)

        # Commit the change
        self.session.commit()

        # Now that the ray has been added, the ray ID should now be 1
        self.assertEqual(ray.id, 1)

    def tearDown(self):
        """
        Shut down the SQL database
        :return:
        """
        sql.db.shutdown_database(self.session, self.engine)