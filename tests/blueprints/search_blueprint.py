import unittest
from unittest.mock import patch

from app import app


class TestSearchEndpoint(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    @patch.dict('os.environ', {
        'ELASTIC_URL': 'http://mock-elastic-url.com:2033',
        'ELASTIC_USERNAME': 'mock-username',
        'ELASTIC_PASSWORD': 'mock-password'
    })
    @patch('elasticsearch.Elasticsearch.search')
    def test_search_bad_request(self, mock_es):
        response = self.app.get('/search')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {'error': 'Search query is required'})

    @patch.dict('os.environ', {
        'ELASTIC_URL': 'http://mock-elastic-url.com:2033',
        'ELASTIC_USERNAME': 'mock-username',
        'ELASTIC_PASSWORD': 'mock-password'
    })
    @patch('elasticsearch.Elasticsearch.search')
    def test_search_successful(self, mock_es):
        mock_es.return_value = {
            'hits': {
                'total': {'value': 2},
                'hits': [
                    {'_source': {'suchtext': 'Example result'}},
                    {'_source': {'suchtext': 'Another result'}}
                ]
            }
        }

        response = self.app.get('/search?q=Big%20Sur')
        data = response.json
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['page'], 1)
        self.assertEqual(data['total_results'], 2)

    @patch.dict('os.environ', {
        'ELASTIC_URL': 'http://mock-elastic-url.com:2033',
        'ELASTIC_USERNAME': 'mock-username',
        'ELASTIC_PASSWORD': 'mock-password'
    })
    @patch('elasticsearch.Elasticsearch.search')
    def test_get_search_stats(self, mock_es):
        mock_es.return_value = {
            'hits': {
                'total': {'value': 2},
                'hits': [
                    {'_source': {'suchtext': 'Example result'}},
                    {'_source': {'suchtext': 'Another result'}}
                ]
            }
        }

        _ = self.app.get('/search?q=Big%20Sur')

        response = self.app.get('/search/stats')
        data = response.json
        print(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['search_stats'], {'successful': 1})
        self.assertEqual(data['top_five_queries'], [{'count': 1, 'query': 'Big Sur'}])

if __name__ == '__main__':
    unittest.main()
