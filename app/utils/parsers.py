from flask import jsonify

def parse_params_to_es_body(query, size, page, filter_fotografen=None, filter_datum=None, sort=None):
    body = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["suchtext", "fotografen"]
            }
        },
        "track_total_hits": True,
        "size": size,
        "from": (page - 1) * size,
    }

    if filter_fotografen or filter_datum:
        body["query"] = {
            "bool": {
                "must": [
                    {"match": {"suchtext": query}}
                ],
                "filter": []
            }
        }
        if filter_fotografen:
            body["query"]["bool"]["filter"].append({"term": {"fotografen": filter_fotografen}})
        if filter_datum:
            start, end = filter_datum.split(' TO ')
            body["query"]["bool"]["filter"].append({
                "range": {
                    "datum": {
                        "gte": start,
                        "lte": end
                    }
                }
            })

    if sort:
        field, order = sort.split(".")
        body["sort"] = [{field: {"order": order}}]

    return body

def parse_es_result_to_json(es_result, page):
    total_results = es_result['hits']['total']['value']
    page_size = len(es_result['hits']['hits'])

    return jsonify({
        'total_results': total_results,
        'page_size': page_size,
        'page': page,
        'results': es_result['hits']['hits']
    })
