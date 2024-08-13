#!/usr/bin/env python3
from flask import Flask, request, jsonify, abort, make_response
from auth import Auth
import logging

# logging.disable(logging.WARNING)

app = Flask(__name__)

AUTH = Auth()


@app.route("/", methods=["GET"])
def welcome() -> str:
    """Route that returns a JSON payload."""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users() -> str:
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
def login() -> str:
    """Login function to handle user sessions."""
    # Extract form data
    email, password = request.form.get("email"), request.form.get("password")

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


@app.route('/sessions', methods=['DELETE'])
def logout() -> str:
    """Logout the user by deleting their session."""
    # Get the session_id from the cookies
    session_id = request.cookies.get('session_id')

    # Find the user by session_id
    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        # If the user does not exist, return a 403 HTTP status
        abort(403)

    # Destroy the session
    AUTH.destroy_session(user.id)

    # Redirect the user to the home page
    return redirect('/')


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile() -> str:
    """GET /profile
    Return:
        - A JSON payload containing the email if successful.
    """
    # Get the session ID from the "session_id" cookie in the request
    session_id = request.cookies.get("session_id")
    # Retrieve the user associated with the session ID
    user = AUTH.get_user_from_session_id(session_id)
    # If no user is found, abort the request with a 403 Forbidden error
    if user:
        return jsonify({'email': user.email}), 200
    else:
        abort(403)


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token() -> str:
    """POST /reset_password
    Return:
        - A JSON payload containing the email & reset token if successful.
    """
    # Retrieve the email from the form data
    email = request.form.get("email")
    try:
        # Attempt to generate a reset token for the given email
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        # If the email is not found in the database, raise a 403 error
        abort(403)
    # Return a JSON payload containing the email and reset token
    return jsonify({"email": email, "reset_token": reset_token})


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password() -> str:
    """PUT /reset_password
    Return:
        - The user's updated password.
    """
    # Retrieve the email, reset_token and new_password from the form data
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")
    try:
        # Attempt to update the password with the new password
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        # If the reset token is invalid, return an HTTP 403 error
        abort(403)
    # If the password was successfully updated, return a JSON object with the
    # user's email and a success message.
    return jsonify({"email": email, "message": "Password updated"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
