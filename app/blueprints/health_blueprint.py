from flask import Blueprint, jsonify

health_blueprint = Blueprint('health_blueprint', __name__)

@health_blueprint.route("/healthcheck", methods=['GET'])
def hello_world():
    return jsonify({'message': 'Hello, World!'})
