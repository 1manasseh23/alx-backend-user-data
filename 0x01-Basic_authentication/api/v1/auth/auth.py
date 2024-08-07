#!/usr/bin/python3
"""
Module to handle authentication.
"""

from flask import request
from typing import List, TypeVar

User = TypeVar('User')


class Auth:
    """
    Class to manage the API authentication.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines if a given path requires authentication.

        Args:
            path (str): The path to check.
            excluded_paths (List[str]): A list of paths that do not require
            authentication.

        Returns:
            bool: True if authentication is required, False otherwise.
        """
        if path is None:
            return True

        if excluded_paths is None or not excluded_paths:
            return True

        # Ensure path ends with a '/'
        if not path.endswith('/'):
            path += '/'

        for excluded_path in excluded_paths:
            if excluded_path.endswith('/') and path == excluded_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the value of the Authorization header from the request.

        Args:
            request (Request, optional): The Flask request object. Defaults
            to None.

        Returns:
            str: The value of the Authorization header, or None if the
            header is not present.
        """
        if request is None:
            return None

        return request.headers.get('Authorization')

    def current_user(self, request=None) -> User:
        """
        Retrieves the current user from the request.

        Args:
            request (Request, optional): The Flask request object. Defaults
            to None.

        Returns:
            User: The current user, or None if not available.
        """
        return None
