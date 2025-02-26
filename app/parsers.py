from flask import jsonify

def parse_params_to_es_body(query, size, page):
    return {
        "query": {
            "match": {
                "suchtext": query
            },
        },
        "track_total_hits": True,
        "size": size,
        "from": (page - 1) * size,
    }

def parse_es_result_to_json(es_result, page):
    total_results = es_result['hits']['total']['value']
    page_size = len(es_result['hits']['hits'])

    return jsonify({
        'total_results': total_results,
        'page_size': page_size,
        'page': page,
        'results': es_result['hits']['hits']
    })
