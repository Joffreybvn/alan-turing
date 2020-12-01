
from flask import Flask

# App blueprint imports
from src.api.v1 import blueprint as blueprint_v1


def create_api():

    # Initialize the Flask server
    flask = Flask(__name__)

    # Load the blueprints
    flask.register_blueprint(blueprint_v1, url_prefix='/v1')
    return flask
