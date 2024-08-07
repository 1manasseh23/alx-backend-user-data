#!/usr/bin/env python3
"""
Main application module for API.
"""
from flask import Flask, jsonify, abort, request
from flask_cors import CORS
import os
from api.v1.views.index import app_views

app = Flask(__name__)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
app.register_blueprint(app_views)

auth = None

# Check the AUTH_TYPE environment variable and initialize auth accordingly
auth_type = os.getenv('AUTH_TYPE')

if auth_type == 'auth':
    from api.v1.auth.auth import Auth
    auth = Auth()

@app.errorhandler(401)
def unauthorized_error(error):
    """
    Handles 401 Unauthorized errors.
    """
    response = jsonify({"error": "Unauthorized"})
    response.status_code = 401
    return response

@app.errorhandler(403)
def forbidden_error(error):
    """
    Handles 403 Forbidden errors.
    """
    response = jsonify({"error": "Forbidden"})
    response.status_code = 403
    return response

@app.before_request
def before_request():
    """
    Method to handle operations before each request.
    """
    if auth is None:
        return

    excluded_paths = ['/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/']
    if not auth.require_auth(request.path, excluded_paths):
        return

    if auth.authorization_header(request) is None:
        abort(401)

    if auth.current_user(request) is None:
        abort(403)

if __name__ == "__main__":
    host = os.getenv("API_HOST", "0.0.0.0")
    port = os.getenv("API_PORT", "5000")
    app.run(host=host, port=port)
