#!/usr/bin/python3
""" Flask Application """
from models import storage
from os import environ
from flask import Flask, render_template, make_response, jsonify
from flask_cors import CORS
from flasgger import Swagger
from flasgger.utils import swag_from
from. import app  
from api.v1.views import app_views

app.register_blueprint(app_views) 

cors = CORS(app, resources={r"/*": {"origins": "*"}}) 


@app.teardown_appcontext
def close_db(error):
    """ Close Storage """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ 404 Error
    ---
    responses:
      404:
        description: a resource was not found
    """
    return make_response(jsonify({'error': "Not found"}), 404)



if __name__ == "__main__":
    """ Main Function """
    host = environ.get('JOPMED_API_HOST')
    port = environ.get('JOPMED_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True)
