#!/usr/bin/env python3
"""Module of Users views.
This module provides routes to handle CRUD operations for User objects.
"""

from flask import abort, jsonify, request
from api.v1.views import app_views
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def view_all_users() -> str:
    """GET /api/v1/users
    Retrieves a list of all User objects in JSON format.

    Returns:
        str: JSON list of all User objects.
    """
    all_users = [user.to_json() for user in User.all()]
    return jsonify(all_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def view_one_user(user_id: str = None) -> str:
    """GET /api/v1/users/<user_id>
    Retrieves a User object by ID in JSON format.

    Args:
        user_id (str): The ID of the User to retrieve.

    Returns:
        str: JSON representation of the User object.
        404 error if the User ID doesn't exist or
        is "me" without a logged-in user.
    """
    if user_id is None:
        abort(404)

    if user_id == 'me':
        if request.current_user is None:
            abort(404)
        return jsonify(request.current_user.to_json())

    user = User.get(user_id)
    if user is None:
        abort(404)

    return jsonify(user.to_json())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id: str = None) -> str:
    """DELETE /api/v1/users/<user_id>
    Deletes a User object by ID.

    Args:
        user_id (str): The ID of the User to delete.

    Returns:
        str: An empty JSON dictionary with a 200 status code if successful.
        404 error if the User ID doesn't exist.
    """
    if user_id is None:
        abort(404)

    user = User.get(user_id)
    if user is None:
        abort(404)

    user.remove()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user() -> str:
    """POST /api/v1/users/
    Creates a new User object.

    JSON body:
        - email (str): The email of the User.
        - password (str): The password of the User.
        - last_name (str, optional): The last name of the User.
        - first_name (str, optional): The first name of the User.

    Returns:
        str: JSON representation of the created User object.
        400 error if creation fails.
    """
    try:
        rj = request.get_json()
    except Exception:
        rj = None

    if rj is None:
        return jsonify({'error': "Wrong format"}), 400
    if rj.get("email", "") == "":
        return jsonify({'error': "email missing"}), 400
    if rj.get("password", "") == "":
        return jsonify({'error': "password missing"}), 400

    try:
        user = User()
        user.email = rj.get("email")
        user.password = rj.get("password")
        user.first_name = rj.get("first_name")
        user.last_name = rj.get("last_name")
        user.save()
        return jsonify(user.to_json()), 201

    except Exception as e:
        return jsonify({'error': f"Can't create User: {e}"}), 400


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id: str = None) -> str:
    """PUT /api/v1/users/<user_id>
    Updates a User object by ID.

    Args:
        user_id (str): The ID of the User to update.

    JSON body:
        - last_name (str, optional): The last name of the User.
        - first_name (str, optional): The first name of the User.

    Returns:
        str: JSON representation of the updated User object.
        404 error if the User ID doesn't exist.
        400 error if update fails.
    """
    if user_id is None:
        abort(404)

    user = User.get(user_id)
    if user is None:
        abort(404)

    try:
        rj = request.get_json()
    except Exception:
        rj = None

    if rj is None:
        return jsonify({'error': "Wrong format"}), 400

    if rj.get('first_name') is not None:
        user.first_name = rj.get('first_name')
    if rj.get('last_name') is not None:
        user.last_name = rj.get('last_name')

    user.save()
    return jsonify(user.to_json()), 200
