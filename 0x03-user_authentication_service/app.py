#!/usr/bin/env python3
from flask import Flask, request, jsonify, abort, make_response
from auth import Auth
import logging

logging.disable(logging.WARNING)

app = Flask(__name__)

AUTH = Auth()


@app.route("/", methods=["GET"])
def welcome():
    """Route that returns a JSON payload."""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users():
    """POST /users route to register a new user."""
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        return jsonify({"message": "email and password are required"}), 400

    try:
        # Attempt to register the user
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"}), 200
    except ValueError:
        # If the user already exists, return an error message
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login():
    """Login function to handle user sessions."""
    # Extract form data
    email = request.form.get('email')
    password = request.form.get('password')

    # Validate credentials
    if not AUTH.valid_login(email, password):
        abort(401)  # Unauthorized if login fails

    # Create a session and generate session ID
    session_id = AUTH.create_session(email)

    # Prepare the response
    response = jsonify({"email": email, "message": "logged in"})

    # Set the session_id in the response cookie
    response.set_cookie("session_id", session_id)

    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
