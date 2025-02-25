import os

from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch
from dotenv import load_dotenv

from app.validations import validate_query_text

load_dotenv()
app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q')
    
    error = validate_query_text(query)

    if error:
        return error
    
    es_client = Elasticsearch(
        hosts=[os.getenv('ELASTIC_URL')],
        http_auth=(os.getenv('ELASTIC_USERNAME'), os.getenv('ELASTIC_PASSWORD')),
        verify_certs=False
    )
    
    body = {
        "query": {
            "match": {
                "suchtext": query
            },
        },
    }

    try:
        results = es_client.search(index='imago', body=body)
        print("#####")
        print(results['hits']['total'])
        return jsonify(results['hits']['hits'])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
