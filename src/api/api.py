
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

# App blueprint imports
from src.api.v1 import blueprint as blueprint_v1


def create_api():

    # Initialize the Flask server
    flask = Flask(__name__)

    # Fix the Swagger UI https
    flask.wsgi_app = ProxyFix(flask.wsgi_app, x_proto=1, x_host=1)

    # Load the blueprints
    flask.register_blueprint(blueprint_v1, url_prefix='/v1')
    return flask
