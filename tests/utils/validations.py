import unittest
from app.utils.validations import validate_query_text

class TestValidateQueryText(unittest.TestCase):

    def test_missing_query(self):
        result = validate_query_text(None)
        self.assertEqual(result[0]['error'], 'Search query is required')
        self.assertEqual(result[1], 400)

    def test_query_too_short(self):
        result = validate_query_text('ab')
        self.assertEqual(result[0]['error'], 'Search query must be at least 3 characters long')
        self.assertEqual(result[1], 400)

    def test_query_too_long(self):
        result = validate_query_text('a' * 101)
        self.assertEqual(result[0]['error'], 'Search query must be at most 100 characters long')
        self.assertEqual(result[1], 400)

    def test_valid_query(self):
        result = validate_query_text('Hello')
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
