#!/usr/bin/python3
""" Authentication module """

from flask import request
from typing import List, TypeVar


class Auth:
    """ Auth class to manage API authentication """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Method to determine if authentication is required.
        Args:
            path (str): The path to check.
            excluded_paths (List[str]): List of paths that do not
            require authentication.
        Returns:
            bool: False for now, actual logic to be implemented later.
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        Method to get the Authorization header from the request.
        Args:
            request: The Flask request object.
        Returns:
            str: None for now, actual logic to be implemented later.
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Method to get the current user from the request.
        Args:
            request: The Flask request object.
        Returns:
            TypeVar('User'): None for now, actual
            logic to be implemented later.
        """
        return None
