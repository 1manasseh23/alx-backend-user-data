#!/usr/bin/env python3
"""
This a _hash_password method that takes in a password
string arguments and returns bytes
"""
import bcrypt
from db import DB
from typing import Optional
from user import User
from bcrypt import hashpw, gensalt
from sqlalchemy.orm.exc import NoResultFound
import uuid


def _generate_uuid() -> str:
    """Generate a new UUID and return its string representation."""
    return str(uuid.uuid4())


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

    def create_session(self, email: str) -> str:
        """Creates a session and returns the session ID as a string.
        Args:
            email (str): Email of user to create session for.
        Returns:
            str: Session ID.
        """
        try:
            # Find the user corresponding to the email
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            # Return None if no user is found with given email
            return None
        # If user is None, return None
        if user is None:
            return None
        # Generate a new UUID and store it in the db as the user’s session_id
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        # Return the session ID.
        return session_id

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

    def valid_login(self, email: str, password: str) -> bool:
        """Validate login credentials."""
        try:
            # Locate the user by email
            user = self._db.find_user_by(email=email)
            if not user:
                return False

            # Check if the provided password matches the stored hashed password
            if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
                return True
            else:
                return False

        except Exception:
            return False
