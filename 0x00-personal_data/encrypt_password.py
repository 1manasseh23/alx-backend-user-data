#!/usr/bin/env python3
"""User passwords should NEVER be stored in plain text in a database"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hash a password with bcrypt and return the hashed password.

    :param password: The plain text password to hash.
    :return: The hashed password as a byte string.
    """
    # Convert the password to bytes if it's a string
    password_bytes = password.encode('utf-8')

    # Generate a salt and hash the password with the salt
    hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())

    return hashed_password
