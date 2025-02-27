import os

from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch
from dotenv import load_dotenv

from app.parsers import parse_params_to_es_body, parse_es_result_to_json
from app.validations import validate_query_text

load_dotenv()
app = Flask(__name__)

@app.route("/healthcheck", methods=['GET'])
def hello_world():
    return jsonify({'message': 'Hello, World!'})

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q')
    size = request.args.get('size', default=10, type=int)
    page = request.args.get('page', default=1, type=int)
    filter_fotografen = request.args.get('filter_fotografen')
    filter_datum = request.args.get('filter_datum')
    sort = request.args.get('sort')

    error = validate_query_text(query)

    if error:
        return error
    
    es_client = Elasticsearch(
        hosts=[os.getenv('ELASTIC_URL')],
        http_auth=(os.getenv('ELASTIC_USERNAME'), os.getenv('ELASTIC_PASSWORD')),
        verify_certs=False
    )
    
    body = parse_params_to_es_body(query, size, page, filter_fotografen, filter_datum, sort)

    try:
        results = es_client.search(index='imago', body=body)
        return parse_es_result_to_json(results, page)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
