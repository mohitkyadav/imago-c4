import unittest
from app import app

class TestHealthCheckEndpoint(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_health_check(self):
        response = self.app.get('/healthcheck')
        self.assertEqual(response.status_code, 200)
