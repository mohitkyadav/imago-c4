import os

from flask import request, jsonify, Blueprint
from elasticsearch import Elasticsearch
from collections import defaultdict, Counter

from app.analytics.decorators import log_execution_time
from app.analytics.logger import LOG
from app.utils.parsers import parse_params_to_es_body, parse_es_result_to_json
from app.utils.validations import validate_query_text

# To not overengineer it, I'm just tracking it in memory 🫣
# A proper solution can be a db or a cache
query_frequencies = defaultdict(int)
search_stats = Counter()

search_blueprint = Blueprint('search_blueprint', __name__)

@search_blueprint.route("/search", methods=['GET'])
@log_execution_time("Search operation")
def search():
    query = request.args.get('q')
    # This is a global variable that will store the frequency of each query
    query_frequencies[query] += 1
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
        search_stats['successful'] += 1
        return parse_es_result_to_json(results, page)
    except ConnectionError as e:
        search_stats['failed'] += 1
        LOG.error(f"Error connecting to Elasticsearch: {e}")
        return jsonify({'error': 'Connection error to Elasticsearch'}), 500
    except Exception as e:
        search_stats['failed'] += 1
        LOG.error(f"Error processing search: {e}")
        return jsonify({'error': str(e)}), 500

@search_blueprint.route("/search/stats", methods=['GET'])
def get_most_common_queries():
    top_five_queries = [{'query': k, 'count': v} for k, v in sorted(query_frequencies.items(),
                                                                    key=lambda x: x[1], reverse=True)[:5]]
    return {
        'top_five_queries': top_five_queries,
        'search_stats': dict(search_stats)
    }
