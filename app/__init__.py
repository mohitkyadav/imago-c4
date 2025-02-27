from flask import Flask
from app.blueprints.health_blueprint import health_blueprint
from app.blueprints.search_blueprint import search_blueprint

app = Flask(__name__)
app.register_blueprint(health_blueprint)
app.register_blueprint(search_blueprint)
