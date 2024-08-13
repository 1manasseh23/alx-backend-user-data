#!/usr/bin/env python3
"""
This a _hash_password method that takes in a password
string arguments and returns bytes
"""
import bcrypt
from db import DB
from user import User
from bcrypt import hashpw, gensalt
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt."""
    # Generate a salt
    salt = bcrypt.gensalt()
    # Hash the password with the generated salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a new user with the provided email and password."""
        try:
            # Check if the user already exists
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            # If no user is found, an exception might be raised,
            # depending on the implementation of `find_user_by`
            pass

        # Hash the password
        hashed_password = _hash_password(password)

        # Add the new user to the database
        new_user = self._db.add_user(email, hashed_password)

        # Return the User object
        return new_user
