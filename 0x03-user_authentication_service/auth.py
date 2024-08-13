#!/usr/bin/env python3
"""
This a _hash_password method that takes in a password
string arguments and returns bytes
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt."""
    # Generate a salt
    salt = bcrypt.gensalt()
    # Hash the password with the generated salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password
