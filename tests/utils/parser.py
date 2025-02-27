import unittest
from app.utils.parsers import parse_params_to_es_body, parse_es_result_to_json
import json

class TestParseParamsToEsBody(unittest.TestCase):

    def test_default_query(self):
        query = "Hello World"
        size = 10
        page = 1
        body = parse_params_to_es_body(query, size, page)
        self.assertEqual(body['query']['multi_match']['query'], query)
        self.assertEqual(body['size'], size)
        self.assertEqual(body['from'], 0)

    def test_query_with_filter_fotografen(self):
        query = "Hello World"
        size = 10
        page = 1
        filter_fotografen = "ZUMA Press Wire"
        body = parse_params_to_es_body(query, size, page, filter_fotografen=filter_fotografen)
        self.assertEqual(body['query']['bool']['must'][0]['match']['suchtext'], query)
        self.assertEqual(body['query']['bool']['filter'][0]['term']['fotografen'], filter_fotografen)

    def test_query_with_filter_datum(self):
        query = "Hello World"
        size = 10
        page = 1
        filter_datum = "2022-01-01 TO 2022-12-31"
        body = parse_params_to_es_body(query, size, page, filter_datum=filter_datum)
        self.assertEqual(body['query']['bool']['must'][0]['match']['suchtext'], query)
        self.assertEqual(body['query']['bool']['filter'][0]['range']['datum']['gte'], '2022-01-01')
        self.assertEqual(body['query']['bool']['filter'][0]['range']['datum']['lte'], '2022-12-31')

    def test_query_with_sort(self):
        query = "Hello World"
        size = 10
        page = 1
        sort = "datum.asc"
        body = parse_params_to_es_body(query, size, page, sort=sort)
        self.assertEqual(body['sort'][0]['datum']['order'], 'asc')

class TestParseEsResultToJson(unittest.TestCase):

    def test_parse_es_result(self):
        es_result = {
            'hits': {
                'total': {'value': 100},
                'hits': [
                    {'_source': {'suchtext': 'Example result'}},
                    {'_source': {'suchtext': 'Another result'}}
                ]
            }
        }
        page = 1
        response = parse_es_result_to_json(es_result, page)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data['total_results'], 100)
        self.assertEqual(data['page_size'], 2)
        self.assertEqual(data['page'], 1)
        self.assertEqual(len(data['results']), 2)

if __name__ == '__main__':
    unittest.main()
