import unittest

import sql.db
import sql.elements

class TestObjectInstantiation(unittest.TestCase):
    def test_ray_instantiation(self):
        """
        Instantiate a ray object
        :return:
        """
        ray = sql.elements.Ray()
        self.assertIsNone(ray.id)

    def test_segment_instantiation(self):
        """
        Instantiate a segment object
        :return:
        """
        segment = sql.elements.Segment()
        self.assertIsNone(segment.id)

    def test_segment_assignment(self):
        """
        Create a segment and then assign it to a ray
        :return:
        """
        # Create a ray and a segment to attach to it
        ray = sql.elements.Ray()
        segment = sql.elements.Segment()

        # Check that the ray has no segments attached to it and the segment number is not yet assigned
        self.assertNotIn(segment, ray.segments)
        self.assertEqual(len(ray.segments), 0)
        self.assertIsNone(segment.segment_number)

        # Append the new segment to the ray
        ray.segments.append(segment)

        # Check that there is now one segment attached to the ray, that it's the one we just appended, and that the
        # segment references the correct parent ray
        self.assertEqual(len(ray.segments), 1)
        self.assertIn(segment, ray.segments)
        self.assertEqual(segment.parent, ray.id)

        # The segment should have segment number 0 now
        self.assertEqual(segment.segment_number, 0)

        # Create and append a second segment to the end of the list
        segment2 = sql.elements.Segment()
        ray.segments.append(segment2)

        # The new segment should be segment number 1
        self.assertEqual(segment.segment_number, 0)
        self.assertEqual(segment2.segment_number, 1)

        # Create and append a second segment to the start of the list
        segment3 = sql.elements.Segment()
        ray.segments.insert(0, segment3)

        # Now check that the other segments have renumbered to match the new numbering
        self.assertEqual(segment3.segment_number, 0)
        self.assertEqual(segment.segment_number, 1)
        self.assertEqual(segment2.segment_number, 2)