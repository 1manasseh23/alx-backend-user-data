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
from typing import Union


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

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """Retrieve a User object from a session ID.
        Args:
            session_id (str): The ID of the session to retrieve the user from.
        Returns:
            Union[User, None]: A User object corresponding to the session ID if
            one exists, otherwise None.
        """
        # If the session ID is None or no user is found, return None
        if session_id is None:
            return None
        try:
            # Attempt to retrieve the user object corresponding to the session
            # ID from the database
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            # If no user object is found, return None
            return None
        # Otherwise return the corresponding user.
        return user

    def destroy_session(self, user_id: int) -> None:
        """Method to destroy the session associated with a user
        Args:
            user_id (int): The ID of the user whose session is to be destroyed.
        Returns:
            None
        """
        # If user ID is None, return None
        if user_id is None:
            return None
        # Update the user object in the database with a null session ID to
        # destroy the session - update it to None
        self._db.update_user(user_id, session_id=None)

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
        """Checks if a user's email and password are valid.
        Args:
            email (str): The email of the user.
            password (str): The password of the user.
        Returns:
            bool: True if the email and password match a registered user,
            False otherwise.
        """
        try:
            # Locate the user by email
            user = self._db.find_user_by(email=email)
            if user is not None:
                # Check if the password matches using bcrypt
                password_bytes = password.encode('utf-8')
                hashed_password = user.hashed_password
                if bcrypt.checkpw(password_bytes, hashed_password):
                    return True
        except NoResultFound:
            return False
        return False

    def get_reset_password_token(self, email: str) -> str:
        """Generates a password reset token for a user.

        Args:
            email (str): A string representing the email address of the user to
            generate a password reset token for.

        Raises:
            ValueError: If no user with the specified email address is found.

        Returns:
            str: A string representing the password reset token generated for
            the user.
        """
        # Find the user with the specified email address
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            user = None
        # If no user is found with specified email address, raise a ValueError
        if user is None:
            raise ValueError()
        # Generate a new password reset token & update the user's record in db
        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        # Return the generated password reset token
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """Updates a user's password using a reset token.
        Args:
            reset_token (str): The reset token associated with the user.
            password (str): The new password to set.
        Raises:
            ValueError: If the reset token is invalid (i.e., not associated
            with a user)..
        Returns:
            None
        """
        # Find user associated with reset_token
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            # If no user found with given reset_token, raise ValueError
            raise ValueError("Invalid reset token")
        # Hash the new password
        new_hashed_password = _hash_password(password)
        # Update the user's hashed password and the reset_token field to None
        self._db.update_user(
            user.id,
            hashed_password=new_hashed_password,
            reset_token=None,
        )
