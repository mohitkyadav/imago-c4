import os

from flask import request, jsonify, Blueprint
from elasticsearch import Elasticsearch
import logging

from app.utils.parsers import parse_params_to_es_body, parse_es_result_to_json
from app.utils.validations import validate_query_text

search_blueprint = Blueprint('search_blueprint', __name__)

@search_blueprint.route("/search", methods=['GET'])
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
    except ConnectionError as e:
        return jsonify({'error': 'Connection error to Elasticsearch'}), 500
    except Exception as e:
        logging.error(f"Error processing search: {e}")
        return jsonify({'error': str(e)}), 500
