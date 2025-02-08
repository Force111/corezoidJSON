import unittest
import random
from testtask import fill_randomdata
class TestingTESTTASK(unittest.TestCase):
    def setUp(self):
        self.schema = {
            "definitions": {
                "attendees": {
                    "type": "object",
                    "properties": {
                        "userId": {"type": "integer"},
                        "access": {"enum": ["view", "modify", "execute"]}
                    },
                    "required": ["userId", "access"]
                }
            },
            "type": "object",
            "properties": {
                "id": {"anyOf": [{"type": "integer"}]},
                "title": {"type": "string"},
                "description": {"type": "string"},
                "startDate": {"type": "integer"},
                "endDate": {"type": "integer"},
                "attendees": {
                    "type": "array",
                    "items": {"$ref": "#attendees"}
                }
            },
            "required": ["id", "title", "description", "startDate", "endDate", "attendees"]
        }
    def test_anyof(self):
        for _ in range(5):
            random_data = fill_randomdata(self.schema)
            self.assertTrue(isinstance(random_data["id"], (str, int)))
    def test_ref_resolution(self):
        random_data = fill_randomdata(self.schema)
        self.assertGreater(len(random_data["attendees"]), 0)
        for attendee in random_data["attendees"]:
            self.assertIn("userId", attendee)
            self.assertIn("access", attendee)
            self.assertIsInstance(attendee["userId"], int)
            self.assertIn(attendee["access"], ["view", "modify", "execute"])

if __name__ == "__main__":
    unittest.main()
