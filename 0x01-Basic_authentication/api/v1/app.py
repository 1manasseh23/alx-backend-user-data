#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os
from api.v1.views import index

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


@app.errorhandler(401)
def unauthorized(error) -> str:
    """ Not found handler
    """
    return jsonify(
        {"error": "Unauthorized"}
        ), 401


@app.errorhandler(403)
def forbidden(error):
    """
    Error handler for 403 status code.
    Returns:
        JSON response with error message and 403 status code.
    """
    response = jsonify({"error": "Forbidden"})
    response.status_code = 403
    return response


if __name__ == "__main__":
    """Run the"""
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
